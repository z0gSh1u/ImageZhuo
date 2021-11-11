# Window
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np


# 使用WW/WL限定data的窗宽窗位，然后拉伸到minGray~maxGray
def windowData(data: np.ndarray, ww: int, wl: int, minGray: int, maxGray: int):
    res = data.copy()
    l = wl - ww // 2
    r = wl + ww // 2
    res[res > r] = r
    res[res < l] = l
    targetRange = (maxGray - minGray)
    res = (res - l) / (r - l) * targetRange + minGray
    return res
