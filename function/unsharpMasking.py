# Unsharp Masking
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np

from .smooth import meanFilter
from misc.utils import normalizeToImg


# 使用均值滤波的高提升滤波
def unsharpMaskingMeanFilter(I_: np.ndarray, ksize: int, k: float):
    assert k >= 1
    I = np.array(I_, dtype=float)
    blur = meanFilter(I, ksize)
    mask = I - blur
    res = I + k * mask
    res = normalizeToImg(res, I)
    return np.array(res, dtype=I_.dtype)
