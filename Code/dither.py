def dither(i, j, image_map, quant_func, info):
    w, h, channels = info

    # quantize and assign
    r, g, b = image_map[i, j][:3]
    qr, qg, qb = quant_func(r), quant_func(g), quant_func(b)
    image_map[i, j] = qr, qg, qb

    # distribute error to neighbors
    '''
        *   7
    3   5   1
    '''
    quant_error = (
        r - qr,
        g - qg,
        b - qb
    )

    neighbors = (
        (-1, 1, 3/16), # left bottom
        ( 0, 1, 5/16), # middle bottom
        ( 1, 1, 1/16), # right bottom
        ( 1, 0, 7/16)  # right top
    )

    for pixel in neighbors:
        adjacent_i, adjacent_j, proportion = i + pixel[0], j + pixel[1], pixel[2]
        if 0 <= adjacent_i < w and 0 <= adjacent_j < h:
            put_pixel_delta(adjacent_i, adjacent_j, proportion, image_map, quant_error)

    return image_map


def put_pixel_delta(i, j, multiplier, image_map, quant_error):

    # calculate and assign new values with error distributed
    delta_r = round(image_map[i, j][0] + quant_error[0] * multiplier)
    delta_g = round(image_map[i, j][1] + quant_error[1] * multiplier)
    delta_b = round(image_map[i, j][2] + quant_error[2] * multiplier)

    image_map[i, j] = delta_r, delta_g, delta_b

