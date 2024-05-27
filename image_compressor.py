import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import time
import matplotlib.pyplot as plt

class ImageCompressor:
    def __init__(self, master):
        self.master = master
        self.master.title("Εργαλείο Συμπίεσης Εικόνας")
        self.master.geometry("600x500")

        self.load_button = tk.Button(master, text="Φόρτωση Εικόνας", command=self.load_image)
        self.load_button.pack()

        self.quality_label = tk.Label(master, text="Επιλογή Ποιότητας (0-100):")
        self.quality_label.pack()

        self.quality_scale = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
        self.quality_scale.set(90)
        self.quality_scale.pack()

        self.algorithm_label = tk.Label(master, text="Επιλογή Αλγορίθμου Συμπίεσης:")
        self.algorithm_label.pack()

        self.algorithm_var = tk.StringVar(master)
        self.algorithm_var.set("JPEG")
        self.algorithm_menu = tk.OptionMenu(master, self.algorithm_var, "JPEG", "Huffman", "LZW")
        self.algorithm_menu.pack()

        self.compress_button = tk.Button(master, text="Συμπίεση Εικόνας", command=self.compress_image)
        self.compress_button.pack()

        self.preview_button = tk.Button(master, text="Προεπισκόπηση Εικόνας", command=self.preview_image)
        self.preview_button.pack()

        self.save_button = tk.Button(master, text="Αποθήκευση Εικόνας", command=self.save_image)
        self.save_button.pack()

        self.history_button = tk.Button(master, text="Προβολή Ιστορικού Συμπίεσης", command=self.show_history)
        self.history_button.pack()

        self.undo_button = tk.Button(master, text="Αναίρεση Τελευταίας Συμπίεσης", command=self.undo_last_compression)
        self.undo_button.pack()

        self.image_path = ""
        self.compressed_data = None
        self.history = []

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            messagebox.showinfo("Εικόνα Φορτώθηκε", "Η εικόνα φορτώθηκε επιτυχώς!")
            self.history.append((self.image_path, self.image.copy(), None))

    def compress_image(self):
        if not self.image_path:
            messagebox.showwarning("Σφάλμα", "Παρακαλώ φορτώστε πρώτα μια εικόνα.")
            return

        quality = self.quality_scale.get()
        algorithm = self.algorithm_var.get()

        start_time = time.time()
        if algorithm == "JPEG":
            _, self.compressed_data = cv2.imencode('.jpg', self.image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        elif algorithm == "Huffman":
            # Εδώ θα μπορούσε να μπει ο κώδικας για συμπίεση με Huffman
            self.compressed_data = self.huffman_compress(self.image)
        elif algorithm == "LZW":
            # Εδώ θα μπορούσε να μπει ο κώδικας για συμπίεση με LZW
            self.compressed_data = self.lzw_compress(self.image)
        end_time = time.time()

        compressed_image = cv2.imdecode(self.compressed_data, 1)

        original_size = cv2.imread(self.image_path).nbytes
        compressed_size = len(self.compressed_data)
        difference = original_size - compressed_size

        stats = (
            f"Μέγεθος αρχείου πριν τη συμπίεση: {original_size} bytes\n"
            f"Μέγεθος αρχείου μετά τη συμπίεση: {compressed_size} bytes\n"
            f"Διαφορά μεγέθους: {difference} bytes\n"
            f"Χρόνος συμπίεσης: {end_time - start_time} δευτερόλεπτα"
        )

        messagebox.showinfo("Στατιστικά Συμπίεσης", stats)

        cv2.imshow("Αρχική Εικόνα", self.image)
        cv2.imshow("Συμπιεσμένη Εικόνα", compressed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        self.history.append((self.image_path, self.image.copy(), self.compressed_data))

    def save_image(self):
        if self.compressed_data is None:
            messagebox.showwarning("Σφάλμα", "Παρακαλώ εκτελέστε πρώτα τη συμπίεση.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if save_path:
            with open(save_path, 'wb') as f:
                f.write(self.compressed_data)
                messagebox.showinfo("Αποθήκευση", "Η συμπιεσμένη εικόνα αποθηκεύτηκε επιτυχώς!")

    def show_history(self):
        if not self.history:
            messagebox.showinfo("Ιστορικό", "Δεν υπάρχει ιστορικό συμπίεσης.")
            return

        history_text = ""
        for i, (path, _, compressed_data) in enumerate(self.history):
            original_size = cv2.imread(path).nbytes
            compressed_size = len(compressed_data) if compressed_data is not None else original_size
            difference = original_size - compressed_size
            history_text += (
                f"Συμπίεση {i + 1}:\n"
                f"  Αρχείο: {path}\n"
                f"  Μέγεθος αρχείου πριν τη συμπίεση: {original_size} bytes\n"
                f"  Μέγεθος αρχείου μετά τη συμπίεση: {compressed_size} bytes\n"
                f"  Διαφορά μεγέθους: {difference} bytes\n"
            )

        messagebox.showinfo("Ιστορικό Συμπίεσης", history_text)

    def undo_last_compression(self):
        if len(self.history) < 2:
            messagebox.showwarning("Σφάλμα", "Δεν υπάρχει προηγούμενη συμπίεση για αναίρεση.")
            return

        self.history.pop()
        self.image_path, self.image, self.compressed_data = self.history[-1]
        messagebox.showinfo("Αναίρεση", "Η τελευταία συμπίεση αναιρέθηκε.")

    def preview_image(self):
        if self.compressed_data is None:
            messagebox.showwarning("Σφάλμα", "Παρακαλώ εκτελέστε πρώτα τη συμπίεση.")
            return

        compressed_image = cv2.imdecode(self.compressed_data, 1)
        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.title("Αρχική Εικόνα")
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title("Συμπιεσμένη Εικόνα")
        plt.imshow(cv2.cvtColor(compressed_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.show()

    def huffman_compress(self, image):
        # Παράδειγμα κώδικα για Huffman συμπίεση
        # Αυτός είναι ένας placeholder, πρέπει να υλοποιηθεί κατάλληλα
        _, compressed_data = cv2.imencode('.png', image)
        return compressed_data

    def lzw_compress(self, image):
        # Παράδειγμα κώδικα για LZW συμπίεση
        # Αυτός είναι ένας placeholder, πρέπει να υλοποιηθεί κατάλληλα
        _, compressed_data = cv2.imencode('.png', image)
        return compressed_data

    def analyze_compression_quality(self):
        quality_values = [50, 60, 70, 80, 90, 100]  # Διαφορετικές ποιότητες συμπίεσης που θα εξεταστούν
        compression_results = []

        for quality in quality_values:
            start_time = time.time()
            _, compressed_data = cv2.imencode('.jpg', self.image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            end_time = time.time()

            compressed_image = cv2.imdecode(compressed_data, 1)

            original_size = cv2.imread(self.image_path).nbytes
            compressed_size = len(compressed_data)

            compression_results.append({
                'quality': quality,
                'compression_ratio': original_size / compressed_size,
                'compression_time': end_time - start_time
            })

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot([result['quality'] for result in compression_results], [result['compression_ratio'] for result in compression_results], marker='o')
        plt.title('Αναλογία Συμπίεσης σε Ποιότητα')
        plt.xlabel('Ποιότητα')
        plt.ylabel('Αναλογία Συμπίεσης')

        plt.subplot(1, 2, 2)
        plt.plot([result['quality'] for result in compression_results], [result['compression_time'] for result in compression_results], marker='o')
        plt.title('Χρόνος Συμπίεσης σε Ποιότητα')
        plt.xlabel('Ποιότητα')
        plt.ylabel('Χρόνος Συμπίεσης (δευτερόλεπτα)')

        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressor(root)
    root.mainloop()