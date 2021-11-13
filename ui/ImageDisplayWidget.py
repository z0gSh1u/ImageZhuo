from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen


class ImageDisplayWidget(QLabel):
    p0 = QPoint(0, 0)
    p1 = QPoint(0, 0)
    enableDrag = False
    dragFlag = False
    aspect = 1 # 控制缩放画框的宽高比

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
            height = abs(event.y() - self.p0.y())
            width = int(height * self.aspect)
            x = self.p0.x() + width * (1 if self.p0.x() < event.x() else -1)
            self.p1 = QPoint(x, event.y())
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.enableDrag:
            rect = QRect(self.p0, self.p1)
            p = QPainter(self)
            p.setPen(QPen(QColor(0x0000ff), 1))
            p.drawRect(rect)
