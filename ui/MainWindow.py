# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""

import traceback
import sys
import importlib
from PyQt5 import QtCore
import numpy as np

from PyQt5.QtCore import QPoint, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMainWindow, QMessageBox
from PyQt5 import QtWidgets

from Ui_MainWindow import Ui_MainWindow
from OpenDialog import OpenDialog
from WWWLDialog import WWWLDialog
from ImageDisplay import ImageDisplay
from HistogramDisplay import HistogramDisplay
from function.window import windowData

from reader import _BaseReader
from writer import PRESET_WRITERS

from function.hist import drawHistogram
from function.smooth import meanFilter, midFilter
from function.metadata import metaDataAsStr
from function.zoom import zoomIn
from function.otsuSegmentation import OtsuSegmentation

from misc import MyImage, ImageZhuoError
from utils import disableResize


def ensureCurrentOpen():
    if currentImage is None:
        raise ImageZhuoError('当前没有打开的图像，无法进行该操作！')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.buzy = False
        self.toggleBusy(False)
        self.inZoomMode = False

    def toggleBusy(self, to=None):
        if to is None:
            self.buzy = not self.buzy
        else:
            self.buzy = to
        self.lbl_busy.setVisible(self.buzy)

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
        self.toggleBusy()
        histogramDisplay.refresh(drawHistogram(reader.data))
        histogramDisplay.show()
        self.toggleBusy()

    # @ensureCurrentOpen
    @pyqtSlot()
    def on_btn_metadata_clicked(self):
        ensureCurrentOpen()
        QMessageBox().information(self, '图像元信息 / ImageZhuo',
                                  metaDataAsStr(reader, currentImage))

    @pyqtSlot()
    def on_btn_save_clicked(self):
        ensureCurrentOpen()
        self.toggleBusy()
        writerName, ok1 = QInputDialog.getItem(self,
                                               '请选择写入器 / ImageZhuo',
                                               '写入器',
                                               PRESET_WRITERS,
                                               editable=False)
        if ok1:
            writerClazz = importlib.import_module(
                'writer.{}'.format(writerName))
            writerClazz = eval('writerClazz.{}'.format(writerName))
            writer = writerClazz(currentImage)
            savePath, _ = QFileDialog.getSaveFileName(self,
                                                      '请选择保存路径 / ImageZhuo',
                                                      'C:/ImageZhuo_Save.raw')
            if savePath != '':
                writer.save(savePath)
        self.toggleBusy()

    @pyqtSlot()
    def on_btn_retinex_clicked(self):
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_btn_otsu_clicked(self):
        ensureCurrentOpen()
        self.toggleBusy()
        segmentationMask = OtsuSegmentation(currentImage.data, currentImage.h,
                                            currentImage.w)
        currentImage.data = segmentationMask
        currentImage.dtype = str(segmentationMask.dtype)
        imageDisplay.loadByMyImage(currentImage)
        self.toggleBusy()

    @pyqtSlot()
    def on_btn_zoom_clicked(self):
        ensureCurrentOpen()
        # 调整当前是否在放大模式的指示
        self.inZoomMode = not self.inZoomMode
        self.btn_zoom.setText(['放大 [未激活]', '放大 [已激活]'][+self.inZoomMode])
        originFont = QFont(self.btn_zoom.font())
        originFont.setBold(self.inZoomMode)
        self.btn_zoom.setFont(originFont)
        # 允许放大拖拽事件处理
        imageDisplay.toggleDrag(self.inZoomMode)
        # @see handle_ImageDisplay_ZoomParams

    @pyqtSlot()
    def on_btn_mid_clicked(self):
        ensureCurrentOpen()
        ksize = QInputDialog.getInt(self,
                                    '参数询问',
                                    '请输入中值滤波核大小',
                                    3,
                                    min=3,
                                    step=2)[0]
        dstData = midFilter(currentImage.data, currentImage.h, currentImage.w,
                            ksize)
        currentImage.data = dstData
        imageDisplay.loadByMyImage(currentImage)

    @pyqtSlot()
    def on_btn_unsharpmasking_clicked(self):
        ensureCurrentOpen()
        

    @pyqtSlot()
    def on_btn_rotate_clicked(self):
        ensureCurrentOpen()
        item_ = QInputDialog.getItem(self,
                                     '请选择旋转角度 / ImageZhuo',
                                     '旋转角度', ['90°', '180°', '270°'],
                                     editable=False)
        print(item_)

    @pyqtSlot()
    def on_btn_reset_clicked(self):
        ensureCurrentOpen()
        currentImage = MyImage(reader.h, reader.w, reader.data)
        imageDisplay.loadByMyImage(currentImage)

    @pyqtSlot()
    def on_btn_mean_clicked(self):
        ensureCurrentOpen()
        ksize = QInputDialog.getInt(self,
                                    '参数询问',
                                    '请输入均值滤波核大小',
                                    3,
                                    min=3,
                                    step=2)[0]
        dstData = meanFilter(currentImage.data, currentImage.h, currentImage.w,
                             ksize)
        currentImage.data = dstData
        imageDisplay.loadByMyImage(currentImage)


def handle_ImageDisplay_ZoomParams(p0: QPoint, p1: QPoint):
    global mainWindow, currentImage
    if mainWindow.inZoomMode:
        # p0: LeftTop, p1: RightBottom
        zoomedData = zoomIn(currentImage.data, p0, p1)
        currentImage.data = np.array(zoomedData, dtype=currentImage.data.dtype)
        currentImage.reWindow()
        imageDisplay.refresh(currentImage.data8bit)


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
    mainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint
                              | QtCore.Qt.WindowMinimizeButtonHint)
    disableResize(mainWindow)
    mainWindow.show()

    # reader.data始终是打开的文件的原始数据
    reader: _BaseReader = None

    # 随着用户使用各种各样的功能，currentImage，即正在展现的图片，会发生变化
    currentImage = None

    # 打开文件对话框
    openDialog = OpenDialog(mainWindow)
    openDialog._SignalOpenDone.connect(handle_OpenDialog_OpenDone)

    # 窗宽窗位对话框
    wwwlDialog = WWWLDialog(mainWindow)
    wwwlDialog._SignalWWWLDone.connect(handle_WWWLDialog_WWWLDone)

    # 图像显示窗口
    imageDisplay = ImageDisplay()
    imageDisplay._SignalZoomParams.connect(handle_ImageDisplay_ZoomParams)

    # 直方图显示窗口
    histogramDisplay = HistogramDisplay()

    sys.exit(app.exec_())
