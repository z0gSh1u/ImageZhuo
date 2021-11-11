# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets

from Ui_MainWindow import Ui_MainWindow
from OpenDialog import OpenDialog
from WWWLDialog import WWWLDialog

from ImageDisplay import ImageDisplay
from HistogramDisplay import HistogramDisplay
from function.window import windowData

import numpy as np

from utils import disableResize
from function.hist import drawHistogram
from reader import _BaseReader


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_open_clicked(self):
        openDialog.show()

    @pyqtSlot()
    def on_btn_wwwl_clicked(self):
        wwwlDialog.show()
        print(reader)

    @pyqtSlot()
    def on_btn_hist_clicked(self):
        histogramDisplay.refresh(drawHistogram(reader.data))
        histogramDisplay.show()


def handle_OpenDialog_OpenDone(reader_):
    # 接管reader，并显示图片
    global reader
    reader = reader_
    imageDisplay.loadByReader(reader)
    disableResize(imageDisplay)
    openDialog.setVisible(False)
    imageDisplay.show()


def handle_WWWLDialog_WWWLDone(ww, wl):
    # 调整窗宽窗位
    srcData = imageDisplay.reader.data
    srcData = windowData(srcData, ww, wl, 0, 255)
    imageDisplay.refresh(np.array(srcData, dtype=np.uint8))
    # wwwlDialog.setVisible(False)

def checkCurrentOpen():
    pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    # reader.data始终是打开的文件的原始数据
    reader: _BaseReader = None

    # 随着用户使用各种各样的功能，currentImage，即正在展现的图片，会发生变化
    currentImageWidth: int = None
    currentImageHeight: int = None
    currentImageData: np.ndarray = None

    openDialog = OpenDialog(mainWindow)
    openDialog._SignalOpenDone.connect(handle_OpenDialog_OpenDone)

    wwwlDialog = WWWLDialog(mainWindow)
    wwwlDialog._SignalWWWLDone.connect(handle_WWWLDialog_WWWLDone)

    imageDisplay = ImageDisplay()

    histogramDisplay = HistogramDisplay()

    sys.exit(app.exec_())
