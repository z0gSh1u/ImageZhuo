from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QColor, QPainter, QPen


class ImageDisplayWidget(QLabel):
    p0 = QPoint(0, 0)
    p1 = QPoint(0, 0)
    dragFlag = False

    def mousePressEvent(self, event):
        self.dragFlag = True
        self.p0 = QPoint(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self.dragFlag = False

    def mouseMoveEvent(self, event):
        if self.dragFlag:
            self.p1 = QPoint(event.x(), event.y())
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.p0, self.p1)
        p = QPainter(self)
        p.setPen(QPen(QColor(0x0000ff), 1))
        p.drawRect(rect)
