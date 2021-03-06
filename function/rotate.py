# Rotate
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

# 《数字图像处理基础》（鲍旭东）课程实验 1 - 图像的旋转和缩放
# 212138-卓旭

import numpy as np
import math
from .zoom import bilinearInterp


def rotate(img: np.ndarray, deg: int):
    h, w = img.shape
    res = np.zeros((h, w), dtype=float)
    rad = deg * math.pi / 180.
    # 遍历目标图像
    for c in range(w):
        for r in range(h):
            # 计算对应的原图像坐标
            r_ = (-h / 2 + r) * math.cos(rad) + (w / 2 -
                                                 c) * math.sin(rad) + h / 2
            c_ = (-h / 2 + r) * math.sin(rad) + (-w / 2 +
                                                 c) * math.cos(rad) + w / 2
            # 双线性插值
            r1 = math.floor(r_)
            c1 = math.floor(c_)
            # 避免 +1 越界
            if c1 >= 0 and r1 >= 0 and c1 < w - 1 and r1 < h - 1:
                res[r, c] = bilinearInterp(img, r_, c_)

    return np.array(res, dtype=img.dtype)
