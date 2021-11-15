# -*- coding: utf-8 -*-
"""
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo
"""

import traceback
import sys
import importlib
from PyQt5 import QtCore
import numpy as np
from PIL import Image

from PyQt5.QtCore import QPoint, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMainWindow, QMessageBox
from PyQt5 import QtWidgets

from Ui_MainWindow import Ui_MainWindow
from OpenDialog import OpenDialog
from WWWLDialog import WWWLDialog
from ImageDisplay import ImageDisplay
from FigureDisplay import FigureDisplay

from reader import _BaseReader
from ui.RetinexParamDialog import RetinexParamDialog
from ui.WaitDialog import WaitDialog
from writer import PRESET_WRITERS

from function.hist import drawHistogram
from function.smooth import meanFilter, midFilter
from function.metadata import metaDataAsStr
from function.zoom import zoomIn
from function.otsuSegmentation import OtsuSegmentation
from function.retinex import Retinex
from function.rotate import rotate
from function.reverse import reverse
from function.fft import fft2d, nextPow2, padZero2d
from function.flip import horizontalFlip
from function.sharpen import laplacian
from function.unsharpMasking import unsharpMaskingMeanFilter

from misc.classes import MyImage, ImageZhuoError
from misc.utils import disableResize, normalize255

# 进行缩放后显示的图像尺寸阈值
THRESHOLD_H = 1080 - 80
THRESHOLD_W = 1920 - 80


def ensureCurrentOpen():
    if currentImage is None:
        raise ImageZhuoError('当前没有打开的图像，无法进行该操作！')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.inZoomMode = False

    def toggleBusy(self, to=None):
        waitDialog.setVisible(to)

    @pyqtSlot()
    def on_btn_open_clicked(self):
        global currentImage
        openDialog.show()

    @pyqtSlot()
    def on_btn_wwwl_clicked(self):
        global currentImage
        ensureCurrentOpen()
        wwwlDialog.updateWWWLValue(currentImage.ww, currentImage.wl)
        wwwlDialog.show()

    @pyqtSlot()
    def on_btn_hist_clicked(self):
        global currentImage
        ensureCurrentOpen()
        self.toggleBusy(True)
        figureDisplay.updateFigure(drawHistogram(currentImage.data))
        figureDisplay.show()
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_metadata_clicked(self):
        global currentImage
        ensureCurrentOpen()
        QMessageBox().information(self, '图像元信息 / ImageZhuo',
                                  metaDataAsStr(reader, currentImage))

    @pyqtSlot()
    def on_btn_save_clicked(self):
        global currentImage
        ensureCurrentOpen()
        self.toggleBusy(True)
        writerName, ok1 = QInputDialog.getItem(self,
                                               '请选择写入器',
                                               '写入器：',
                                               PRESET_WRITERS,
                                               editable=False)
        if ok1:
            writerClazz = importlib.import_module(
                'writer.{}'.format(writerName))
            writerClazz = eval('writerClazz.{}'.format(writerName))
            writer = writerClazz(currentImage)
            savePath, _ = QFileDialog.getSaveFileName(self, '请选择保存路径',
                                                      'C:/ImageZhuo_Save.raw')
            if savePath != '':
                writer.save(savePath)
                QMessageBox().information(self, '保存完毕！', '保存完毕！')
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_retinex_clicked(self):
        global currentImage
        ensureCurrentOpen()
        # 处理后仍在4096级灰度范围
        retinexParamDialog.show()

    @pyqtSlot()
    def on_btn_otsu_clicked(self):
        self.toggleBusy(True)
        global currentImage
        ensureCurrentOpen()
        segmentationMask, th = OtsuSegmentation(currentImage.data8bit,
                                                currentImage.h, currentImage.w)
        currentImage = MyImage(segmentationMask.shape[0],
                               segmentationMask.shape[1], segmentationMask)
        imageDisplay.loadFromMyImage(currentImage)
        self.toggleBusy(False)
        QMessageBox().information(self, '大津阈值分割完成',
                                  '大津阈值分割完成！使用的阈值：{}'.format(th))

    @pyqtSlot()
    def on_btn_zoom_clicked(self):
        self.toggleBusy(True)
        global currentImage
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
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_mid_clicked(self):
        self.toggleBusy(True)
        global currentImage
        ensureCurrentOpen()
        ksize, ok = QInputDialog.getInt(self,
                                        '参数询问',
                                        '请输入中值滤波核大小',
                                        3,
                                        min=3,
                                        step=2)
        if ok:
            dstData = midFilter(currentImage.data, ksize)
            currentImage.data = dstData
            currentImage.reGen8bit()
            imageDisplay.loadFromMyImage(currentImage)
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_unsharpmasking_clicked(self):
        self.toggleBusy(True)
        global currentImage
        ensureCurrentOpen()
        ksize, ok1 = QInputDialog.getItem(self,
                                          '请选择均值核尺寸',
                                          '均值核尺寸：', ['3', '5', '7', '9'],
                                          editable=False)
        if ok1:
            ksize = int(ksize)
            k, ok2 = QInputDialog.getDouble(self, '请输入残差权重', '残差权重：', 1.0, 1.0,
                                            5.0)
            if ok2:
                res = unsharpMaskingMeanFilter(currentImage.data, ksize, k)
                currentImage.data = res
                currentImage.reGen8bit()
                imageDisplay.loadFromMyImage(currentImage)
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_rotate_clicked(self):
        global currentImage
        ensureCurrentOpen()
        item, ok = QInputDialog.getItem(self,
                                        '请选择旋转角度',
                                        '旋转角度：', ['90°', '180°', '270°'],
                                        editable=False)
        if ok:
            deg = int(item[:-1])
            self.toggleBusy(True)
            rotatedImage = rotate(currentImage.data, deg)
            currentImage.data = rotatedImage
            currentImage.reGen8bit()
            imageDisplay.loadFromMyImage(currentImage)
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_reset_clicked(self):
        global currentImage
        ensureCurrentOpen()
        currentImage = MyImage(reader.h, reader.w, reader.data)
        imageDisplay.loadFromMyImage(currentImage)

    @pyqtSlot()
    def on_btn_mean_clicked(self):
        self.toggleBusy(True)
        global currentImage
        ensureCurrentOpen()
        ksize, ok = QInputDialog.getInt(self,
                                        '参数询问',
                                        '请输入均值滤波核大小',
                                        3,
                                        min=3,
                                        step=2)
        if ok:
            dstData = meanFilter(currentImage.data, ksize)
            currentImage.data = dstData
            currentImage.reGen8bit()
            imageDisplay.loadFromMyImage(currentImage)
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_reverse_clicked(self):
        global currentImage
        ensureCurrentOpen()
        reverseResult = reverse(currentImage.data)
        currentImage.data = reverseResult
        currentImage.reGen8bit()
        imageDisplay.loadFromMyImage(currentImage)

    @pyqtSlot()
    def on_btn_fft_clicked(self):
        global currentImage
        ensureCurrentOpen()
        if not imageDisplay.by50Percent:
            self.toggleBusy(True)
            padded = padZero2d(currentImage.data, nextPow2(currentImage.h),
                               nextPow2(currentImage.w))
            fftRes = fft2d(padded, fftshift=True)
            # 幅度取对数便于观察
            fftLog = normalize255(np.log(fftRes))
            figureDisplay.updateFigure(Image.fromarray(fftLog))
            figureDisplay.show()
            self.toggleBusy(False)
        else:
            QMessageBox().critical(self, '无法进行2D FFT', '由于图像太大，无法进行2D FFT。',
                                   QMessageBox.Yes, QMessageBox.Yes)

    @pyqtSlot()
    def on_btn_flip_clicked(self):
        global currentImage
        ensureCurrentOpen()
        flipRes = horizontalFlip(currentImage.data)
        currentImage.data = flipRes
        currentImage.reGen8bit()
        imageDisplay.loadFromMyImage(currentImage)

    @pyqtSlot()
    def on_btn_laplacian_clicked(self):
        self.toggleBusy(True)
        global currentImage
        ensureCurrentOpen()
        kOrder, ok = QInputDialog.getItem(self,
                                          '请选择拉普拉斯核阶数',
                                          '拉普拉斯核阶数：', ['1', '2'],
                                          editable=False)

        if ok:
            kOrder = int(kOrder)
            lapRes = laplacian(currentImage.data, kOrder)
            currentImage.data = lapRes
            currentImage.reGen8bit()
            imageDisplay.loadFromMyImage(currentImage)
        self.toggleBusy(False)

    @pyqtSlot()
    def on_btn_autowwwl_clicked(self):
        global currentImage
        ensureCurrentOpen()
        currentImage.defaultWWWL()
        currentImage.reGen8bit()
        imageDisplay.loadFromMyImage(currentImage)


# 处理图像放大
def handle_ImageDisplay_ZoomParams(p0: QPoint, p1: QPoint):
    global mainWindow, currentImage
    if mainWindow.inZoomMode:
        # Make p0: LeftTop, p1: RightBottom
        xmin, xmax = sorted([p0.x(), p1.x()])
        ymin, ymax = sorted([p0.y(), p1.y()])
        p0 = QPoint(xmin, ymin)
        p1 = QPoint(xmax, ymax)
        # Zoom it
        zoomedData = zoomIn(currentImage.data, p0, p1,
                            imageDisplay.by50Percent)
        currentImage.data = np.array(zoomedData, dtype=currentImage.data.dtype)
        currentImage.reGen8bit()
        imageDisplay.loadFromMyImage(currentImage)
        # 消去画的框
        imageDisplay.lbl_display.p0 = QPoint(0, 0)
        imageDisplay.lbl_display.p1 = QPoint(0, 0)


# 处理图像显示窗口关闭
def handle_ImageDisplay_Close():
    global reader, currentImage
    reader = None
    currentImage = None


# 处理打开文件
def handle_OpenDialog_OpenDone(reader_):
    # 接管reader
    global reader, currentImage
    reader = reader_
    # 组装currentImage
    currentImage = MyImage(reader.h, reader.w, reader.data)
    # 显示图片
    if reader.h >= THRESHOLD_H or reader.w >= THRESHOLD_W:
        imageDisplay.toggleBy50Percent()
    imageDisplay.loadFromMyImage(currentImage)
    openDialog.setVisible(False)
    imageDisplay.show()


# 处理窗宽窗位调整
def handle_WWWLDialog_WWWLDone(ww, wl):
    # 调整窗宽窗位
    currentImage.ww = ww
    currentImage.wl = wl
    currentImage.reGen8bit()
    imageDisplay.loadFromMyImage(currentImage)


# 处理Retinex参数
def handle_RetinexParamDialog_retinexParam(gammaH, gammaL, c, D0):
    mainWindow.toggleBusy(True)
    retinexResult = Retinex(currentImage.data, gammaH, gammaL, c, D0)
    currentImage.data = retinexResult
    currentImage.reGen8bit()
    imageDisplay.loadFromMyImage(currentImage)
    retinexParamDialog.setVisible(False)
    mainWindow.toggleBusy(False)


# 处理异常，避免程序崩溃
def customizedExceptHook(exceptionType, exceptionValue, exceptionTraceback):
    traceBackText = "".join(
        traceback.format_exception(exceptionType, exceptionValue,
                                   exceptionTraceback))
    if exceptionType == ImageZhuoError:  # ImageZhuo自定义类型异常
        QMessageBox.critical(mainWindow, '错误提示 / ImageZhuo',
                             exceptionValue.payload + '\n\n' + traceBackText,
                             QMessageBox.Yes, QMessageBox.Yes)
    else:
        QMessageBox.critical(mainWindow, '未知错误提示 / ImageZhuo', traceBackText,
                             QMessageBox.Yes, QMessageBox.Yes)
        print("[Unknown Error]\n", traceBackText)
        # QtWidgets.QApplication.quit()


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

    # Retinex参数对话框
    retinexParamDialog = RetinexParamDialog(mainWindow)
    retinexParamDialog._SignalRetinexParam.connect(
        handle_RetinexParamDialog_retinexParam)

    # 图像显示窗口
    imageDisplay = ImageDisplay()
    imageDisplay._SignalZoomParams.connect(handle_ImageDisplay_ZoomParams)
    imageDisplay._SignalWindowClose.connect(handle_ImageDisplay_Close)

    # 直方图显示窗口
    figureDisplay = FigureDisplay()

    # 提示用户等待窗口
    waitDialog = WaitDialog()

    sys.exit(app.exec_())
