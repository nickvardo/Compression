import cv2
import numpy as np
import time
import os
from io import BytesIO
from PIL import Image

class LZW:
    def __init__(self):
        self.dictionary_size = 256
        self.dictionary = {bytes([i]): i for i in range(self.dictionary_size)}

    def compress(self, data):
        compressed_data = []
        buffer = b''
        for byte in data:
            new_buffer = buffer + bytes([byte])
            if new_buffer in self.dictionary:
                buffer = new_buffer
            else:
                compressed_data.append(self.dictionary[buffer])
                if len(self.dictionary) < 65536:
                    self.dictionary[new_buffer] = len(self.dictionary)
                buffer = bytes([byte])
        if buffer in self.dictionary:
            compressed_data.append(self.dictionary[buffer])
        return compressed_data

    def decompress(self, compressed_data):
        decompressed_data = []
        reverse_dictionary = {v: k for k, v in self.dictionary.items()}
        previous_sequence = bytes([compressed_data[0]])
        decompressed_data.append(previous_sequence)
        for code in compressed_data[1:]:
            if code in reverse_dictionary:
                sequence = reverse_dictionary[code]
            elif code == len(self.dictionary):
                sequence = previous_sequence + bytes([previous_sequence[0]])
            else:
                raise ValueError("Μη έγκυρα συμπιεσμένα δεδομένα")
            decompressed_data.append(sequence)
            self.dictionary[len(self.dictionary)] = previous_sequence + sequence[:1]
            previous_sequence = sequence
        return b''.join(decompressed_data)

def jpeg_compression(image_path):
    algorithm_name = "LZW"
    user_name = "Νικόλαος Βαρδονικολάκης"  # Αντικατάστησε αυτό με το πραγματικό σου όνομα

    # Φόρτωση της εικόνας από το αρχείο
    image = cv2.imread(image_path)

    # Πληροφορίες πριν τη συμπίεση
    print("Πριν τη συμπίεση:")
    print("Μέγεθος εικόνας:", image.shape)
    print("Μέγεθος εικόνας (πλάτος x ύψος):", image.shape[1], "x", image.shape[0])
    print("Τύπος εικόνας:", image.dtype)

    # Μέγεθος αρχείου πριν τη συμπίεση
    image_size = os.path.getsize(image_path)
    print("Μέγεθος αρχείου πριν τη συμπίεση:", image_size, "bytes")

    # Συμπίεση LZW
    lzw = LZW()
    compressed_data = lzw.compress(image.tobytes())

    # Πληροφορίες μετά τη συμπίεση
    print("\nΜετά τη συμπίεση:")
    print("Μέγεθος συμπιεσμένης εικόνας:", image.shape)
    print("Μέγεθος συμπιεσμένης εικόνας (πλάτος x ύψος):", image.shape[1], "x", image.shape[0])
    compressed_size = len(compressed_data)
    print("Μέγεθος συμπιεσμένης εικόνας σε bytes:", compressed_size, "bytes")
    print("Διαφορά μεταξύ συμπιεσμένου και αρχικού μεγέθους:", image_size - compressed_size, "bytes")

    # Αποσυμπίεση των συμπιεσμένων δεδομένων
    decompressed_data = lzw.decompress(compressed_data)

    # Μετατροπή των δεδομένων σε εικόνα
    width = image.shape[1]
    height = image.shape[0]
    decompressed_image = np.frombuffer(decompressed_data, dtype=np.uint8).reshape((height, width, 3))

    # Εμφάνιση της αρχικής και της αποσυμπιεσμένης εικόνας για σύγκριση
    original_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    decompressed_image = Image.fromarray(cv2.cvtColor(decompressed_image, cv2.COLOR_BGR2RGB))

    # Εμφάνιση των εικόνων σε δύο διαφορετικά παράθυρα
    cv2.imshow("Αρχική Εικόνα", np.array(original_image))
    cv2.imshow("Αποσυμπιεσμένη Εικόνα", np.array(decompressed_image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Ο αλγόριθμος συμπίεσης που εφαρμόστηκε είναι ο", algorithm_name)
    print("Ο χρήστης που εκτέλεσε το πρόγραμμα είναι ο", user_name)

# Κλήση της συνάρτησης με το όνομα του αρχείου εικόνας
jpeg_compression("my_image.png")
