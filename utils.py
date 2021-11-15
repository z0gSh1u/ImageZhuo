# Utilities
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np

from misc import ImageZhuoError


# Convert bytes data to integer.
def bytesToInt(bytes_, littleEndian=True):
    return int.from_bytes(bytes_, 'little' if littleEndian else 'big')


# Convert interger to bytes data.
def intToBytes(int_, byteLength: int, littleEndian=True):
    return int.to_bytes(int(int_), byteLength,
                        'little' if littleEndian else 'big')


# Forbid QT Component resize.
def disableResize(qtComponent, h=None, w=None):
    size = (w, h) if h is not None and w is not None else qtComponent.size()
    qtComponent.setFixedSize(size)


# Clip.
def minmaxClip(v, min_, max_):
    return (max_ if v > max_ else (min_ if v < min_ else v))


# Normalize img to 0~255 uint8.
def normalize255(img):
    res = np.zeros_like(img)
    targetRange = 255
    l = np.min(img)
    r = np.max(img)
    res = (img - l) / (r - l) * targetRange
    return np.array(res, dtype=np.uint8)


# Get min max.
def getMinMax(arr):
    return np.min(arr), np.max(arr)


# Normalize result according to dynamic range of base.
def normalizeToImg(result, base):
    norm = np.zeros_like(result, dtype=float)
    minR, maxR = getMinMax(result)
    min_, max_ = getMinMax(base)
    norm = (result - minR) / (maxR - minR) * (max_ - min_)
    return norm


# 0-1 normalize
def normalize01(arr):
    norm = np.zeros_like(arr, dtype=float)
    min_, max_ = getMinMax(arr)
    norm = (arr - min_) / (max_ - min_)
    return norm


# 断言
def myAssert(cond, hint):
    if not cond:
        raise ImageZhuoError(hint)