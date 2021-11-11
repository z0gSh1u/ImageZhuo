# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox
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
from misc import MyImage, ImageZhuoError

from function.metadata import metaDataAsStr
import traceback
import sys

from writer import PRESET_WRITERS

from function.smooth import meanFilter, midFilter

# 要求当前必须有打开的图像才能进行操作
# def ensureCurrentOpen(func):
#     def wrapper(*args, **kwargs):
#         if currentImage is not None:
#             func(*args, **kwargs)
#         else:
#             raise ImageZhuoError('当前没有打开的图像，无法进行该操作！')

#     return wrapper


def ensureCurrentOpen():
    if currentImage is None:
        raise ImageZhuoError('当前没有打开的图像，无法进行该操作！')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_open_clicked(self):
        openDialog.show()

    @pyqtSlot()
    def on_btn_wwwl_clicked(self):
        ensureCurrentOpen()
        wwwlDialog.updateWWWLValue(currentImage.ww, currentImage.wl)
        wwwlDialog.show()

    @pyqtSlot()
    def on_btn_hist_clicked(self):
        ensureCurrentOpen()
        histogramDisplay.refresh(drawHistogram(reader.data))
        histogramDisplay.show()

    # @ensureCurrentOpen
    @pyqtSlot()
    def on_btn_metadata_clicked(self):
        ensureCurrentOpen()
        QMessageBox().information(self, '图像元信息 / ImageZhuo',
                                  metaDataAsStr(reader, currentImage))

    @pyqtSlot()
    def on_btn_save_clicked(self):
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_btn_retinex_clicked(self):
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_btn_otsu_clicked(self):
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_btn_zoom_clicked(self):
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_btn_mid_clicked(self):
        dstData = midFilter(currentImage.data, currentImage.h, currentImage.w,
                            5)
        currentImage.data = dstData
        imageDisplay.loadByMyImage(currentImage)

    @pyqtSlot()
    def on_btn_unsharpmasking_clicked(self):
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_btn_rotate_clicked(self):
        # TODO: not implemented yet
        raise NotImplementedError


def handle_OpenDialog_OpenDone(reader_):
    # 接管reader，并显示图片
    global reader, currentImage
    reader = reader_
    currentImage = MyImage(reader.h, reader.w, reader.data)
    imageDisplay.loadByMyImage(currentImage)
    disableResize(imageDisplay)
    openDialog.setVisible(False)
    imageDisplay.show()


def handle_WWWLDialog_WWWLDone(ww, wl):
    # 调整窗宽窗位
    windowedData = windowData(currentImage.data, ww, wl, 0, 255)
    imageDisplay.refresh(np.array(windowedData, dtype=np.uint8))
    # wwwlDialog.setVisible(False)


def customizedExceptHook(exceptionType, exceptionValue, exceptionTraceback):
    traceBackText = "".join(
        traceback.format_exception(exceptionType, exceptionValue,
                                   exceptionTraceback))
    if exceptionType == ImageZhuoError:
        QMessageBox.critical(mainWindow, '错误提示 / ImageZhuo',
                             exceptionValue.payload + '\n\n' + traceBackText,
                             QMessageBox.Yes, QMessageBox.Yes)
    else:
        QMessageBox.critical(mainWindow, '未知错误提示 / ImageZhuo', traceBackText,
                             QMessageBox.Yes, QMessageBox.Yes)
        print("[Unknown Error]\n", traceBackText)
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    sys.excepthook = customizedExceptHook

    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    # reader.data始终是打开的文件的原始数据
    reader: _BaseReader = None

    # 随着用户使用各种各样的功能，currentImage，即正在展现的图片，会发生变化
    currentImage = None

    openDialog = OpenDialog(mainWindow)
    openDialog._SignalOpenDone.connect(handle_OpenDialog_OpenDone)

    wwwlDialog = WWWLDialog(mainWindow)
    wwwlDialog._SignalWWWLDone.connect(handle_WWWLDialog_WWWLDone)

    imageDisplay = ImageDisplay()

    histogramDisplay = HistogramDisplay()

    sys.exit(app.exec_())

    # elsewise throw
