# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\ImageZhuo\ui/FigureDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FigureDisplay(object):
    def setupUi(self, FigureDisplay):
        FigureDisplay.setObjectName("FigureDisplay")
        FigureDisplay.resize(432, 324)
        FigureDisplay.setSizeGripEnabled(True)
        self.lbl_display = QtWidgets.QLabel(FigureDisplay)
        self.lbl_display.setGeometry(QtCore.QRect(4, 4, 72, 15))
        self.lbl_display.setObjectName("lbl_display")

        self.retranslateUi(FigureDisplay)
        QtCore.QMetaObject.connectSlotsByName(FigureDisplay)

    def retranslateUi(self, FigureDisplay):
        _translate = QtCore.QCoreApplication.translate
        FigureDisplay.setWindowTitle(_translate("FigureDisplay", "图表显示 / ImageZhuo"))
        self.lbl_display.setText(_translate("FigureDisplay", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FigureDisplay = QtWidgets.QDialog()
    ui = Ui_FigureDisplay()
    ui.setupUi(FigureDisplay)
    FigureDisplay.show()
    sys.exit(app.exec_())
