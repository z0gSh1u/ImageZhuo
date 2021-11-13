# BaoWriter
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

from utils import intToBytes
from . import _BaseWriter
from misc import MyImage


# 鲍老师RAW格式保存接口
# 0~4B 宽，4~8B 高，后续为每像素2B的数据
# 小端存储，像素有效数据为低12bit
class BaoWriter(_BaseWriter):
    def __init__(self, img: MyImage) -> None:
        super().__init__(img)
        self.img = img

    def save(self, path):
        dstBytes = b''
        # 宽高
        dstBytes += intToBytes(self.img.w, 4, 'little')
        dstBytes += intToBytes(self.img.h, 4, 'little')
        # 图像数据
        for pixel in self.img.data.ravel():
            dstBytes += intToBytes(pixel, 2, 'little')
        assert len(dstBytes) == 4 + 4 + 2 * int(self.img.h * self.img.w)
        with open(path, 'wb') as f:
            f.write(dstBytes)
