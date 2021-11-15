# -*- coding: utf-8 -*-
"""
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog

from Ui_OpenDialog import Ui_OpenDialog

import sys
import os.path as path
import importlib
from utils import myAssert

dirname__ = path.dirname(path.abspath(__file__))
sys.path.append(path.join(dirname__, '../'))

from reader import PRESET_READERS, _BaseReader


class OpenDialog(QDialog, Ui_OpenDialog):

    _SignalOpenDone = pyqtSignal(_BaseReader)  # 向父窗口回报图像打开完成

    def __init__(self, parent=None):
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
            # 适配其他raw格式的reader不能自动解析宽高
            self.edt_width.setText(
                str('N/A' if self.reader.w is None else self.reader.w))
            self.edt_height.setText(
                str('N/A' if self.reader.h is None else self.reader.h))
        self.lbl_hourglass.setVisible(False)

    @pyqtSlot()
    def on_btn_done_clicked(self):
        # 进一步检查相关参数
        myAssert(
            len(self.edt_width.getText().strip()) > 0
            and len(self.edt_height.getText().strip()) > 0, '请输入图像的宽高！')
        try:
            if self.reader.w is None:
                self.reader.w = int(self.edt_width.getText())
            if self.reader.h is None:
                self.reader.h = int(self.edt_height.getText())
        except:
            myAssert(False, '请检查宽高是否合法，要求为正整数！')
        myAssert(self.reader.w > 0 and self.reader.h > 0, '请检查宽高是否合法，要求为正整数！')
        self._SignalOpenDone.emit(self.reader)  # 将reader托管到父窗口
