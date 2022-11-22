
def dither(i, j, image_map, quant_func, size):

    w, h = size
    r, g, b = image_map[i, j]
    qr, qg, qb = quant_func(r), quant_func(g), quant_func(b)
    image_map[i, j] = qr, qg, qb
    quant_error = (
        r - qr,
        g - qg,
        b - qb
    )

    if 0 < i < w - 1 and 0 < j < h - 1:
        r_deltas = calculate_error_deltas(0, i, j, image_map, quant_error)
        g_deltas = calculate_error_deltas(1, i, j, image_map, quant_error)
        b_deltas = calculate_error_deltas(2, i, j, image_map, quant_error)

        left_bottom =   r_deltas[0], g_deltas[0], b_deltas[0]
        middle_bottom = r_deltas[1], g_deltas[1], b_deltas[1]
        right_bottom =  r_deltas[2], g_deltas[2], b_deltas[2]
        right_top =     r_deltas[3], g_deltas[3], b_deltas[3]

        image_map[i - 1, j + 1] = left_bottom
        image_map[i    , j + 1] = middle_bottom
        image_map[i + 1, j + 1] = right_bottom
        image_map[i + 1, j    ] = right_top

    return image_map


def calculate_error_deltas(channel, i, j, image_map, quant_error):
    left_bottom =   round(image_map[i - 1, j + 1][channel] + quant_error[channel] * 3 / 16)
    middle_bottom = round(image_map[i    , j + 1][channel] + quant_error[channel] * 5 / 16)
    right_bottom =  round(image_map[i + 1, j + 1][channel] + quant_error[channel] * 1 / 16)
    right_top =     round(image_map[i + 1, j    ][channel] + quant_error[channel] * 7 / 16)

    return left_bottom, middle_bottom, right_bottom, right_top