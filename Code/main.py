import numpy as np
from PIL import Image
from math import log, sqrt
from tqdm import tqdm
import click

from dither import dither
from median_cut import palette


@click.command()
@click.argument('image_file', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument('tones', default=1)
@click.option('--uniform', 'quantize_method', flag_value='uniform', default=True)
@click.option('--median_cut', 'quantize_method', flag_value='median_cut')
@click.option('--gray', is_flag=True, default=False, help='convert image to grayscale before processing')
def main(image_file, tones, quantize_method, gray):
    # initialize images and maps
    input_image = Image.open(image_file)
    width, height = input_image.size
    channels = len(input_image.getbands())

    if gray:
        input_image = Image.open(grayscale_image(input_image, image_file))

    quantized_image = input_image.copy()
    dithered_image = input_image.copy()

    quantized_map = quantized_image.load()
    dithered_map = dithered_image.load()

    # choose quantization method
    try:
        quantize = choose_quantization_method(quantize_method, tones, input_image, gray)
    except ValueError:
        print("Please enter a valid number of tones.")
        return

    # process images: Floyd-Steinberg dithering
    for j in tqdm(range(height)):
        for i in range(width):

            if quantized_map[i, j] is not None:
                r, g, b = quantized_map[i, j][:3]
                qr, qg, qb = quantize(r, g, b)
                quantized_map[i, j] = qr, qg, qb

            # populate dithered map
            dithered_map = dither(i, j, dithered_map, quantize, (width, height, channels))

    # save images and output stats
    # https://stackoverflow.com/questions/73242236/image-colors-changed-after-saving-with-pil
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    stem = get_path(image_file)
    new_file =  f"{stem}_" \
                f"{'gray_' if gray else ''}" \
                f"{tones}tone_" \
                f"{quantize_method}_"  \

    quantized_image.save(new_file + "quantized.png")
    dithered_image.save(new_file + "dithered.png")

    print(f'''
original image:     {len(input_image.getcolors(width * height))} colors
quantized image:    {len(quantized_image.getcolors(width * height))} colors
dithered image:     {len(dithered_image.getcolors(width * height))} colors

output:
{new_file}quantized.png
{new_file}dithered.png
    ''')
    return True


def choose_quantization_method(quantize_method, tones, img, gray):
    # https://web.cs.wpi.edu/~matt/courses/cs563/talks/color_quant/CQindex.html

    bits = log(tones, 2)
    if bits != int(bits) or bits < 1:
        raise ValueError
    else:
        bits = int(bits)

    match quantize_method:
        case "uniform":
            # set number of levels per r/g/b
            if gray:    levels = tones - 1  # accounting for 0 condition
            else:       levels = bits / 3
            if levels < 1: raise ValueError

            def quantize_uniform(r, g, b):
                return (
                    round(round(r / 255 * levels) / levels * 255),
                    round(round(g / 255 * levels) / levels * 255),
                    round(round(b / 255 * levels) / levels * 255)
                )

            return quantize_uniform

        case "median_cut":
            # bits become the number of cuts
            colors = palette(img, bits)

            def quantize_median_cut(r, g, b):
                distances = []
                for R, G, B in colors:
                    distance = sqrt((R - r)**2 + (G - g)**2 + (B - b)**2)
                    distances.append(distance)
                return colors[distances.index(min(distances))]

            return quantize_median_cut


def grayscale_image(input_image, image_file):
    width, height = input_image.size

    gray_image = input_image.copy()
    gray_map = gray_image.load()

    for j in range(height):
        for i in range(width):
            r, g, b = input_image.getpixel((i, j))[:3]
            grayscale = int(0.299 * r + 0.587 * g + 0.114 * b)

            gray_map[i, j] = grayscale, grayscale, grayscale

    new_filename = get_path(image_file) + "_gray.png"
    gray_image.save(get_path(image_file) + "_gray.png")

    return new_filename


def get_path(filename):
    ext = "." + filename.split('.')[-1]
    stem = str(filename.replace(ext, ""))
    return stem


if __name__ == '__main__':
    main()
