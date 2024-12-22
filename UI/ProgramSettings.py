import configparser

from PyQt6 import QtCore, QtGui, QtWidgets

configsDir = QtCore.QDir.currentPath() + r"/configs/"
configFileName = "Program Settings.ini"
configFilePath = configsDir + configFileName

sectionNames = ["Dir Settings", "MultiThread Settings", "DRT Settings"]
skipList = [sectionNames[0]]

from .DirSetting import DirSettingDialog


class ProgramSettingsDialog(object):
    dirSettings = None
    multiThreadSettings = {
        "Enable MultiThread": "No",
        "Thread Limit": "1",
    }
    DRTSettings = {"Overwrite DRT Data": "Yes"}

    settings = [dirSettings, multiThreadSettings, DRTSettings]

    settingsSignal = QtCore.pyqtSignal(list)

    def setupUi(self, ProgramSettingsDialog):
        ProgramSettingsDialog.setObjectName("ProgramSettingsDialog")
        ProgramSettingsDialog.resize(181, 270)
        self.ChangeDirButton = QtWidgets.QPushButton(parent=ProgramSettingsDialog)
        self.ChangeDirButton.setGeometry(QtCore.QRect(20, 20, 141, 51))
        self.ChangeDirButton.setObjectName("ChangeDirButton")
        self.MultiThreadCheckBox = QtWidgets.QCheckBox(parent=ProgramSettingsDialog)
        self.MultiThreadCheckBox.setGeometry(QtCore.QRect(20, 90, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MultiThreadCheckBox.setFont(font)
        self.MultiThreadCheckBox.setObjectName("MultiThreadCheckBox")
        self.staticLabel1 = QtWidgets.QLabel(parent=ProgramSettingsDialog)
        self.staticLabel1.setGeometry(QtCore.QRect(20, 120, 101, 21))
        self.staticLabel1.setObjectName("staticLabel1")
        self.ThreadLimitSpinBox = QtWidgets.QSpinBox(parent=ProgramSettingsDialog)
        self.ThreadLimitSpinBox.setGeometry(QtCore.QRect(20, 150, 121, 21))
        self.ThreadLimitSpinBox.setMinimum(-1)
        self.ThreadLimitSpinBox.setObjectName("ThreadLimitSpinBox")
        self.OverwriteDRTDataCheckBox = QtWidgets.QCheckBox(
            parent=ProgramSettingsDialog
        )
        self.OverwriteDRTDataCheckBox.setGeometry(QtCore.QRect(20, 190, 141, 20))
        self.OverwriteDRTDataCheckBox.setObjectName("OverwriteDRTDataCheckBox")
        self.layoutWidget = QtWidgets.QWidget(parent=ProgramSettingsDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 220, 158, 42))
        self.layoutWidget.setObjectName("layoutWidget")
        self.ButtomButtons = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.ButtomButtons.setContentsMargins(0, 0, 0, 0)
        self.ButtomButtons.setObjectName("ButtomButtons")
        self.CloseButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.CloseButton.setMinimumSize(QtCore.QSize(0, 40))
        self.CloseButton.setObjectName("CloseButton")
        self.ButtomButtons.addWidget(self.CloseButton)
        self.SaveSettingsButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.SaveSettingsButton.setMinimumSize(QtCore.QSize(0, 40))
        self.SaveSettingsButton.setObjectName("SaveSettingsButton")
        self.ButtomButtons.addWidget(self.SaveSettingsButton)

        self.retranslateUi(ProgramSettingsDialog)
        self.ChangeDirButton.clicked.connect(ProgramSettingsDialog.changeDirButtonClicked)  # type: ignore
        self.ThreadLimitSpinBox.valueChanged["int"].connect(ProgramSettingsDialog.threadLimitChanged)  # type: ignore
        self.MultiThreadCheckBox.clicked.connect(ProgramSettingsDialog.multiThreadCheckBoxChanged)  # type: ignore
        self.OverwriteDRTDataCheckBox.clicked.connect(ProgramSettingsDialog.overwriteDRTDataChanged)  # type: ignore
        self.CloseButton.clicked.connect(ProgramSettingsDialog.close)  # type: ignore
        self.SaveSettingsButton.clicked.connect(ProgramSettingsDialog.saveSettings)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ProgramSettingsDialog)
        ProgramSettingsDialog.setTabOrder(
            self.ChangeDirButton, self.MultiThreadCheckBox
        )
        ProgramSettingsDialog.setTabOrder(
            self.MultiThreadCheckBox, self.ThreadLimitSpinBox
        )
        ProgramSettingsDialog.setTabOrder(
            self.ThreadLimitSpinBox, self.OverwriteDRTDataCheckBox
        )
        ProgramSettingsDialog.setTabOrder(
            self.OverwriteDRTDataCheckBox, self.CloseButton
        )
        ProgramSettingsDialog.setTabOrder(self.CloseButton, self.SaveSettingsButton)

    def retranslateUi(self, ProgramSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgramSettingsDialog.setWindowTitle(
            _translate("ProgramSettingsDialog", "程序设置")
        )
        self.ChangeDirButton.setText(
            _translate("ProgramSettingsDialog", "更改各种路径")
        )
        self.MultiThreadCheckBox.setText(
            _translate("ProgramSettingsDialog", "启用多线程")
        )
        self.staticLabel1.setText(_translate("ProgramSettingsDialog", "线程上限："))
        self.OverwriteDRTDataCheckBox.setText(
            _translate("ProgramSettingsDialog", "是否总是覆盖DRT数据")
        )
        self.CloseButton.setText(_translate("ProgramSettingsDialog", "关闭"))
        self.SaveSettingsButton.setText(_translate("ProgramSettingsDialog", "保存设置"))

    def setupComponents(self):
        self.dirSettingDialog = DirSettingDialog()
        self.dirSettingDialog.configFilePath = configFilePath
        self.dirSettingDialog.sectionName = sectionNames[0]
        self.dirSettingDialog.dirSignal.connect(self.receiveDirs)

        self.dirSettingDialog.setupComponents()
        self.dirSettingDialog.emitDirs()

        self.readSettings()

    def updateUIs(self):
        if self.multiThreadSettings["Enable MultiThread"] == "Yes":
            self.MultiThreadCheckBox.setChecked(True)
            threadLimit = int(self.multiThreadSettings["Thread Limit"])
            self.ThreadLimitSpinBox.setValue(threadLimit)
        else:
            self.MultiThreadCheckBox.setChecked(False)

        self.ThreadLimitSpinBox.setEnabled(self.MultiThreadCheckBox.isChecked())

        if self.DRTSettings["Overwrite DRT Data"] == "Yes":
            self.OverwriteDRTDataCheckBox.setChecked(True)
        else:
            self.OverwriteDRTDataCheckBox.setChecked(False)

    def changeDirButtonClicked(self):
        self.dirSettingDialog.setupComponents()
        self.dirSettingDialog.show()

    def receiveDirs(self, dirs):
        self.settings[0] = dirs
        print("Dirs Received by ProgramSettings!")

    def threadLimitChanged(self, limit: int):
        self.multiThreadSettings["Thread Limit"] = str(limit)
        self.updateUIs()

    def multiThreadCheckBoxChanged(self):
        if self.MultiThreadCheckBox.isChecked():
            self.multiThreadSettings["Enable MultiThread"] = "Yes"
        else:
            self.multiThreadSettings["Enable MultiThread"] = "No"

        self.updateUIs()

    def overwriteDRTDataChanged(self):
        if self.OverwriteDRTDataCheckBox.isChecked():
            self.DRTSettings["Overwrite DRT Data"] = "Yes"
        else:
            self.DRTSettings["Overwrite DRT Data"] = "No"

        self.updateUIs()

    def emitSettings(self):
        print("Settings Emitted!")
        self.settingsSignal.emit(self.settings)

    def readSettings(self):
        config = configparser.ConfigParser()
        config.read(configFilePath)

        if len(config.sections()) != 0:
            for setting, sectionName in zip(self.settings, sectionNames):
                if sectionName in skipList:
                    continue

                for key in setting.keys():
                    text = config[sectionName][key]
                    if text != "":
                        setting[key] = text

            self.updateUIs()

    def writeSettings(self):
        config = configparser.ConfigParser()

        for setting, sectionName in zip(self.settings, sectionNames):
            config[sectionName] = setting

        with open(configFilePath, "w") as configfile:
            config.write(configfile)

    def saveSettings(self):
        self.writeSettings()
        self.emitSettings()
        self.close()


class ProgramSettingsDialog(QtWidgets.QDialog, ProgramSettingsDialog):
    def __init__(self):
        super(ProgramSettingsDialog, self).__init__()
        self.setupUi(self)
        self.setupComponents()
