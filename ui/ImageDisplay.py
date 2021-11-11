# -*- coding: utf-8 -*-
"""
Module implementing ImageDisplay.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_ImageDisplay import Ui_Dialog

from reader import _BaseReader
import numpy as np
from PIL import Image

from utils import disableResize

from function.window import windowData


class ImageDisplay(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(ImageDisplay, self).__init__(parent)
        self.setupUi(self)
        self.reader = None

        self.setWindowTitle(self.windowTitle() + ' (50 %)')

    def loadByReader(self, reader: _BaseReader):
        self.reader = reader

        data256 = reader.data
        min_ = np.min(data256)
        max_ = np.max(data256)
        data256 = (data256 - min_) / (max_ - min_) * 255
        data256 = np.array(data256, dtype=np.uint8)

        image256 = Image.fromarray(data256)

        # wh
        tsize = list(map(lambda x: x // 2, image256.size))
        twsize = list(map(lambda x: x + 4, tsize))
        image256 = image256.resize(tuple(tsize), Image.BICUBIC)

        self.resize(*twsize)
        # disableResize(self)

        self.lbl_display.resize(*tsize)
        # disableResize(self.lbl_display)

        self.lbl_display.setPixmap(image256.toqpixmap())

    def refresh(self, data8bit):
        image256 = Image.fromarray(data8bit)
        tsize = list(map(lambda x: x // 2, image256.size))
        twsize = list(map(lambda x: x + 4, tsize))
        image256 = image256.resize(tuple(tsize), Image.BICUBIC)
        self.resize(*twsize)
        self.lbl_display.setPixmap(image256.toqpixmap())
