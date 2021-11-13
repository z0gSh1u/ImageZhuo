# -*- coding: utf-8 -*-
"""
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo
"""

from PyQt5.QtWidgets import QDialog

from Ui_WaitDialog import Ui_WaitDialog


class WaitDialog(QDialog, Ui_WaitDialog):

    def __init__(self, parent=None):
        super(WaitDialog, self).__init__(parent)
        self.setupUi(self)
