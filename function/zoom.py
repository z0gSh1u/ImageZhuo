# 《数字图像处理基础》课程实验 1 - 图像的旋转和缩放
# 212138-卓旭

from PIL import Image
import numpy as np
import math

ROTATE_DEG = 45  # 顺时针旋转角度
ZOOM_IN_RATIO = 3  # 放大倍率
source = np.array(Image.open('barbara.bmp'), dtype=np.uint8)


def biliear_interp(img, r_, c_):
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


# 注：本部分代码修改自本人本科的《数字图像处理》课程实验3代码，学号09017227
def zoom_in(img, ratio):
    h, w = img.shape
    res = np.zeros((h, w), dtype=float)

    # 利用放大倍率计算目标图像在原图像的对应视区，返回四元组 (左上角x坐标, 左上角y坐标, 宽度, 高度)
    def get_viewport():
        r_center, c_center = h / 2, w / 2
        r_new, c_new = h / ratio, w / ratio
        r_lefttop, c_lefttop = r_center - r_new / 2, c_center - c_new / 2
        return (r_lefttop, c_lefttop, r_new, c_new)

    # 循环目标图像
    for c in range(w):
        for r in range(h):
            r_lefttop, c_lefttop, _, _ = get_viewport()
            # 目标图像中1像素的步进，在原图像中相当于 1/ratio 像素的步进，据此算出原图像四个插值数据点的坐标
            r_, c_ = r / ratio + r_lefttop, c / ratio + c_lefttop
            res[r, c] = biliear_interp(img, r_, c_)

    return res
