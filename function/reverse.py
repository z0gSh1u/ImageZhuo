# Reverse
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np

from misc.utils import getMinMax


# 图片反相
def reverse(img: np.ndarray):
    h, w = img.shape
    min_, max_ = getMinMax(img)
    res = np.zeros_like(img, dtype=img.dtype)
    for r in range(h):
        for c in range(w):
            res[r, c] = max_ - (img[r, c] - min_)

    return res