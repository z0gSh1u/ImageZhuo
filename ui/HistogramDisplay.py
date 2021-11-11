# -*- coding: utf-8 -*-
"""
Module implementing HistogramDisplay.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_HistogramDisplay import Ui_HistogramDisplay
from PIL.Image import Image


class HistogramDisplay(QDialog, Ui_HistogramDisplay):
    def __init__(self, parent=None):
        super(HistogramDisplay, self).__init__(parent)
        self.setupUi(self)

    def refresh(self, histImage: Image):
        windowPadding = 12
        w, h = histImage.size
        self.resize(w + windowPadding * 2, h + windowPadding * 2)
        self.lbl_display.resize(w, h)
        self.lbl_display.setPixmap(histImage.toqpixmap())