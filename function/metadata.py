# Metadata
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

from misc.classes import MyImage
from reader import _BaseReader
import numpy as np

from misc.utils import getMinMax


def metaDataAsStr(reader: _BaseReader, img: MyImage):
    meanValue = np.mean(img.data)
    varValue = np.var(img.data)
    min_, max_ = getMinMax(img.data)

    return "文件名：{}\n高：{}\n宽：{}\n像素格式：{}\n窗宽：{}\n窗位：{}\n像素最大值：{}\n像素最小值：{}\n像素均值：{:.2f}\n像素方差：{:.2f}".format(
        *(reader.filename, img.h, img.w, img.dtype, img.ww, img.wl, min_, max_,
          meanValue, varValue))
