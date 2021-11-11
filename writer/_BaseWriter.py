# _BaseWriter
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np
from misc import MyImage


# 读取器基类
class _BaseWriter():
    def __init__(self, img: MyImage) -> None:
        self.img = img

    def save(self, path: str):
        pass