# _BaseWriter
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

from misc.classes import MyImage


# 读取器基类
class _BaseWriter():
    def __init__(self, img: MyImage) -> None:
        self.img = img

    def save(self, path: str):
        pass