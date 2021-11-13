# -*- coding: utf-8 -*-
"""
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo
"""

from PyQt5.QtWidgets import QDialog

from Ui_FigureDisplay import Ui_FigureDisplay
from PIL import Image


# 用于显示图表的窗口（如直方图、FFT结果）
class FigureDisplay(QDialog, Ui_FigureDisplay):
    def __init__(self, parent=None):
        super(FigureDisplay, self).__init__(parent)
        self.setupUi(self)

    def updateFigure(self, histImage: Image.Image):
        windowPadding = 4
        w, h = histImage.size
        self.resize(w + windowPadding * 2, h + windowPadding * 2)
        self.lbl_display.resize(w, h)
        self.lbl_display.setPixmap(histImage.toqpixmap())
