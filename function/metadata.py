# Metadata
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

from misc import MyImage
from reader import _BaseReader
import numpy as np


def metaDataAsStr(reader: _BaseReader, img: MyImage):
    meanValue = np.mean(img.data)
    varValue = np.var(img.data)

    return "文件名：{}\n高：{}\n宽：{}\n像素格式：{}\n窗宽：{}\n窗位：{}\n像素均值：{:.2f}\n像素方差：{:.2f}".format(
        *(reader.filename, img.h, img.w, img.dtype, img.ww, img.wl, meanValue,
          varValue))
