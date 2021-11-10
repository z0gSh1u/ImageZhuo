# -*- coding: utf-8 -*-
"""
Module implementing OpenDialog.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog

from Ui_OpenDialog import Ui_OpenDialog

import os.path as path

dirname__ = path.dirname(path.abspath(__file__))
import sys

sys.path.append(path.join(dirname__, '../'))

from reader import PRESET_READERS, _BaseReader

import importlib

from ImageDisplay import ImageDisplay


class OpenDialog(QDialog, Ui_OpenDialog):

    _SignalOpenDone = pyqtSignal(_BaseReader)
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(OpenDialog, self).__init__(parent)
        self.setupUi(self)

        self.reader: _BaseReader = None

        self.lbl_hourglass.setVisible(False)

        # 填充预设的Reader
        for reader in PRESET_READERS:
            self.combo_reader.addItem(reader['Name'])
            self.combo_pixelFormat.addItem(reader['DataType'])
        self.combo_reader.setCurrentIndex(0)

    @pyqtSlot()
    def on_btn_browse_clicked(self):
        """
        Slot documentation goes here.
        """
        self.lbl_hourglass.setVisible(True)
        qFileDialog = QFileDialog(self)
        if qFileDialog.exec():
            selectedFilePath = qFileDialog.selectedFiles()[0]
            self.edt_filePath.setText(selectedFilePath)

            # 使用Reader填充元信息
            selectedReader = self.combo_reader.currentText()
            readerClazz = importlib.import_module(
                'reader.{}'.format(selectedReader))
            readerClazz = eval('readerClazz.{}'.format(selectedReader))
            self.reader = readerClazz(selectedFilePath)
            self.edt_width.setText(str(self.reader.w))
            self.edt_height.setText(str(self.reader.h))

        self.lbl_hourglass.setVisible(False)

    @pyqtSlot()
    def on_btn_done_clicked(self):
        """
        Slot documentation goes here.
        """

        self._SignalOpenDone.emit(self.reader)
