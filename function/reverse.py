# Reverse
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np

# 图片反相
def reverse(img: np.ndarray):
    h, w = img.shape
    max_ = np.max(img)
    min_ = np.min(img)
    res = np.zeros_like(img, dtype=img.dtype)
    for r in range(h):
        for c in range(w):
            res[r, c] = max_ - (img[r, c] - min_)

    return res