# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\ImageZhuo\ui\OpenDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenDialog(object):
    def setupUi(self, OpenDialog):
        OpenDialog.setObjectName("OpenDialog")
        OpenDialog.resize(476, 310)
        OpenDialog.setSizeGripEnabled(True)
        self.gridLayoutWidget = QtWidgets.QWidget(OpenDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 461, 291))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.edt_height = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edt_height.setObjectName("edt_height")
        self.gridLayout.addWidget(self.edt_height, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edt_width = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edt_width.setObjectName("edt_width")
        self.gridLayout.addWidget(self.edt_width, 2, 1, 1, 1)
        self.combo_pixelFormat = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.combo_pixelFormat.setObjectName("combo_pixelFormat")
        self.gridLayout.addWidget(self.combo_pixelFormat, 4, 1, 1, 1)
        self.btn_browse = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_browse.setObjectName("btn_browse")
        self.gridLayout.addWidget(self.btn_browse, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.edt_filePath = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edt_filePath.setObjectName("edt_filePath")
        self.gridLayout.addWidget(self.edt_filePath, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.combo_reader = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.combo_reader.setObjectName("combo_reader")
        self.gridLayout.addWidget(self.combo_reader, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.btn_done = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_done.setObjectName("btn_done")
        self.gridLayout.addWidget(self.btn_done, 5, 1, 1, 1)
        self.lbl_hourglass = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_hourglass.setText("")
        self.lbl_hourglass.setPixmap(QtGui.QPixmap(":/icon/asset/hourglass.png"))
        self.lbl_hourglass.setObjectName("lbl_hourglass")
        self.gridLayout.addWidget(self.lbl_hourglass, 5, 2, 1, 1)

        self.retranslateUi(OpenDialog)
        QtCore.QMetaObject.connectSlotsByName(OpenDialog)
        OpenDialog.setTabOrder(self.edt_filePath, self.btn_browse)
        OpenDialog.setTabOrder(self.btn_browse, self.combo_reader)
        OpenDialog.setTabOrder(self.combo_reader, self.edt_width)
        OpenDialog.setTabOrder(self.edt_width, self.edt_height)
        OpenDialog.setTabOrder(self.edt_height, self.combo_pixelFormat)
        OpenDialog.setTabOrder(self.combo_pixelFormat, self.btn_done)

    def retranslateUi(self, OpenDialog):
        _translate = QtCore.QCoreApplication.translate
        OpenDialog.setWindowTitle(_translate("OpenDialog", "打开文件对话框 / ImageZhuo"))
        self.label_5.setText(_translate("OpenDialog", "像素格式"))
        self.label.setText(_translate("OpenDialog", "文件路径"))
        self.btn_browse.setText(_translate("OpenDialog", "浏览.."))
        self.label_4.setText(_translate("OpenDialog", "高"))
        self.label_2.setText(_translate("OpenDialog", "读取器"))
        self.label_3.setText(_translate("OpenDialog", "宽"))
        self.btn_done.setText(_translate("OpenDialog", "确定"))
import OpenDialog_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenDialog = QtWidgets.QDialog()
    ui = Ui_OpenDialog()
    ui.setupUi(OpenDialog)
    OpenDialog.show()
    sys.exit(app.exec_())