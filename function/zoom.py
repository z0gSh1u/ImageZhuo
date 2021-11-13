# Zoom
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

# 《数字图像处理基础》（鲍旭东）课程实验 1 - 图像的旋转和缩放
# 212138-卓旭
# 注：本部分代码修改自本人本科的《数字图像处理》（鲍旭东）课程实验代码，学号09017227

from PyQt5.QtCore import QPoint
import numpy as np
import math

# 双线性插值
def bilinearInterp(img, r_, c_):
    r1 = math.floor(r_)
    c1 = math.floor(c_)
    r2, c2 = r1, c1 + 1
    r3, c3 = r1 + 1, c1
    r4, c4 = r1 + 1, c1 + 1
    u, v = r_ - r1, c_ - c1  # 取小数部分
    p = (1 - u) * (1 - v) * img[r1, c1] + \
        (1 - u) * v * img[r2, c2] + \
        u * (1 - v) * img[r3, c3] + \
        u * v * img[r4, c4]
    return p


# 放大
# p0: 左上角点，p1: 右下角点。目标尺寸大小与img相同。
def zoomIn(img: np.ndarray, p0: QPoint, p1: QPoint, by50Percent: bool):
    h, w = img.shape
    res = np.zeros((h, w), dtype=float)

    # 长宽支持不同的放大比例
    ratio = [h / (p1.y() - p0.y()), w / (p1.x() - p0.x())]
    r_lefttop, c_lefttop = p0.y(), p0.x()

    # 当图像以50%尺寸显示时，真实的画框长宽是操作的两倍，放大比率是操作的一半
    if by50Percent:
        ratio = list(map(lambda x: x / 2, ratio))
        r_lefttop *= 2
        c_lefttop *= 2

    # 循环目标图像
    for r in range(h):
        for c in range(w):
            # 目标图像中1像素的步进，在原图像中相当于 1/ratio 像素的步进，据此算出原图像四个插值数据点的坐标
            r_, c_ = r / ratio[0] + r_lefttop, c / ratio[1] + c_lefttop
            res[r, c] = bilinearInterp(img, r_, c_)

    return np.array(res, dtype=img.dtype)
