# Smooth
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np


def smoothFilter(data: np.ndarray, filterSize: int, replacer) -> np.ndarray:
    h, w = data.shape
    # 周围一圈保留处理
    padding = (filterSize - 1) // 2

    # 获取某像素的邻域及其自身
    def getNeighborAndMe(x, y, padding):
        res = []
        for i in range(-padding, padding + 1):
            for j in range(-padding, padding + 1):
                res.append(data[x + i, y + j])
        return res

    result = np.array(data)
    for i in range(h):
        for j in range(w):
            # 边界保留
            if i < padding or j < padding or i > h - padding - 1 or j > w - padding - 1:
                continue
            result[i, j] = replacer(getNeighborAndMe(i, j, padding))
    return np.array(result, dtype=data.dtype)


# 均值滤波
def meanFilter(data, filterSize: int):
    return smoothFilter(data, filterSize, lambda x: sum(x) / len(x))


# 中值滤波
def midFilter(data, filterSize: int):
    return smoothFilter(data, filterSize,
                        lambda x: sorted(x)[(len(x) + 1) // 2 - 1])
