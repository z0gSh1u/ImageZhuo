# BaoWriter
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

from misc.utils import intToBytes
from . import _BaseWriter
from misc.classes import MyImage


# 鲍老师RAW格式保存接口
# 0~4B 宽，4~8B 高，后续为每像素2B的数据
# 小端存储，像素有效数据为低12bit
class BaoWriter(_BaseWriter):
    def __init__(self, img: MyImage) -> None:
        super().__init__(img)
        self.img = img

    def save(self, path):
        f = open(path, 'wb')
        # 宽高
        f.write(intToBytes(self.img.w, 4, 'little'))
        f.write(intToBytes(self.img.h, 4, 'little'))
        # 图像数据
        for r in range(self.img.h):
            for c in range(self.img.w):
                f.write(intToBytes(self.img.data[r, c], 2, 'little'))
        f.close()
