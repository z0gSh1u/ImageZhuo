# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from numpy import dtype

from Ui_MainWindow import Ui_MainWindow
from OpenDialog import OpenDialog
from WWWLDialog import WWWLDialog

from ImageDisplay import ImageDisplay
from function.window import windowData

import numpy as np

from utils import disableResize


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_open_clicked(self):
        """
        Slot documentation goes here.
        """
        openDialog.show()

    @pyqtSlot()
    def on_btn_wwwl_clicked(self):
        """
        Slot documentation goes here.
        """
        wwwlDialog.show()


# Event bus


def handle_OpenDialog_OpenDone(reader):
    imageDisplay.loadByReader(reader)
    disableResize(imageDisplay)
    openDialog.setVisible(False)
    imageDisplay.show()


def handle_WWWLDialog_WWWLDone(ww, wl):
    _data = imageDisplay.reader.data
    _data = windowData(_data, ww, wl, 0, 255)
    imageDisplay.refresh(np.array(_data, dtype=np.uint8))
    wwwlDialog.setVisible(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    openDialog = OpenDialog(mainWindow)
    openDialog._SignalOpenDone.connect(handle_OpenDialog_OpenDone)

    wwwlDialog = WWWLDialog(mainWindow)
    wwwlDialog._SignalWWWLDone.connect(handle_WWWLDialog_WWWLDone)

    imageDisplay = ImageDisplay()

    sys.exit(app.exec_())
