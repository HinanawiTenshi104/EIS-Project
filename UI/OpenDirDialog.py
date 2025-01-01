import os

from PyQt6 import QtCore, QtWidgets


class OpenDirDialog(object):
    dirs = {}

    def setupUi(self, OpenDirDialog):
        OpenDirDialog.setObjectName("OpenDirDialog")
        OpenDirDialog.resize(150, 211)
        self.widget = QtWidgets.QWidget(parent=OpenDirDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 131, 191))
        self.widget.setObjectName("widget")
        self.ButtonsLayout = QtWidgets.QVBoxLayout(self.widget)
        self.ButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.ButtonsLayout.setSpacing(0)
        self.ButtonsLayout.setObjectName("ButtonsLayout")
        self.ResultButton = QtWidgets.QPushButton(parent=self.widget)
        self.ResultButton.setMinimumSize(QtCore.QSize(0, 40))
        self.ResultButton.setObjectName("ResultButton")
        self.ButtonsLayout.addWidget(self.ResultButton)
        self.ExpDataButton = QtWidgets.QPushButton(parent=self.widget)
        self.ExpDataButton.setMinimumSize(QtCore.QSize(0, 40))
        self.ExpDataButton.setObjectName("ExpDataButton")
        self.ButtonsLayout.addWidget(self.ExpDataButton)
        self.ProcessedDataButton = QtWidgets.QPushButton(parent=self.widget)
        self.ProcessedDataButton.setMinimumSize(QtCore.QSize(0, 40))
        self.ProcessedDataButton.setObjectName("ProcessedDataButton")
        self.ButtonsLayout.addWidget(self.ProcessedDataButton)
        self.DRTDataButton = QtWidgets.QPushButton(parent=self.widget)
        self.DRTDataButton.setMinimumSize(QtCore.QSize(0, 40))
        self.DRTDataButton.setObjectName("DRTDataButton")
        self.ButtonsLayout.addWidget(self.DRTDataButton)

        self.retranslateUi(OpenDirDialog)
        self.ResultButton.clicked.connect(OpenDirDialog.openResultDir)  # type: ignore
        self.ProcessedDataButton.clicked.connect(OpenDirDialog.openProcessedDataDir)  # type: ignore
        self.ExpDataButton.clicked.connect(OpenDirDialog.openExpDataDir)  # type: ignore
        self.DRTDataButton.clicked.connect(OpenDirDialog.openDRTDataDir)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(OpenDirDialog)
        OpenDirDialog.setTabOrder(self.ResultButton, self.ExpDataButton)
        OpenDirDialog.setTabOrder(self.ExpDataButton, self.ProcessedDataButton)
        OpenDirDialog.setTabOrder(self.ProcessedDataButton, self.DRTDataButton)

    def retranslateUi(self, OpenDirDialog):
        _translate = QtCore.QCoreApplication.translate
        OpenDirDialog.setWindowTitle(_translate("OpenDirDialog", "打开目录"))
        self.ResultButton.setText(_translate("OpenDirDialog", "拟合结果目录"))
        self.ExpDataButton.setText(_translate("OpenDirDialog", "实验数据目录"))
        self.ProcessedDataButton.setText(
            _translate("OpenDirDialog", "预处理后数据目录")
        )
        self.DRTDataButton.setText(_translate("OpenDirDialog", "DRT数据目录"))

    def openDir(self, dir: str):
        os.startfile(dir)

    def openResultDir(self):
        dir = self.dirs["Result Dir"]
        self.openDir(dir)

    def openProcessedDataDir(self):
        dir = self.dirs["Processed Data Dir"]
        self.openDir(dir)

    def openExpDataDir(self):
        dir = self.dirs["Data Dir"]
        self.openDir(dir)

    def openDRTDataDir(self):
        dir = self.dirs["DRT Data Dir"]
        self.openDir(dir)


class OpenDirDialog(QtWidgets.QDialog, OpenDirDialog):
    def __init__(self):
        super(OpenDirDialog, self).__init__()
        self.setupUi(self)
