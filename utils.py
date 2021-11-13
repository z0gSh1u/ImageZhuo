# Utilities
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np


# Convert bytes data to integer.
def bytesToInt(bytes_, littleEndian=True):
    return int.from_bytes(bytes_, 'little' if littleEndian else 'big')


# Convert interger to bytes data.
def intToBytes(int_, byteLength: int, littleEndian=True):
    return int.to_bytes(int(int_), byteLength,
                        'little' if littleEndian else 'big')


# Forbid QT Component resize.
def disableResize(qtComponent):
    qtComponent.setFixedSize(qtComponent.size())


# Clip.
def minmaxClip(v, min_, max_):
    return (max_ if v > max_ else (min_ if v < min_ else v))


# Normalize img to 0~255 uint8.
def normalize255(img):
    res = np.zeros_like(img, dtype=np.uint8)
    targetRange = 255
    l = np.min(img)
    r = np.max(img)
    res = (res - l) / (r - l) * targetRange
    return res