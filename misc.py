# misc
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np


class ImageZhuoError(RuntimeError):
    def __init__(self, payload: str) -> None:
        super().__init__()
        self.payload = payload


class MyImage():
    def __init__(self, h, w, data) -> None:
        self.h = h
        self.w = w
        self.data: np.ndarray = data

        # metadata
        max_ = np.max(data)
        min_ = np.min(data)
        self.ww = max_ - min_
        self.wl = self.ww // 2
        self.dtype = str(self.data.dtype)
