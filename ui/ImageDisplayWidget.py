"""
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen

from misc.utils import minmaxClip


class ImageDisplayWidget(QLabel):
    p0 = QPoint(0, 0)
    p1 = QPoint(0, 0)
    enableDrag = False
    dragFlag = False
    aspect = None  # 控制缩放画框的宽高比，等比画框

    _SignalZoomDragDone = pyqtSignal(QPoint, QPoint)

    def mousePressEvent(self, event):
        if self.enableDrag:
            self.dragFlag = True
            self.p0 = QPoint(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        if self.enableDrag:
            self.dragFlag = False
            self._SignalZoomDragDone.emit(self.p0, self.p1)

    def mouseMoveEvent(self, event):
        if self.enableDrag and self.dragFlag:
            # 检查框大小不画出图像范围
            y = minmaxClip(event.y(), 0, self.height())
            height = abs(y - self.p0.y())
            # 控制等比画框
            width = int(height * self.aspect)
            x = self.p0.x() + width * (1 if self.p0.x() < event.x() else -1)
            # 检查框大小不画出图像范围
            x = minmaxClip(x, 0, self.width())
            self.p1 = QPoint(x, y)
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.enableDrag:
            rect = QRect(self.p0, self.p1)
            p = QPainter(self)
            p.setPen(QPen(QColor(0x0000ff), 1))
            p.drawRect(rect)
