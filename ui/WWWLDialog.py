# -*- coding: utf-8 -*-
"""
Module implementing WWWLDialog.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from Ui_WWWLDialog import Ui_Dialog


class WWWLDialog(QDialog, Ui_Dialog):
    _SignalWWWLDone = pyqtSignal(int, int)
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        super(WWWLDialog, self).__init__(parent)
        self.setupUi(self)

    def updateWWWLValue(self, ww, wl):
        self.spin_ww.setValue(ww)
        self.spin_wl.setValue(wl)
        

    @pyqtSlot()
    def on_btn_apply_clicked(self):
        ww = self.spin_ww.value()
        wl = self.spin_wl.value()
        self._SignalWWWLDone.emit(ww, wl)
