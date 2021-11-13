# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\ImageZhuo\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(621, 392)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/asset/bitbug_favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 100, 601, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_fft = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_fft.setObjectName("btn_fft")
        self.gridLayout.addWidget(self.btn_fft, 1, 2, 1, 1)
        self.btn_metadata = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_metadata.setObjectName("btn_metadata")
        self.gridLayout.addWidget(self.btn_metadata, 0, 1, 1, 1)
        self.btn_unsharpmasking = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_unsharpmasking.setObjectName("btn_unsharpmasking")
        self.gridLayout.addWidget(self.btn_unsharpmasking, 3, 1, 1, 1)
        self.btn_retinex = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_retinex.setObjectName("btn_retinex")
        self.gridLayout.addWidget(self.btn_retinex, 3, 2, 1, 1)
        self.btn_laplacian = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_laplacian.setObjectName("btn_laplacian")
        self.gridLayout.addWidget(self.btn_laplacian, 4, 2, 1, 1)
        self.btn_mean = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_mean.setObjectName("btn_mean")
        self.gridLayout.addWidget(self.btn_mean, 4, 0, 1, 1)
        self.btn_wwwl = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_wwwl.setObjectName("btn_wwwl")
        self.gridLayout.addWidget(self.btn_wwwl, 1, 0, 1, 1)
        self.btn_open = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_open.setObjectName("btn_open")
        self.gridLayout.addWidget(self.btn_open, 0, 0, 1, 1)
        self.btn_mid = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_mid.setObjectName("btn_mid")
        self.gridLayout.addWidget(self.btn_mid, 4, 1, 1, 1)
        self.btn_autowwwl = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_autowwwl.setObjectName("btn_autowwwl")
        self.gridLayout.addWidget(self.btn_autowwwl, 5, 1, 1, 1)
        self.btn_flip = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_flip.setObjectName("btn_flip")
        self.gridLayout.addWidget(self.btn_flip, 2, 2, 1, 1)
        self.btn_reset = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_reset.setObjectName("btn_reset")
        self.gridLayout.addWidget(self.btn_reset, 5, 2, 1, 1)
        self.btn_zoom = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_zoom.setObjectName("btn_zoom")
        self.gridLayout.addWidget(self.btn_zoom, 2, 0, 1, 1)
        self.btn_reverse = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_reverse.sizePolicy().hasHeightForWidth())
        self.btn_reverse.setSizePolicy(sizePolicy)
        self.btn_reverse.setObjectName("btn_reverse")
        self.gridLayout.addWidget(self.btn_reverse, 5, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 0, 2, 1, 1)
        self.btn_hist = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_hist.setObjectName("btn_hist")
        self.gridLayout.addWidget(self.btn_hist, 1, 1, 1, 1)
        self.btn_rotate = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_rotate.setObjectName("btn_rotate")
        self.gridLayout.addWidget(self.btn_rotate, 2, 1, 1, 1)
        self.btn_otsu = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_otsu.setObjectName("btn_otsu")
        self.gridLayout.addWidget(self.btn_otsu, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 350, 531, 20))
        self.label_2.setObjectName("label_2")
        self.lbl_banner = QtWidgets.QLabel(self.centralwidget)
        self.lbl_banner.setGeometry(QtCore.QRect(180, 10, 261, 61))
        self.lbl_banner.setText("")
        self.lbl_banner.setPixmap(QtGui.QPixmap(":/banner/asset/banner.png"))
        self.lbl_banner.setObjectName("lbl_banner")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 195, 59))
        self.label.setMinimumSize(QtCore.QSize(0, 59))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ImageZhuo / SEU / 212138-卓旭 @ github.com/z0gSh1u/ImageZhuo"))
        self.btn_fft.setText(_translate("MainWindow", "FFT 幅度频谱"))
        self.btn_metadata.setText(_translate("MainWindow", "当前图像元信息"))
        self.btn_unsharpmasking.setText(_translate("MainWindow", "Unsharp Masking"))
        self.btn_retinex.setText(_translate("MainWindow", "Retinex 同态滤波"))
        self.btn_laplacian.setText(_translate("MainWindow", "拉普拉斯算子"))
        self.btn_mean.setText(_translate("MainWindow", "均值滤波"))
        self.btn_wwwl.setText(_translate("MainWindow", "调节窗宽窗位"))
        self.btn_open.setText(_translate("MainWindow", "打开图像"))
        self.btn_mid.setText(_translate("MainWindow", "中值滤波"))
        self.btn_autowwwl.setText(_translate("MainWindow", "自动窗宽窗位"))
        self.btn_flip.setText(_translate("MainWindow", "水平镜像"))
        self.btn_reset.setText(_translate("MainWindow", "重置为原图"))
        self.btn_zoom.setText(_translate("MainWindow", "放大 [未激活]"))
        self.btn_reverse.setText(_translate("MainWindow", "反相"))
        self.btn_save.setText(_translate("MainWindow", "保存当前图像"))
        self.btn_hist.setText(_translate("MainWindow", "灰度直方图"))
        self.btn_rotate.setText(_translate("MainWindow", "旋转"))
        self.btn_otsu.setText(_translate("MainWindow", "大津阈值分割"))
        self.label_2.setText(_translate("MainWindow", "ImageZhuo / SEU / 212138-卓旭 / github.com/z0gSh1u/ImageZhuo"))
        self.label.setText(_translate("MainWindow", "ImageZhuo 功能列表"))
import MainWindow_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
