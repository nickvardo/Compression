import cv2

image = cv2.imread('my_image.jpg')
if image is not None:
    print("Η εικόνα φορτώθηκε επιτυχώς!")
    print("Πληροφορίες αρχείου εικόνας:")
    print(image.shape)  # Διαστάσεις εικόνας (ύψος, πλάτος, κανάλια)
    print(image.dtype)  # Τύπος δεδομένων εικόνας
else:
    print("Αδυναμία φόρτωσης της εικόνας. Ελέγξτε το όνομα και την τοποθεσία του αρχείου.")
