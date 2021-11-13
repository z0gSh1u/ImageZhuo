# -*- coding: utf-8 -*-
"""
Module implementing ImageDisplay.
"""

from PyQt5.QtCore import QPoint, QRect, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QDialog

from Ui_ImageDisplay import Ui_Dialog

from misc import MyImage
import numpy as np
from PIL import Image

from utils import disableResize


class ImageDisplay(QDialog, Ui_Dialog):

    _SignalZoomParams = pyqtSignal(QPoint, QPoint)

    def __init__(self, parent=None):
        super(ImageDisplay, self).__init__(parent)
        self.setupUi(self)
        self.img = None

        self.setWindowTitle(self.windowTitle() + ' (50 %)')

        self.lbl_display._SignalZoomDragDone.connect(
            self.handle_ImageDisplayWidget_ZoomDragDone)

    def handle_ImageDisplayWidget_ZoomDragDone(self, p0, p1):
        self._SignalZoomParams.emit(p0, p1)

    def toggleDrag(self, to: bool):
        self.lbl_display.enableDrag = to

    def loadByMyImage(self, img: MyImage):
        self.img = img
        self.lbl_display.aspect = self.img.h / self.img.w

        img256 = img.PILImg8bit

        # wh
        tsize = list(map(lambda x: x // 2, img256.size))
        twsize = list(map(lambda x: x + 4, tsize))
        img256 = img256.resize(tuple(tsize), Image.BICUBIC)

        self.resize(*twsize)
        self.lbl_display.resize(*tsize)
        self.lbl_display.setPixmap(img256.toqpixmap())

    def refresh(self, data8bit):
        image256 = Image.fromarray(data8bit)
        tsize = list(map(lambda x: x // 2, image256.size))
        twsize = list(map(lambda x: x + 4, tsize))
        image256 = image256.resize(tuple(tsize), Image.BICUBIC)
        self.resize(*twsize)
        self.lbl_display.setPixmap(image256.toqpixmap())
