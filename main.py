import shortuuid
import sys
import json
import pysftp
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget

if(os.name == 'nt'):
    import ctypes
    myappid = u'Cargo'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
        self.label.setGeometry(QtCore.QRect(30, 20, 71, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Upload)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 71, 31))
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
        self.upload.clicked.connect(self.uploadfile)
        self.tabWidget.addTab(self.Upload, "")
        self.Download = QtWidgets.QWidget()
        self.Download.setObjectName("Download")
        self.label_3 = QtWidgets.QLabel(self.Download)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 71, 31))
        self.label_3.setObjectName("label_3")
        self.downloadcontID = QtWidgets.QLineEdit(self.Download)
        self.downloadcontID.setGeometry(QtCore.QRect(120, 30, 441, 20))
        self.downloadcontID.setObjectName("downloadcontID")
        self.label_4 = QtWidgets.QLabel(self.Download)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 81, 31))
        self.label_4.setObjectName("label_4")
        self.downloadLocation = QtWidgets.QLineEdit(self.Download)
        self.downloadLocation.setGeometry(QtCore.QRect(120, 70, 351, 20))
        self.downloadLocation.setObjectName("downloadLocation")
        self.browseDownload = QtWidgets.QToolButton(self.Download)
        self.browseDownload.setGeometry(QtCore.QRect(490, 70, 71, 20))
        self.browseDownload.setObjectName("browseDownload")
        self.browseDownload.clicked.connect(self.getfileDownload)
        self.download = QtWidgets.QPushButton(self.Download)
        self.download.setGeometry(QtCore.QRect(30, 120, 531, 101))
        self.download.setObjectName("download")
        self.download.clicked.connect(self.downloadfile)
        self.tabWidget.addTab(self.Download, "")
        self.Connect = QtWidgets.QWidget()
        self.Connect.setObjectName("Connect")
        self.label_5 = QtWidgets.QLabel(self.Connect)
        self.label_5.setGeometry(QtCore.QRect(30, 20, 121, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.Connect)
        self.label_6.setGeometry(QtCore.QRect(30, 70, 71, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.Connect)
        self.label_7.setGeometry(QtCore.QRect(30, 120, 71, 31))
        self.label_7.setObjectName("label_7")
        self.serverAdress = QtWidgets.QLineEdit(self.Connect)
        self.serverAdress.setGeometry(QtCore.QRect(160, 30, 401, 20))
        self.serverAdress.setObjectName("serverAdress")
        self.username = QtWidgets.QLineEdit(self.Connect)
        self.username.setGeometry(QtCore.QRect(120, 80, 441, 20))
        self.username.setObjectName("username")
        self.passwd = QtWidgets.QLineEdit(self.Connect)
        self.passwd.setGeometry(QtCore.QRect(120, 130, 441, 20))
        self.passwd.setObjectName("passwd")
        self.passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.connectButton = QtWidgets.QPushButton(self.Connect)
        self.connectButton.setGeometry(QtCore.QRect(30, 180, 531, 31))
        self.connectButton.setObjectName("connectButton")
        self.connectButton.clicked.connect(self.connectSFTP)
        self.tabWidget.addTab(self.Connect, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def genID(self):
        if self.uppath != '' and os.path.exists(self.uppath):
            self.uploadLocation.setText(self.uppath)
            _, extension = self.uppath.rsplit('.', 1)
            self.upID = shortuuid.random(40) + '.' + extension
            self.uploadcontID.setText(self.upID)

    def getfileUpload(self):
        self.uppath, _ = QFileDialog.getOpenFileName(self, 'Select file to upload', '', "All files (*)")
        self.uploadLocation.setText(self.uppath)

    def getfileDownload(self):
        self.dlpath = QFileDialog.getExistingDirectory(self, 'Select save location')
        self.downloadLocation.setText(str(self.dlpath))

    def display_userdata(self):
        self.serverAdress.setText(self.userdata["server"])
        self.username.setText(self.userdata["user"])
        self.passwd.setText(self.userdata["pass"])
    def init_userdata(self):
        try:
            with open("secret.json", "r") as secret_file:
                self.userdata = json.load(secret_file)
            self.display_userdata()
        except:
            self.userdata = {
                "server" : "ip:port",
                "user" : "username",
                "pass" : "password"
            }
            self.display_userdata()
            self.statusbar.showMessage("No secret.json file found. Using default connection parameters.", 5000)

    def connectSFTP(self):
        self.userdata["server"] = self.serverAdress.text()
        self.userdata["user"] = self.username.text()
        self.userdata["pass"] = self.passwd.text()

        with open("secret.json", "w+") as secret_file:
            json.dump(self.userdata, secret_file)

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        try:
            if(hasattr(self, "sftp")):
                self.sftp.close()
            self.sftp = pysftp.Connection(self.userdata["server"], username=self.userdata["user"], password= self.userdata["pass"], cnopts=cnopts)
            self.statusbar.showMessage("Connection successful.", 5000)
        except:
            self.statusbar.showMessage("Connection unsuccessful. Check connection parameters and try again.", 5000)

    def downloadfile(self):
        self.dlpath = self.downloadLocation.text()
        self.dlID = self.downloadcontID.text()
        self.dlfilePath = self.dlpath + '/' + self.dlID
        def dl():
            if (not os.path.exists(self.dlpath)) or self.dlID == '': raise Exception
            self.sftp.get(self.dlID, self.dlfilePath)
            self.statusbar.showMessage("File was downloaded successfully.", 5000)

        try:
            dl()
        except:
            try:
                self.connectSFTP()
                dl()
            except:
                if os.path.exists(self.dlfilePath):
                    os.remove(self.dlfilePath)
                self.statusbar.showMessage("Download failed. Either check that the file and location exist or the connection parameters.", 5000)


    def uploadfile(self):
        self.uppath = self.uploadLocation.text()
        def up():
            self.genID()
            self.sftp.put(self.uppath, './' + self.upID)
            self.statusbar.showMessage("File was uploaded successfully.", 5000)

        try:
            up()
        except:
            try:
                self.connectSFTP()
                up()
            except:
                self.statusbar.showMessage("Upload failed. Either check that the file exists or the connection parameters.", 5000)

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
        self.label_5.setText(_translate("MainWindow", "Server adress and port:"))
        self.label_6.setText(_translate("MainWindow", "SSH username:"))
        self.label_7.setText(_translate("MainWindow", "SSH password:"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Connect), _translate("MainWindow", "Connection"))


def startup():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('logo.ico'))
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.init_userdata()
    MainWindow.show()
    sys.exit(app.exec_())


startup()