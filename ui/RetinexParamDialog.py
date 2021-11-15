# -*- coding: utf-8 -*-
"""
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from Ui_RetinexParamDialog import Ui_RetinexParamDialog


class RetinexParamDialog(QDialog, Ui_RetinexParamDialog):
    # 向上回报Retinex参数
    _SignalRetinexParam = pyqtSignal(float, float, float, float)

    def __init__(self, parent=None):
        super(RetinexParamDialog, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_btn_done_clicked(self):
        gammaH = self.spin_gammaH.value()
        gammaL = self.spin_gammaL.value()
        c = self.spin_c.value()
        D0 = self.spin_D0.value()
        self._SignalRetinexParam.emit(
            *tuple(map(float, (gammaH, gammaL, c, D0))))
