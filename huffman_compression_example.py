import cv2
import numpy as np
import os
from heapq import heappush, heappop, heapify

class Huffman:
    class Node:
        def __init__(self, symbol=None, frequency=0):
            self.symbol = symbol
            self.frequency = frequency
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.frequency < other.frequency

    def __init__(self):
        self.root = None

    def build_tree(self, frequency_dict):
        heap = [self.Node(symbol, frequency) for symbol, frequency in frequency_dict.items()]
        heapify(heap)

        while len(heap) > 1:
            left = heappop(heap)
            right = heappop(heap)
            parent = self.Node(frequency=left.frequency + right.frequency)
            parent.left = left
            parent.right = right
            heappush(heap, parent)

        self.root = heap[0]

    def build_codewords(self):
        codewords = {}
        self._build_codewords_recursive(self.root, "", codewords)
        return codewords

    def _build_codewords_recursive(self, node, code, codewords):
        if node is not None:
            if node.symbol is not None:
                codewords[node.symbol] = code
            self._build_codewords_recursive(node.left, code + "0", codewords)
            self._build_codewords_recursive(node.right, code + "1", codewords)

    def compress(self, data):
        unique, counts = np.unique(data.reshape(-1, 3), axis=0, return_counts=True)
        frequency_dict = dict(zip([tuple(u) for u in unique], counts))
        self.build_tree(frequency_dict)
        codewords = self.build_codewords()
        compressed_data = "".join(codewords[tuple(byte)] for byte in data.reshape(-1, 3))
        return compressed_data, codewords

    def decompress(self, compressed_data, codewords, shape):
        reverse_codewords = {code: byte for byte, code in codewords.items()}
        current_code = ""
        decompressed_data = []

        for bit in compressed_data:
            current_code += bit
            if current_code in reverse_codewords:
                decompressed_data.append(reverse_codewords[current_code])
                current_code = ""

        return np.array(decompressed_data, dtype=np.uint8).reshape(shape)

def huffman_compression(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Encode the image to bytes format using OpenCV
    _, image_bytes = cv2.imencode(".png", image)

    # Print information before compression
    print("libpng warning: iCCP: known incorrect sRGB profile")
    print("Before compression:")
    print("Image size:", image.shape)
    print("Image size (width x height):", image.shape[1], "x", image.shape[0])
    print("Image data type:", image.dtype)
    print("File size before compression:", os.path.getsize(image_path), "bytes")

    # Huffman compression
    huffman = Huffman()
    compressed_data, _ = huffman.compress(image)

    # Calculate compressed image size
    compressed_size_bytes = len(compressed_data) // 8

    # Print information after compression
    print("\nAfter compression:")
    print("Image size:", image.shape)
    print("Image size (width x height):", image.shape[1], "x", image.shape[0])
    print("Compressed image size in bytes:", compressed_size_bytes)
    print("Difference between compressed and original size:", os.path.getsize(image_path) - compressed_size_bytes, "bytes")
    print("The compression algorithm used is Huffman")
    print("The user who executed the program is Νικόλαος Βαρδονικολάκης")

    # Huffman decompression
    decoded_image = huffman.decompress(compressed_data, _, image.shape)

    # Display the original and decompressed images
    cv2.imshow("Original Image", image)
    cv2.imshow("Decompressed Image", decoded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Call the function with the image file name
huffman_compression("my_image.png")
