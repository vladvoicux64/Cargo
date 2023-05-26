import shortuuid
import sys
import json
import pysftp
import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtTest import QSignalSpy

if os.name == 'nt':
    import ctypes

    myappid = u'Cargo'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

error_download = 'Download failed. Either check that the file and location exist or the connection parameters.'
error_upload = 'Upload failed. Either check that the file exists or the connection parameters.'


class Worker(QObject):
    status_update = pyqtSignal(str, int)

    connectionattempt_finished = pyqtSignal()
    request_reconnect = pyqtSignal()

    uploadID = pyqtSignal(str)
    uploadattempt_finished = pyqtSignal()

    downloadattempt_finished = pyqtSignal()

    def connectSFTP(self, userdata, usermade):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        try:
            if hasattr(self, 'sftp'):
                self.sftp.close()
            self.sftp = pysftp.Connection(userdata["server"], username=userdata["username"],
                                          password=userdata["password"], cnopts=cnopts)
            if usermade:
                self.status_update.emit("Connection successful.", 5000)
        except:
            if usermade:
                self.status_update.emit("Connection unsuccessful. Check connection parameters and try again.", 5000)

        self.connectionattempt_finished.emit()

    def deco_builder(self, errmsg, additional):
        def retry_w_connection(func):
            def wrapper(args):
                try:
                    func(args)
                except:
                    try:
                        spy = QSignalSpy(self.connectionattempt_finished)
                        self.request_reconnect.emit()
                        spy.wait(1000)
                        func(args)
                    except:
                        if additional is not None: additional(args)
                        self.status_update.emit(errmsg, 5000)

            return wrapper

        return retry_w_connection

    def clean_up(self, args):
        if os.path.exists(args['dlfilePath']) and args['dlID'] != '':
            os.remove(args['dlfilePath'])

    def genID(self, uppath):
        _, extension = uppath.rsplit('.', 1)
        self.upID = shortuuid.random(40) + '.' + extension

    def downloadfile(self, args):
        @self.deco_builder(error_download, self.clean_up)
        def dl(dlargs):
            if (not os.path.exists(dlargs['dlpath'])) or dlargs['dlID'] == '': raise Exception
            self.sftp.get(dlargs['dlID'], dlargs['dlfilePath'])
            self.status_update.emit("File was downloaded successfully.", 5000)

        dl(args)
        self.downloadattempt_finished.emit()

    def uploadfile(self, args):
        @self.deco_builder(error_upload, lambda args: self.uploadID.emit(''))
        def up(upargs):
            if not (upargs['uppath'] != '' and os.path.exists(upargs['uppath'])): raise Exception
            self.genID(upargs['uppath'])
            self.sftp.put(upargs['uppath'], './' + self.upID)
            self.uploadID.emit(self.upID)
            self.status_update.emit("File was uploaded successfully.", 5000)

        up(args)
        self.uploadattempt_finished.emit()


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
        self.label.setGeometry(QtCore.QRect(30, 20, 86, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Upload)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 86, 31))
        self.label_2.setObjectName("label_2")
        self.uploadcontID = QtWidgets.QLineEdit(self.Upload)
        self.uploadcontID.setGeometry(QtCore.QRect(135, 70, 426, 20))
        self.uploadcontID.setObjectName("uploadcontID")
        self.uploadcontID.setReadOnly(True)
        self.uploadLocation = QtWidgets.QLineEdit(self.Upload)
        self.uploadLocation.setGeometry(QtCore.QRect(135, 30, 336, 20))
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
        self.label_3.setGeometry(QtCore.QRect(30, 20, 81, 31))
        self.label_3.setObjectName("label_3")
        self.downloadcontID = QtWidgets.QLineEdit(self.Download)
        self.downloadcontID.setGeometry(QtCore.QRect(135, 30, 426, 20))
        self.downloadcontID.setObjectName("downloadcontID")
        self.label_4 = QtWidgets.QLabel(self.Download)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 96, 31))
        self.label_4.setObjectName("label_4")
        self.downloadLocation = QtWidgets.QLineEdit(self.Download)
        self.downloadLocation.setGeometry(QtCore.QRect(135, 70, 336, 20))
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
        self.label_5.setGeometry(QtCore.QRect(30, 20, 141, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.Connect)
        self.label_6.setGeometry(QtCore.QRect(30, 70, 91, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.Connect)
        self.label_7.setGeometry(QtCore.QRect(30, 120, 91, 31))
        self.label_7.setObjectName("label_7")
        self.serverAdress = QtWidgets.QLineEdit(self.Connect)
        self.serverAdress.setGeometry(QtCore.QRect(180, 30, 381, 20))
        self.serverAdress.setObjectName("serverAdress")
        self.serverAdress.textEdited.connect(self.save_userdata)
        self.username = QtWidgets.QLineEdit(self.Connect)
        self.username.setGeometry(QtCore.QRect(130, 80, 431, 20))
        self.username.setObjectName("username")
        self.username.textEdited.connect(self.save_userdata)
        self.passwd = QtWidgets.QLineEdit(self.Connect)
        self.passwd.setGeometry(QtCore.QRect(130, 130, 431, 20))
        self.passwd.setObjectName("passwd")
        self.passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwd.textEdited.connect(self.save_userdata)
        self.connectButton = QtWidgets.QPushButton(self.Connect)
        self.connectButton.setGeometry(QtCore.QRect(30, 180, 531, 31))
        self.connectButton.setObjectName("connectButton")
        self.connectButton.clicked.connect(lambda: self.connectSFTP(True))
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

    startconnection = pyqtSignal(object, bool)
    startupload = pyqtSignal(dict)
    startdownload = pyqtSignal(dict)

    def init_worker(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.worker.status_update.connect(self.display_msg)

        self.startconnection.connect(self.worker.connectSFTP)
        self.worker.connectionattempt_finished.connect(lambda: self.connectButton.setEnabled(True))
        self.worker.request_reconnect.connect(lambda: self.connectSFTP((False)))

        self.startupload.connect(self.worker.uploadfile)
        self.worker.uploadID.connect(lambda ID: self.fetchID(ID))
        self.worker.uploadattempt_finished.connect(lambda: self.upload.setEnabled(True))

        self.startdownload.connect(self.worker.downloadfile)
        self.worker.downloadattempt_finished.connect(lambda: self.download.setEnabled(True))

        self.thread.start()

    def display_msg(self, msg, time):
        self.statusbar.showMessage(msg, time)

    def display_userdata(self):
        self.serverAdress.setText(self.userdata["server"])
        self.username.setText(self.userdata["username"])
        self.passwd.setText(self.userdata["password"])

    def init_userdata(self):
        try:
            with open("secret.json", "r") as secret_file:
                self.userdata = json.load(secret_file)
            self.display_userdata()
        except:
            self.userdata = {
                "server": "ip:port",
                "username": "username",
                "password": "password"
            }
            self.display_userdata()
            self.statusbar.showMessage("No secret.json file found. Using default connection parameters.", 5000)

    def save_userdata(self):
        self.userdata = {
            "server": self.serverAdress.text(),
            "username": self.username.text(),
            "password": self.passwd.text()
        }

        with open("secret.json", "w+") as secret_file:
            json.dump(self.userdata, secret_file)

    def connectSFTP(self, usermade):
        self.connectButton.setEnabled(False)
        self.startconnection.emit(self.userdata, usermade)

    def getfileUpload(self):
        uppath, _ = QFileDialog.getOpenFileName(self, 'Select file to upload', '', "All files (*)")
        self.uploadLocation.setText(uppath)

    def getfileDownload(self):
        dlpath = QFileDialog.getExistingDirectory(self, 'Select save location')
        self.downloadLocation.setText(str(dlpath))

    def fetchID(self, ID):
        self.uploadcontID.setText(ID)

    def uploadfile(self):
        self.upload.setEnabled(False)
        self.startupload.emit({'uppath': self.uploadLocation.text()})

    def downloadfile(self):
        self.download.setEnabled(False)
        self.startdownload.emit({'dlpath': self.downloadLocation.text(), 'dlID': self.downloadcontID.text(),
                                 'dlfilePath': self.downloadLocation.text() + '/' + self.downloadcontID.text()})

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
    ui.init_worker()
    MainWindow.show()
    sys.exit(app.exec_())


startup()
