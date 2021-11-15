# -*- coding: utf-8 -*-
"""
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo
"""

from PIL import Image
from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtWidgets import QDialog

from Ui_ImageDisplay import Ui_Dialog

from misc.classes import MyImage
from PIL import Image

from misc.utils import disableResize


class ImageDisplay(QDialog, Ui_Dialog):
    # 向上回报放大参数
    _SignalZoomParams = pyqtSignal(QPoint, QPoint)
    # 向上回报窗口关闭
    _SignalWindowClose = pyqtSignal()

    def __init__(self, parent=None):
        super(ImageDisplay, self).__init__(parent)
        self.setupUi(self)
        self.by50Percent = False  # 是否按长宽50%显示（避免过大图片显示不全）
        self.lbl_display._SignalZoomDragDone.connect(
            self.handle_ImageDisplayWidget_ZoomDragDone)

    def toggleBy50Percent(self, to: bool = True):
        self.by50Percent = to

    # 获取图片放大参数（通过拖拽）
    def handle_ImageDisplayWidget_ZoomDragDone(self, p0, p1):
        self._SignalZoomParams.emit(p0, p1)

    # 调节是否允许拖动画框
    def toggleDrag(self, to: bool):
        self.lbl_display.enableDrag = to

    # 从MyImage类型更新显示
    def loadFromMyImage(self, img: MyImage):
        self.lbl_display.aspect = img.h / img.w
        self.loadFromPIL8bit(img.PILImg8bit)

    # 从PIL Image更新显示
    def loadFromPIL8bit(self, pil8bit: Image.Image):
        if self.by50Percent:
            targetDisplaySize = tuple(map(lambda x: x // 2, pil8bit.size))
            # * 由于自己实现的缩放（function/zoom.py）在大图像上效率不高，故此处仍调用PIL库的缩放功能
            pil8bit = pil8bit.resize(targetDisplaySize, Image.BICUBIC)
        else:
            targetDisplaySize = pil8bit.size
        self.setWindowTitle('图像显示 / ImageZhuo ' +
                            ('(50%)' if self.by50Percent else '(100%)'))
        targetWindowSize = tuple(
            map(lambda x: x + 4,
                pil8bit.size))  # 图像显示Label放在(2, 2)处，四周padding为2个像素
        self.resize(*targetWindowSize)
        self.lbl_display.resize(*targetDisplaySize)
        self.lbl_display.setPixmap(pil8bit.toqpixmap())

    # 关闭窗口时销毁reader和currentImage
    def closeEvent(self, event) -> None:
        self._SignalWindowClose.emit()