from itertools import zip_longest

from PIL import Image

path_to_image = input("Path to image: ")
image = Image.open(path_to_image)
pixels = image.load()
bits = []
for i in range(image.size[1]):
    for j in range(image.size[0]):
        for channel in range(3):
            bits.append(pixels[j, i][channel] & 1)
args = [iter(bits)] * 8
grouped = list(zip_longest(*args, fillvalue=0))
for group in grouped:
    print(chr(int("".join(map(str, group)), base=2)), end="")
print()
