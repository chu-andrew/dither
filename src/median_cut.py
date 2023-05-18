import numpy as np


def palette(img, cuts):
    # TODO test if img is large enough to split
    img = np.array(img)
    img = img[:, :, 0:3]  # remove other channels
    img = np.reshape(img, (-1, 3))  # combine rows * columns (3d to 2d)
    img = np.array([img])  # add wrapping dimension: img --> [img], outside brackets necessary for internal splitting

    # split pixels into bins
    bins = median_cut(img, cuts)

    palette = []
    for bin in bins:
        # take average pixel of bin and return as tuple
        rgb = np.median(np.array(bin).T, axis=1)
        rgb = tuple(round(pixel) for pixel in rgb.tolist())
        palette.append(rgb)

    # print(palette)
    return palette


def median_cut(img, cuts):
    splits = img.tolist()
    for i in range(cuts):
        temp = []
        for index in range(len(splits)):
            sub = np.array(splits[index])  # convert list to np for faster operations
            channels = sub.transpose()
            target_channel, median = get_img_info(channels)

            # https://stackoverflow.com/questions/7662458/how-to-split-an-array-according-to-a-condition-in-numpy
            condition = (channels[target_channel] < median)
            cut_a, cut_b = sub[condition], sub[~condition]

            temp += [cut_a.tolist(), cut_b.tolist()]

        splits = temp

    return splits


def get_img_info(channels):
    target_channel = np.ptp(channels, axis=1).argmax()  # get channel with greatest range
    median = np.median(channels[target_channel], 0)

    return target_channel, median
