# misc
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

from PIL import Image
import numpy as np
from function.window import windowData
from utils import getMinMax


# 自定义异常类
class ImageZhuoError(RuntimeError):
    def __init__(self, payload: str) -> None:
        super().__init__()
        self.payload = payload


# 图像包装类
class MyImage():
    def __init__(self, h, w, data) -> None:
        self.h = h  # 高
        self.w = w  # 宽
        self.data: np.ndarray = data  # 原始数据

        min_, max_ = getMinMax(self.data)
        self.ww = max_ - min_  # 窗宽，默认为max_-min_
        self.wl = self.ww // 2  # 窗位，默认为ww/2
        self.dtype = str(self.data.dtype)  # 原始数据的数据类型

        self.data8bit: np.ndarray = None  # 加窗后的256级灰度图
        self.PILImg8bit: Image.Image = None  # PIL.Image格式的加窗后灰度图
        self.reGen8bit()

    # 重新生成256级灰度
    def reGen8bit(self):
        data = windowData(
            self.data, self.ww,
            self.wl) if self.data.dtype == np.uint16 else self.data
        self.data8bit = np.array(data, dtype=np.uint8)
        self.PILImg8bit = Image.fromarray(self.data8bit)

    # 重置为默认窗宽窗位
    def defaultWWWL(self):
        min_, max_ = getMinMax(self.data)
        self.ww = max_ - min_  # 窗宽，默认为max_-min_
        self.wl = self.ww // 2  # 窗位，默认为ww/2