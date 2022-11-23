from math import log

from PIL import Image
from tqdm import tqdm
import click

from dither import dither


@click.command()
@click.argument('image_file',
                type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument('bits', default=1)
@click.option('--uniform', 'quantize_method', flag_value='uniform',
              default=True)
@click.option('--median_cut', 'quantize_method', flag_value='median_cut')
@click.option('--gray', is_flag=True, default=False, help='convert image to grayscale before processing')
def main(image_file, bits, quantize_method, gray):
    # choose quantization method
    quantize = choose_quantization_method(quantize_method, bits)

    # initialize images and maps
    input_image = Image.open(image_file)
    width, height = input_image.size

    quantized_image = input_image.copy()
    dithered_image = input_image.copy()

    quantized_map = quantized_image.load()
    dithered_map = dithered_image.load()

    if gray: quantized_map, dithered_map = grayscale_image(input_image, quantized_map, dithered_map)

    # process images: Floyd-Steinberg dithering
    for j in tqdm(range(height)):
        for i in range(width):
            # populate a quantized map
            if quantized_map[i, j] is not None:
                r, g, b = quantized_map[i, j]
                quantized_map[i, j] = quantize(r), quantize(g), quantize(b)

            # populate a dithered map
            dithered_map = dither(i, j, dithered_map, quantize, (width, height))

    # save images and output stats
    ext = "." + image_file.split('.')[-1]
    stem = str(image_file.replace(ext, ""))
    new_file = f"{stem}_" \
               f"{bits}bit_" \
               f"{'gray_' if gray else ''}"

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


def grayscale_image(input_image, quantized_map, dithered_map):
    width, height = input_image.size
    for j in range(height):
        for i in range(width):
            r, g, b = input_image.getpixel((i, j))
            grayscale = int(0.299 * r + 0.587 * g + 0.114 * b)

            gray_pixel = grayscale, grayscale, grayscale
            quantized_map[i, j] = gray_pixel
            dithered_map[i, j] = gray_pixel

    return quantized_map, dithered_map


def choose_quantization_method(quantize_method,bits):
    # https://web.cs.wpi.edu/~matt/courses/cs563/talks/color_quant/CQindex.html
    match quantize_method:
        case "uniform":
            bits_per_channel = log(bits) / (3 * log(2))
            if bits_per_channel != int(round(bits_per_channel)) or bits_per_channel < 1:
                print()  # TODO error message for incorrect bits option
                return False
            else:
                bits_per_channel = int(round(bits_per_channel))
            levels = (1 << bits_per_channel) - 1

            # bits = (2 ** bits_per_channel) ** 3

            return lambda x: round(round(x / 255 * levels) / levels * 255)
        case "median_cut":
            raise NotImplementedError


if __name__ == '__main__':
    main()
