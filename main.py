import shortuuid
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
import sys



class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 300)
        MainWindow.setMinimumSize(QtCore.QSize(600, 300))
        MainWindow.setMaximumSize(QtCore.QSize(600, 300))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 601, 260))
        self.tabWidget.setObjectName("tabWidget")
        self.Upload = QtWidgets.QWidget()
        self.Upload.setObjectName("Upload")
        self.label = QtWidgets.QLabel(self.Upload)
        self.label.setGeometry(QtCore.QRect(30, 20, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Upload)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 91, 31))
        self.label_2.setObjectName("label_2")
        self.uploadcontID = QtWidgets.QLineEdit(self.Upload)
        self.uploadcontID.setGeometry(QtCore.QRect(120, 70, 441, 20))
        self.uploadcontID.setObjectName("uploadcontID")
        self.uploadcontID.setReadOnly(True);
        self.uploadLocation = QtWidgets.QLineEdit(self.Upload)
        self.uploadLocation.setGeometry(QtCore.QRect(120, 30, 351, 20))
        self.uploadLocation.setObjectName("uploadLocation")
        self.browseUpload = QtWidgets.QToolButton(self.Upload)
        self.browseUpload.setGeometry(QtCore.QRect(490, 30, 71, 19))
        self.browseUpload.setObjectName("browseUpload")
        self.browseUpload.clicked.connect(self.getfileUpload)
        self.upload = QtWidgets.QPushButton(self.Upload)
        self.upload.setGeometry(QtCore.QRect(30, 120, 531, 101))
        self.upload.setObjectName("upload")
        self.tabWidget.addTab(self.Upload, "")
        self.Download = QtWidgets.QWidget()
        self.Download.setObjectName("Download")
        self.label_3 = QtWidgets.QLabel(self.Download)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 91, 31))
        self.label_3.setObjectName("label_3")
        self.downloadcontID = QtWidgets.QLineEdit(self.Download)
        self.downloadcontID.setGeometry(QtCore.QRect(120, 30, 441, 20))
        self.downloadcontID.setObjectName("downloadcontID")
        self.label_4 = QtWidgets.QLabel(self.Download)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 101, 31))
        self.label_4.setObjectName("label_4")
        self.downloadLocation = QtWidgets.QLineEdit(self.Download)
        self.downloadLocation.setGeometry(QtCore.QRect(130, 70, 351, 20))
        self.downloadLocation.setObjectName("downloadLocation")
        self.browseDownload = QtWidgets.QToolButton(self.Download)
        self.browseDownload.setGeometry(QtCore.QRect(490, 70, 71, 20))
        self.browseDownload.setObjectName("browseDownload")
        self.browseDownload.clicked.connect(self.getfileDownload)
        self.download = QtWidgets.QPushButton(self.Download)
        self.download.setGeometry(QtCore.QRect(30, 120, 531, 101))
        self.download.setObjectName("download")
        self.tabWidget.addTab(self.Download, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def getfileUpload(self):
        fpath, _ = QFileDialog.getOpenFileName(self, 'Select file to upload', 'c:\\', "All files (*)")
        self.uploadLocation.setText(fpath)
        ID = shortuuid.random(40);
        self.uploadcontID.setText(ID);

    def getfileDownload(self):
        fname= QFileDialog.getExistingDirectory(self, 'Select save location')
        self.downloadLocation.setText(str(fname))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cargo"))
        self.label.setText(_translate("MainWindow", "File to upload:"))
        self.label_2.setText(_translate("MainWindow", "Container ID:"))
        self.browseUpload.setText(_translate("MainWindow", "Browse"))
        self.upload.setText(_translate("MainWindow", "Upload"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Upload), _translate("MainWindow", "Upload"))
        self.label_3.setText(_translate("MainWindow", "Container ID:"))
        self.label_4.setText(_translate("MainWindow", "Download path:"))
        self.browseDownload.setText(_translate("MainWindow", "Browse"))
        self.download.setText(_translate("MainWindow", "Download"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Download), _translate("MainWindow", "Download"))


def startup():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowIcon(QtGui.QIcon('logo.ico'))
    MainWindow.show()
    sys.exit(app.exec_())


startup()