# Flipping
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np


def horizontalFlip(img: np.ndarray):
    h, w = img.shape
    res = np.zeros_like(img, dtype=img.dtype)
    for r in range(h):
        for c in range(w):
            res[r, c] = img[r, w - c - 1]
    return res