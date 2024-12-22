from PyQt5 import QtCore, QtGui, QtWidgets

from UI.ProgramSetting import ProgramSettingDialog

resourceDir = QtCore.QDir.currentPath() + r"/UI/UI Elements/Main/"


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.mainWindowWidget = QtWidgets.QWidget(MainWindow)
        self.mainWindowWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWindowWidget.sizePolicy().hasHeightForWidth()
        )
        self.mainWindowWidget.setSizePolicy(sizePolicy)
        self.mainWindowWidget.setObjectName("mainWindowWidget")
        self.widgets = QtWidgets.QStackedWidget(self.mainWindowWidget)
        self.widgets.setGeometry(QtCore.QRect(0, 0, 800, 600))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgets.sizePolicy().hasHeightForWidth())
        self.widgets.setSizePolicy(sizePolicy)
        self.widgets.setObjectName("widgets")
        self.Start = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Start.sizePolicy().hasHeightForWidth())

        self.Start.setSizePolicy(sizePolicy)
        self.Start.setObjectName("Start")
        self.TitlePic = QtWidgets.QLabel(self.Start)
        self.TitlePic.setGeometry(QtCore.QRect(10, 10, 771, 221))
        self.TitlePic.setText("")
        self.TitlePic.setPixmap(QtGui.QPixmap(resourceDir + "MainTitle.jpg"))
        self.TitlePic.setScaledContents(True)
        self.TitlePic.setObjectName("TitlePic")

        self.CornerPic = QtWidgets.QLabel(self.Start)
        self.CornerPic.setGeometry(QtCore.QRect(30, 240, 371, 331))
        self.CornerPic.setText("")
        movie = QtGui.QMovie()
        movie.setFileName(resourceDir + "MainCorner.gif")
        self.CornerPic.setMovie(movie)
        movie.start()
        self.CornerPic.setScaledContents(True)
        self.CornerPic.setObjectName("CornerPic")
        self.VersionText = QtWidgets.QLabel(self.Start)
        self.VersionText.setGeometry(QtCore.QRect(20, 575, 371, 21))
        self.VersionText.setObjectName("VersionText")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Start)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(481, 240, 302, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.StartButtons = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.StartButtons.setContentsMargins(0, 0, 0, 0)
        self.StartButtons.setObjectName("StartButtons")
        self.ReadDataButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ReadDataButton.sizePolicy().hasHeightForWidth()
        )
        self.ReadDataButton.setSizePolicy(sizePolicy)
        self.ReadDataButton.setMinimumSize(QtCore.QSize(280, 80))
        self.ReadDataButton.setObjectName("ReadDataButton")
        self.StartButtons.addWidget(
            self.ReadDataButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.ProgramSettingBtiion = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProgramSettingBtiion.sizePolicy().hasHeightForWidth()
        )
        self.ProgramSettingBtiion.setSizePolicy(sizePolicy)
        self.ProgramSettingBtiion.setMinimumSize(QtCore.QSize(280, 80))
        self.ProgramSettingBtiion.setObjectName("ProgramSettingBtiion")
        self.StartButtons.addWidget(
            self.ProgramSettingBtiion,
            0,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
        )
        self.ExitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExitButton.sizePolicy().hasHeightForWidth())
        self.ExitButton.setSizePolicy(sizePolicy)
        self.ExitButton.setMinimumSize(QtCore.QSize(280, 80))
        self.ExitButton.setObjectName("ExitButton")
        self.StartButtons.addWidget(
            self.ExitButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.widgets.addWidget(self.Start)

        self.ReadData = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ReadData.sizePolicy().hasHeightForWidth())
        self.ReadData.setSizePolicy(sizePolicy)
        self.ReadData.setObjectName("ReadData")
        self.scrollArea = QtWidgets.QScrollArea(self.ReadData)
        self.scrollArea.setGeometry(QtCore.QRect(30, 20, 231, 541))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 229, 539))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtWidgets.QLabel(self.ReadData)
        self.label.setGeometry(QtCore.QRect(420, 50, 311, 181))
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setPixmap(
            QtGui.QPixmap(
                "C:/Users/PanHa/Pictures/49d7fde9f169f2405f6b7727b10cd36c2033765513.jpg"
            )
        )
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.widgets.addWidget(self.ReadData)
        MainWindow.setCentralWidget(self.mainWindowWidget)

        self.retranslateUi(MainWindow)
        self.widgets.setCurrentIndex(0)
        self.ReadDataButton.clicked.connect(self.changeToReadDataInterface)  # type: ignore
        self.ProgramSettingBtiion.clicked.connect(self.openProgramSettingDialog)
        self.ExitButton.clicked.connect(MainWindow.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EIS程序嘻嘻"))
        self.VersionText.setText(
            _translate("MainWindow", "Version 0.0.00000000000000001")
        )
        self.ReadDataButton.setText(_translate("MainWindow", "读取数据"))
        self.ProgramSettingBtiion.setText(_translate("MainWindow", "程序设置"))
        self.ExitButton.setText(_translate("MainWindow", "退出"))

    def changePage(self, index: int):
        self.widgets.setCurrentIndex(index)

    def changeToReadDataInterface(self):
        self.changePage(1)

    def openProgramSettingDialog(self):
        self.dialog = ProgramSettingDialog()
        self.dialog.dirSignal.connect(self.receiveDirs)

        self.dialog.readDirs()
        self.dialog.show()

    def receiveDirs(self, dirList):
        print("hello from main.py")
        print(dirList)


class MainWindow(QtWidgets.QMainWindow, MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
