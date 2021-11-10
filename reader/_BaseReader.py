# _BaseReader
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np


# 读取器基类
class _BaseReader():
    def __init__(self) -> None:
        self.h: int = None
        self.w: int = None
        self.data: np.ndarray = None
