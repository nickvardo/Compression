import cv2
import numpy as np
import time
import os

def jpeg_compression(image_path):
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

    # Συμπίεση JPEG
    start_time = time.time()
    _, compressed_data = cv2.imencode('.jpg', image)
    end_time = time.time()
    compressed_image = cv2.imdecode(compressed_data, 1)

    # Πληροφορίες μετά τη συμπίεση
    print("\nΜετά τη συμπίεση:")
    print("Μέγεθος συμπιεσμένης εικόνας:", compressed_image.shape)
    print("Μέγεθος συμπιεσμένης εικόνας (πλάτος x ύψος):", compressed_image.shape[1], "x", compressed_image.shape[0])
    print("Μέγεθος συμπιεσμένης εικόνας σε bytes:", len(compressed_data))
    print("Χρόνος συμπίεσης:", end_time - start_time, "δευτερόλεπτα")

    # Υπολογισμός διαφοράς σε μέγεθος αρχείου μεταξύ αρχικής και συμπιεσμένης εικόνας
    difference = image_size - len(compressed_data)
    print("Διαφορά μεταξύ συμπιεσμένου και αρχικού μεγέθους:", difference, "bytes")

    # Προβολή της αρχικής και της συμπιεσμένης εικόνας για σύγκριση
    cv2.imshow("Αρχική εικόνα", image)
    cv2.imshow("Συμπιεσμένη εικόνα", compressed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Ο αλγόριθμος συμπίεσης που εφαρμόστηκε
    algorithm_name = "JPEG"
    print("Ο αλγόριθμος συμπίεσης που εφαρμόστηκε είναι ο", algorithm_name)

    # Το όνομα του χρήστη που εκτέλεσε το πρόγραμμα
    user_name = "Νικόλαος Βαρδονικολάκης"  # Αντικατάστησε αυτό με το πραγματικό σου όνομα
    print("Ο χρήστης που εκτέλεσε το πρόγραμμα είναι ο", user_name)

# Κλήση της συνάρτησης με το όνομα του αρχείου εικόνας
jpeg_compression("my_image.png")
