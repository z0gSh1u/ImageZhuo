# BaoReader
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

from . import _BaseReader
from utils import bytesToInt
import numpy as np
import os


# 鲍老师RAW格式读取接口
# 0~4B 宽，4~8B 高，后续为每像素2B的数据
# 小端存储，像素有效数据为低12bit
class BaoReader(_BaseReader):
    def __init__(self, rawPath: str) -> None:
        super().__init__()

        self.path = rawPath
        self.filename = os.path.basename(self.path)

        f = open(rawPath, 'rb')
        self.w = np.uint32(bytesToInt(f.read(4)))
        self.h = np.uint32(bytesToInt(f.read(4)))
        self.data = []

        while True:
            pixel = f.read(2)
            if pixel == b'':
                break
            pixel = np.uint16(bytesToInt(pixel))
            # 抹去高4bit的杂数据
            pixel = pixel & 0x0fff
            self.data.append(pixel)

        self.data = np.array(self.data, dtype=np.uint16).reshape(
            (self.h, self.w))
        f.close()
