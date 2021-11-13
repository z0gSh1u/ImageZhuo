# Sharpen
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np

from utils import normalizeToImg

LAPLACIAN_KERNEL = [
    [],
    [0, -1, 0, -1, 4, -1, 0, -1, 0],  # 一阶拉普拉斯算子
    [-1, -1, -1, -1, 8, -1, -1, -1, -1]  # 二阶拉普拉斯算子
]


# 拉普拉斯锐化
def laplacian(img: np.ndarray, kOrder: int):
    assert kOrder == 1 or kOrder == 2
    kernel = LAPLACIAN_KERNEL[kOrder]
    ksize = 3
    padding = (ksize - 1) // 2
    h, w = img.shape

    # 获取某像素的邻域及其自身（自上而下，从左向右扫描）
    def getNeighborAndMe(x, y, padding):
        res = []
        for i in range(-padding, padding + 1):
            for j in range(-padding, padding + 1):
                res.append(img[x + i, y + j])
        return res

    def _laplacian(neighbor):
        assert len(neighbor) == ksize * ksize
        res = 0
        for i in range(len(neighbor)):
            res += kernel[i] * neighbor[i]
        return res

    result = np.zeros_like(img, dtype=float)
    for i in range(h):
        for j in range(w):
            # 边界保留
            if i < padding or j < padding or i > h - padding - 1 or j > w - padding - 1:
                continue
            result[i, j] = _laplacian(getNeighborAndMe(i, j, padding))

    result = result + img
    result = normalizeToImg(result, img)

    return np.array(result, dtype=img.dtype)
