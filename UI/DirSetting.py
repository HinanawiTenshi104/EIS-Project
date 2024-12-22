import configparser

from PyQt6 import QtCore, QtGui, QtWidgets


class DirSettingDialog(object):
    configFilePath = ""
    sectionName = ""

    dirs = {
        "Data Dir": "",
        "DRT Data Dir": "",
        "Result Dir": "",
    }
    dirSignal = QtCore.pyqtSignal(dict)

    def setupUi(self, DirSettingDialog):
        DirSettingDialog.setObjectName("DirSettingDialog")
        DirSettingDialog.resize(400, 380)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DirSettingDialog.sizePolicy().hasHeightForWidth())
        DirSettingDialog.setSizePolicy(sizePolicy)
        self.layoutWidget = QtWidgets.QWidget(parent=DirSettingDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 381, 301))
        self.layoutWidget.setObjectName("layoutWidget")
        self.DirInputLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.DirInputLayout.setContentsMargins(0, 0, 0, 0)
        self.DirInputLayout.setSpacing(40)
        self.DirInputLayout.setObjectName("DirInputLayout")
        self.dataInputLayout = QtWidgets.QVBoxLayout()
        self.dataInputLayout.setSpacing(20)
        self.dataInputLayout.setObjectName("dataInputLayout")
        self.dataDirLabel = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.dataDirLabel.setFont(font)
        self.dataDirLabel.setObjectName("dataDirLabel")
        self.dataInputLayout.addWidget(self.dataDirLabel)
        self.dataDirInputLayout = QtWidgets.QHBoxLayout()
        self.dataDirInputLayout.setSpacing(7)
        self.dataDirInputLayout.setObjectName("dataDirInputLayout")
        self.dataDirLineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dataDirLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.dataDirLineEdit.setSizePolicy(sizePolicy)
        self.dataDirLineEdit.setMinimumSize(QtCore.QSize(350, 30))
        self.dataDirLineEdit.setMaximumSize(QtCore.QSize(350, 16777215))
        self.dataDirLineEdit.setObjectName("dataDirLineEdit")
        self.dataDirInputLayout.addWidget(self.dataDirLineEdit)
        self.dataDirInputButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dataDirInputButton.sizePolicy().hasHeightForWidth()
        )
        self.dataDirInputButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.dataDirInputButton.setFont(font)
        self.dataDirInputButton.setObjectName("dataDirInputButton")
        self.dataDirInputLayout.addWidget(self.dataDirInputButton)
        self.dataInputLayout.addLayout(self.dataDirInputLayout)
        self.DirInputLayout.addLayout(self.dataInputLayout)
        self.DRTDataInputLayout = QtWidgets.QVBoxLayout()
        self.DRTDataInputLayout.setSpacing(20)
        self.DRTDataInputLayout.setObjectName("DRTDataInputLayout")
        self.DRTDataDirLabel = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.DRTDataDirLabel.setFont(font)
        self.DRTDataDirLabel.setObjectName("DRTDataDirLabel")
        self.DRTDataInputLayout.addWidget(self.DRTDataDirLabel)
        self.DRTDataDirInputLayout = QtWidgets.QHBoxLayout()
        self.DRTDataDirInputLayout.setSpacing(7)
        self.DRTDataDirInputLayout.setObjectName("DRTDataDirInputLayout")
        self.DRTDataDirLineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.DRTDataDirLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.DRTDataDirLineEdit.setSizePolicy(sizePolicy)
        self.DRTDataDirLineEdit.setMinimumSize(QtCore.QSize(350, 30))
        self.DRTDataDirLineEdit.setMaximumSize(QtCore.QSize(350, 16777215))
        self.DRTDataDirLineEdit.setObjectName("DRTDataDirLineEdit")
        self.DRTDataDirInputLayout.addWidget(self.DRTDataDirLineEdit)
        self.DRTDataDirInputButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.DRTDataDirInputButton.sizePolicy().hasHeightForWidth()
        )
        self.DRTDataDirInputButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.DRTDataDirInputButton.setFont(font)
        self.DRTDataDirInputButton.setObjectName("DRTDataDirInputButton")
        self.DRTDataDirInputLayout.addWidget(self.DRTDataDirInputButton)
        self.DRTDataInputLayout.addLayout(self.DRTDataDirInputLayout)
        self.DirInputLayout.addLayout(self.DRTDataInputLayout)
        self.resultInputLayout = QtWidgets.QVBoxLayout()
        self.resultInputLayout.setSpacing(20)
        self.resultInputLayout.setObjectName("resultInputLayout")
        self.resultDirLabel = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.resultDirLabel.setFont(font)
        self.resultDirLabel.setObjectName("resultDirLabel")
        self.resultInputLayout.addWidget(self.resultDirLabel)
        self.resultDirInputLayout = QtWidgets.QHBoxLayout()
        self.resultDirInputLayout.setSpacing(7)
        self.resultDirInputLayout.setObjectName("resultDirInputLayout")
        self.resultDirLineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.resultDirLineEdit.sizePolicy().hasHeightForWidth()
        )
        self.resultDirLineEdit.setSizePolicy(sizePolicy)
        self.resultDirLineEdit.setMinimumSize(QtCore.QSize(350, 30))
        self.resultDirLineEdit.setMaximumSize(QtCore.QSize(350, 16777215))
        self.resultDirLineEdit.setObjectName("resultDirLineEdit")
        self.resultDirInputLayout.addWidget(self.resultDirLineEdit)
        self.resultDirInputButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.resultDirInputButton.sizePolicy().hasHeightForWidth()
        )
        self.resultDirInputButton.setSizePolicy(sizePolicy)
        self.resultDirInputButton.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.resultDirInputButton.setFont(font)
        self.resultDirInputButton.setObjectName("resultDirInputButton")
        self.resultDirInputLayout.addWidget(self.resultDirInputButton)
        self.resultInputLayout.addLayout(self.resultDirInputLayout)
        self.DirInputLayout.addLayout(self.resultInputLayout)
        self.layoutWidget1 = QtWidgets.QWidget(parent=DirSettingDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(160, 330, 231, 41))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.bottomButtons = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.bottomButtons.setContentsMargins(0, 0, 0, 0)
        self.bottomButtons.setObjectName("bottomButtons")
        self.saveButton = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.saveButton.setObjectName("saveButton")
        self.bottomButtons.addWidget(self.saveButton)
        self.cancelButton = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.cancelButton.setObjectName("cancelButton")
        self.bottomButtons.addWidget(self.cancelButton)

        self.retranslateUi(DirSettingDialog)
        self.dataDirInputButton.clicked.connect(DirSettingDialog.inputDataDir)  # type: ignore
        self.DRTDataDirInputButton.clicked.connect(DirSettingDialog.inputDRTDataDir)  # type: ignore
        self.resultDirInputButton.clicked.connect(DirSettingDialog.inputResultDir)  # type: ignore
        self.saveButton.clicked.connect(DirSettingDialog.saveDirs)  # type: ignore
        self.cancelButton.clicked.connect(DirSettingDialog.close)  # type: ignore
        self.dataDirLineEdit.editingFinished.connect(DirSettingDialog.readLineEdits)  # type: ignore
        self.DRTDataDirLineEdit.editingFinished.connect(DirSettingDialog.readLineEdits)  # type: ignore
        self.resultDirLineEdit.editingFinished.connect(DirSettingDialog.readLineEdits)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DirSettingDialog)
        DirSettingDialog.setTabOrder(self.dataDirLineEdit, self.dataDirInputButton)
        DirSettingDialog.setTabOrder(self.dataDirInputButton, self.DRTDataDirLineEdit)
        DirSettingDialog.setTabOrder(
            self.DRTDataDirLineEdit, self.DRTDataDirInputButton
        )
        DirSettingDialog.setTabOrder(self.DRTDataDirInputButton, self.resultDirLineEdit)
        DirSettingDialog.setTabOrder(self.resultDirLineEdit, self.resultDirInputButton)
        DirSettingDialog.setTabOrder(self.resultDirInputButton, self.saveButton)
        DirSettingDialog.setTabOrder(self.saveButton, self.cancelButton)

    def retranslateUi(self, DirSettingDialog):
        _translate = QtCore.QCoreApplication.translate
        DirSettingDialog.setWindowTitle(_translate("DirSettingDialog", "路径设置"))
        self.dataDirLabel.setText(_translate("DirSettingDialog", "实验数据路径："))
        self.dataDirInputButton.setText(_translate("DirSettingDialog", ".\n" ".\n" "."))
        self.DRTDataDirLabel.setText(_translate("DirSettingDialog", "DRT数据路径："))
        self.DRTDataDirInputButton.setText(
            _translate("DirSettingDialog", ".\n" ".\n" ".")
        )
        self.resultDirLabel.setText(_translate("DirSettingDialog", "程序输出路径："))
        self.resultDirInputButton.setText(
            _translate("DirSettingDialog", ".\n" ".\n" ".")
        )
        self.saveButton.setText(_translate("DirSettingDialog", "保存配置"))
        self.cancelButton.setText(_translate("DirSettingDialog", "返回"))

    def setupComponents(self):
        self.readDirs()

    def updateDirTexts(self):
        dataDir, DRTDataDir, resultDir = self.dirs.values()

        self.dataDirLineEdit.setText(dataDir)
        self.DRTDataDirLineEdit.setText(DRTDataDir)
        self.resultDirLineEdit.setText(resultDir)

    def emitDirs(self):
        self.dirSignal.emit(self.dirs)
        # print("Dirs Emitted!")

    def readDirs(self):
        config = configparser.ConfigParser()
        config.read(self.configFilePath)

        if (self.sectionName in config.sections()) and (
            len(config[self.sectionName]) != 0
        ):
            for key in self.dirs.keys():
                self.dirs[key] = config[self.sectionName][key]

            self.updateDirTexts()

    def saveDirs(self):
        self.emitDirs()
        self.close()

    def inputDir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "./")
        return directory

    def inputDataDir(self):
        self.dirs["Data Dir"] = self.inputDir()
        self.dataDirLineEdit.setText(self.dirs["Data Dir"])

    def inputDRTDataDir(self):
        self.dirs["DRT Data Dir"] = self.inputDir()
        self.DRTDataDirLineEdit.setText(self.dirs["DRT Data Dir"])

    def inputResultDir(self):
        self.dirs["Result Dir"] = self.inputDir()
        self.resultDirLineEdit.setText(self.dirs["Result Dir"])

    def readLineEdits(self):
        self.dirs["Data Dir"] = self.dataDirLineEdit.text()
        self.dirs["DRT Data Dir"] = self.DRTDataDirLineEdit.text()
        self.dirs["Result Dir"] = self.resultDirLineEdit.text()
        self.dirs["DRT Tool Dir"] = self.DRTToolDirLineEdit.text()


class DirSettingDialog(QtWidgets.QDialog, DirSettingDialog):
    def __init__(self):
        super(DirSettingDialog, self).__init__()
        self.setupUi(self)
