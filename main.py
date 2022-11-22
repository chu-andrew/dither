from PIL import Image
from tqdm import tqdm
from dither_v2 import dither

dir = "test_images/"
filename = "jeju_small.jpg"
input_image = Image.open(dir + filename)
width, height = input_image.size

quantized_image = input_image.copy()
dithered_image = input_image.copy()

quantized_map = quantized_image.load()
dithered_map = dithered_image.load()

BITS = 1
GRAYSCALE = False
if GRAYSCALE:
    # grayscale = lambda r, g, b: int(0.299 * r + 0.587 * g + 0.114 * b)
    for j in range(height):
        for i in range(width):
            r, g, b = input_image.getpixel((i, j))
            grayscale = int(0.299 * r + 0.587 * g + 0.114 * b)
            quantized_map[i, j] = grayscale, grayscale, grayscale
            dithered_map[i, j] = grayscale, grayscale, grayscale

for j in tqdm(range(height)):
    for i in range(width):

        levels = (1 << BITS) - 1
        def quantize(x):  return round(round(x / 255 * levels) / levels * 255)
        if quantized_map[i, j] is not None:
            r, g, b = quantized_map[i, j]
            quantized_map[i, j] = quantize(r), quantize(g), quantize(b)

        dithered_map = dither(i, j, dithered_map, quantize, (width, height))

import numpy as np
Image.fromarray(np.hstack((np.array(input_image), np.array(quantized_image), np.array(dithered_image)))).show()

qc = quantized_image.getcolors()
dc = dithered_image.getcolors()
print(len(qc), qc)
print(len(dc), dc)

name = filename.split('.')[0]
dir = dir + "output_images/"
quantized_image.save(dir + name + "_quantized.png")
dithered_image.save(dir + name + "_dithered.png")
