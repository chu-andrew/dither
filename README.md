# dither

_dither_ uses the Floyd-Steinberg dithering algorithm to process images, with either uniform quantization or median-cut
quantization.

This program provides a command-line interface to dither images:

```commandline
python main.py [OPTIONS] IMAGE_FILE [TONES]
```

Options:

    --uniform [default]
    --median_cut
    --gray [convert image to grayscale before processing]
    --help

| Original Image                          | Grayscaled Image                             |
|-----------------------------------------|----------------------------------------------|
| ![image](/Data/test_images/subway.jpg/) | ![image](/Data/test_images/subway_gray.png/) |

| Grayscale Uniform Quantized 2-tone                                   | Grayscale Uniform Quantized 2-tone Dithered                         |
|----------------------------------------------------------------------|---------------------------------------------------------------------|
| ![image](/Data/test_images/subway_gray_2tone_uniform_quantized.png/) | ![image](/Data/test_images/subway_gray_2tone_uniform_dithered.png/) |

| Uniform Quantized 8-tone                                        | Uniform Quantized 8-tone Dithered                                |
|-----------------------------------------------------------------|------------------------------------------------------------------|
| ![image](/Data/test_images/subway_8tone_uniform_quantized.png/) | ![image](/Data/test_images/subway_8tone_uniform_dithered.png/)   |

| Median-Cut Quantized 8-tone                                        | Median-Cut Quantized 8-tone Dithered                              |
|--------------------------------------------------------------------|-------------------------------------------------------------------|
| ![image](/Data/test_images/subway_8tone_median_cut_quantized.png/) | ![image](/Data/test_images/subway_8tone_median_cut_dithered.png/) |

PIP Requirements:

- Pillow
- numpy
- click
- tqdm