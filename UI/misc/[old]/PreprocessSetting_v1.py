import configparser

from PyQt6 import QtCore, QtGui, QtWidgets

configsDir = QtCore.QDir.currentPath() + r"/configs/"
configFileName = "Preprocess Setting.ini"
configFilePath = configsDir + configFileName


class PreprocessSettingDialog(object):
    invaildRead = False

    preprocessorSwitch = []
    filterOptions = []
    cutofferOptions = []
    interpModes = ["10^x"]
    interpolaterOptions = []
    smootherOptions = []
    downSamplerOptions = []
    preprocessorInfo = []

    preprocessorInfoSignal = QtCore.pyqtSignal(list)

    def setupUi(self, PreprocessSettingDialog):
        PreprocessSettingDialog.setObjectName("PreprocessSettingDialog")
        PreprocessSettingDialog.resize(540, 480)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            PreprocessSettingDialog.sizePolicy().hasHeightForWidth()
        )
        PreprocessSettingDialog.setSizePolicy(sizePolicy)
        self.layoutWidget = QtWidgets.QWidget(parent=PreprocessSettingDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 521, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.preprocessSwitchLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.preprocessSwitchLayout.setContentsMargins(0, 0, 0, 0)
        self.preprocessSwitchLayout.setSpacing(0)
        self.preprocessSwitchLayout.setObjectName("preprocessSwitchLayout")
        self.staticLabel1 = QtWidgets.QLabel(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticLabel1.sizePolicy().hasHeightForWidth())
        self.staticLabel1.setSizePolicy(sizePolicy)
        self.staticLabel1.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.staticLabel1.setFont(font)
        self.staticLabel1.setObjectName("staticLabel1")
        self.preprocessSwitchLayout.addWidget(self.staticLabel1)
        self.preprocessSwitchTable = QtWidgets.QTableWidget(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.preprocessSwitchTable.sizePolicy().hasHeightForWidth()
        )
        self.preprocessSwitchTable.setSizePolicy(sizePolicy)
        self.preprocessSwitchTable.setMaximumSize(QtCore.QSize(16777215, 60))
        self.preprocessSwitchTable.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.preprocessSwitchTable.setObjectName("preprocessSwitchTable")
        self.preprocessSwitchTable.setColumnCount(5)
        self.preprocessSwitchTable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preprocessSwitchTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.preprocessSwitchTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.preprocessSwitchTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.preprocessSwitchTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.preprocessSwitchTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.preprocessSwitchTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preprocessSwitchTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preprocessSwitchTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preprocessSwitchTable.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preprocessSwitchTable.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preprocessSwitchTable.setItem(0, 4, item)
        self.preprocessSwitchTable.horizontalHeader().setDefaultSectionSize(95)
        self.preprocessSwitchTable.horizontalHeader().setMinimumSectionSize(31)
        self.preprocessSwitchTable.verticalHeader().setDefaultSectionSize(30)
        self.preprocessSwitchLayout.addWidget(self.preprocessSwitchTable)
        self.layoutWidget1 = QtWidgets.QWidget(parent=PreprocessSettingDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 102, 521, 361))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.OptionsLayout = QtWidgets.QFormLayout(self.layoutWidget1)
        self.OptionsLayout.setContentsMargins(0, 0, 0, 0)
        self.OptionsLayout.setSpacing(10)
        self.OptionsLayout.setObjectName("OptionsLayout")
        self.filterOptionsLayout = QtWidgets.QVBoxLayout()
        self.filterOptionsLayout.setSpacing(0)
        self.filterOptionsLayout.setObjectName("filterOptionsLayout")
        self.staticLabel2 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticLabel2.sizePolicy().hasHeightForWidth())
        self.staticLabel2.setSizePolicy(sizePolicy)
        self.staticLabel2.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.staticLabel2.setFont(font)
        self.staticLabel2.setObjectName("staticLabel2")
        self.filterOptionsLayout.addWidget(self.staticLabel2)
        self.filterOptionsTable = QtWidgets.QTableWidget(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filterOptionsTable.sizePolicy().hasHeightForWidth()
        )
        self.filterOptionsTable.setSizePolicy(sizePolicy)
        self.filterOptionsTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.filterOptionsTable.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.filterOptionsTable.setObjectName("filterOptionsTable")
        self.filterOptionsTable.setColumnCount(1)
        self.filterOptionsTable.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filterOptionsTable.setItem(4, 0, item)
        self.filterOptionsTable.horizontalHeader().setDefaultSectionSize(100)
        self.filterOptionsTable.horizontalHeader().setMinimumSectionSize(31)
        self.filterOptionsTable.verticalHeader().setDefaultSectionSize(30)
        self.filterOptionsLayout.addWidget(self.filterOptionsTable)
        self.OptionsLayout.setLayout(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.filterOptionsLayout
        )
        self.cutofferOptionsLayout = QtWidgets.QVBoxLayout()
        self.cutofferOptionsLayout.setSpacing(0)
        self.cutofferOptionsLayout.setObjectName("cutofferOptionsLayout")
        self.staticLabel3 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticLabel3.sizePolicy().hasHeightForWidth())
        self.staticLabel3.setSizePolicy(sizePolicy)
        self.staticLabel3.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.staticLabel3.setFont(font)
        self.staticLabel3.setObjectName("staticLabel3")
        self.cutofferOptionsLayout.addWidget(self.staticLabel3)
        self.cutofferOptionsTable = QtWidgets.QTableWidget(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cutofferOptionsTable.sizePolicy().hasHeightForWidth()
        )
        self.cutofferOptionsTable.setSizePolicy(sizePolicy)
        self.cutofferOptionsTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cutofferOptionsTable.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.cutofferOptionsTable.setObjectName("cutofferOptionsTable")
        self.cutofferOptionsTable.setColumnCount(1)
        self.cutofferOptionsTable.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.cutofferOptionsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cutofferOptionsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.cutofferOptionsTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.cutofferOptionsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cutofferOptionsTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cutofferOptionsTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cutofferOptionsTable.setItem(2, 0, item)
        self.cutofferOptionsTable.horizontalHeader().setDefaultSectionSize(100)
        self.cutofferOptionsTable.horizontalHeader().setMinimumSectionSize(31)
        self.cutofferOptionsTable.verticalHeader().setDefaultSectionSize(30)
        self.cutofferOptionsLayout.addWidget(self.cutofferOptionsTable)
        self.OptionsLayout.setLayout(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cutofferOptionsLayout
        )
        self.interpolaterOptionsLayout = QtWidgets.QVBoxLayout()
        self.interpolaterOptionsLayout.setSpacing(0)
        self.interpolaterOptionsLayout.setObjectName("interpolaterOptionsLayout")
        self.staticLabel4 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticLabel4.sizePolicy().hasHeightForWidth())
        self.staticLabel4.setSizePolicy(sizePolicy)
        self.staticLabel4.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.staticLabel4.setFont(font)
        self.staticLabel4.setObjectName("staticLabel4")
        self.interpolaterOptionsLayout.addWidget(self.staticLabel4)
        self.interpolaterOptionsTable = QtWidgets.QTableWidget(
            parent=self.layoutWidget1
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.interpolaterOptionsTable.sizePolicy().hasHeightForWidth()
        )
        self.interpolaterOptionsTable.setSizePolicy(sizePolicy)
        self.interpolaterOptionsTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.interpolaterOptionsTable.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.interpolaterOptionsTable.setObjectName("interpolaterOptionsTable")
        self.interpolaterOptionsTable.setColumnCount(1)
        self.interpolaterOptionsTable.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.interpolaterOptionsTable.setItem(3, 0, item)
        self.interpolaterOptionsTable.horizontalHeader().setDefaultSectionSize(100)
        self.interpolaterOptionsTable.horizontalHeader().setMinimumSectionSize(31)
        self.interpolaterOptionsTable.verticalHeader().setDefaultSectionSize(30)
        self.interpolaterOptionsLayout.addWidget(self.interpolaterOptionsTable)
        self.OptionsLayout.setLayout(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.interpolaterOptionsLayout
        )
        self.smootherOptionsLayout = QtWidgets.QVBoxLayout()
        self.smootherOptionsLayout.setSpacing(0)
        self.smootherOptionsLayout.setObjectName("smootherOptionsLayout")
        self.staticLabel5 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticLabel5.sizePolicy().hasHeightForWidth())
        self.staticLabel5.setSizePolicy(sizePolicy)
        self.staticLabel5.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.staticLabel5.setFont(font)
        self.staticLabel5.setObjectName("staticLabel5")
        self.smootherOptionsLayout.addWidget(self.staticLabel5)
        self.smootherOptionsTable = QtWidgets.QTableWidget(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.smootherOptionsTable.sizePolicy().hasHeightForWidth()
        )
        self.smootherOptionsTable.setSizePolicy(sizePolicy)
        self.smootherOptionsTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.smootherOptionsTable.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.smootherOptionsTable.setObjectName("smootherOptionsTable")
        self.smootherOptionsTable.setColumnCount(1)
        self.smootherOptionsTable.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.smootherOptionsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.smootherOptionsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.smootherOptionsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.smootherOptionsTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.smootherOptionsTable.setItem(1, 0, item)
        self.smootherOptionsTable.horizontalHeader().setDefaultSectionSize(100)
        self.smootherOptionsTable.horizontalHeader().setMinimumSectionSize(31)
        self.smootherOptionsTable.verticalHeader().setDefaultSectionSize(30)
        self.smootherOptionsLayout.addWidget(self.smootherOptionsTable)
        self.OptionsLayout.setLayout(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.smootherOptionsLayout
        )
        self.downsamplerOptionsLayout = QtWidgets.QVBoxLayout()
        self.downsamplerOptionsLayout.setSpacing(0)
        self.downsamplerOptionsLayout.setObjectName("downsamplerOptionsLayout")
        self.staticLabel6 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticLabel6.sizePolicy().hasHeightForWidth())
        self.staticLabel6.setSizePolicy(sizePolicy)
        self.staticLabel6.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.staticLabel6.setFont(font)
        self.staticLabel6.setObjectName("staticLabel6")
        self.downsamplerOptionsLayout.addWidget(self.staticLabel6)
        self.downsamplerOptionsTable = QtWidgets.QTableWidget(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.downsamplerOptionsTable.sizePolicy().hasHeightForWidth()
        )
        self.downsamplerOptionsTable.setSizePolicy(sizePolicy)
        self.downsamplerOptionsTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.downsamplerOptionsTable.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.downsamplerOptionsTable.setObjectName("downsamplerOptionsTable")
        self.downsamplerOptionsTable.setColumnCount(1)
        self.downsamplerOptionsTable.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.downsamplerOptionsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsamplerOptionsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.downsamplerOptionsTable.setItem(0, 0, item)
        self.downsamplerOptionsTable.horizontalHeader().setDefaultSectionSize(100)
        self.downsamplerOptionsTable.horizontalHeader().setMinimumSectionSize(31)
        self.downsamplerOptionsTable.verticalHeader().setDefaultSectionSize(30)
        self.downsamplerOptionsLayout.addWidget(self.downsamplerOptionsTable)
        self.OptionsLayout.setLayout(
            2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.downsamplerOptionsLayout
        )
        self.bottomButtonsLayout = QtWidgets.QVBoxLayout()
        self.bottomButtonsLayout.setObjectName("bottomButtonsLayout")
        self.spacer = QtWidgets.QFrame(parent=self.layoutWidget1)
        self.spacer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.spacer.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.spacer.setObjectName("spacer")
        self.bottomButtonsLayout.addWidget(self.spacer)
        self.bottomButtonFrame = QtWidgets.QFrame(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bottomButtonFrame.sizePolicy().hasHeightForWidth()
        )
        self.bottomButtonFrame.setSizePolicy(sizePolicy)
        self.bottomButtonFrame.setObjectName("bottomButtonFrame")
        self.bottomButtons = QtWidgets.QHBoxLayout(self.bottomButtonFrame)
        self.bottomButtons.setObjectName("bottomButtons")
        self.saveButton = QtWidgets.QPushButton(parent=self.bottomButtonFrame)
        self.saveButton.setObjectName("saveButton")
        self.bottomButtons.addWidget(self.saveButton)
        self.cancelButton = QtWidgets.QPushButton(parent=self.bottomButtonFrame)
        self.cancelButton.setObjectName("cancelButton")
        self.bottomButtons.addWidget(self.cancelButton)
        self.bottomButtonsLayout.addWidget(self.bottomButtonFrame)
        self.OptionsLayout.setLayout(
            2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.bottomButtonsLayout
        )

        self.retranslateUi(PreprocessSettingDialog)
        self.saveButton.clicked.connect(PreprocessSettingDialog.saveOptions)  # type: ignore
        self.cancelButton.clicked.connect(PreprocessSettingDialog.close)  # type: ignore
        self.preprocessSwitchTable.clicked["QModelIndex"].connect(PreprocessSettingDialog.updateEnableStates)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(PreprocessSettingDialog)
        PreprocessSettingDialog.setTabOrder(
            self.preprocessSwitchTable, self.filterOptionsTable
        )
        PreprocessSettingDialog.setTabOrder(
            self.filterOptionsTable, self.cutofferOptionsTable
        )
        PreprocessSettingDialog.setTabOrder(
            self.cutofferOptionsTable, self.interpolaterOptionsTable
        )
        PreprocessSettingDialog.setTabOrder(
            self.interpolaterOptionsTable, self.smootherOptionsTable
        )
        PreprocessSettingDialog.setTabOrder(
            self.smootherOptionsTable, self.downsamplerOptionsTable
        )
        PreprocessSettingDialog.setTabOrder(
            self.downsamplerOptionsTable, self.saveButton
        )
        PreprocessSettingDialog.setTabOrder(self.saveButton, self.cancelButton)

    def retranslateUi(self, PreprocessSettingDialog):
        _translate = QtCore.QCoreApplication.translate
        PreprocessSettingDialog.setWindowTitle(
            _translate("PreprocessSettingDialog", "程序设置")
        )
        self.staticLabel1.setText(_translate("PreprocessSettingDialog", "总开关："))
        item = self.preprocessSwitchTable.verticalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "开关"))
        item = self.preprocessSwitchTable.horizontalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "过滤器"))
        item = self.preprocessSwitchTable.horizontalHeaderItem(1)
        item.setText(_translate("PreprocessSettingDialog", "截断器"))
        item = self.preprocessSwitchTable.horizontalHeaderItem(2)
        item.setText(_translate("PreprocessSettingDialog", "插值器"))
        item = self.preprocessSwitchTable.horizontalHeaderItem(3)
        item.setText(_translate("PreprocessSettingDialog", "平滑器"))
        item = self.preprocessSwitchTable.horizontalHeaderItem(4)
        item.setText(_translate("PreprocessSettingDialog", "降采样器"))
        __sortingEnabled = self.preprocessSwitchTable.isSortingEnabled()
        self.preprocessSwitchTable.setSortingEnabled(False)
        self.preprocessSwitchTable.setSortingEnabled(__sortingEnabled)
        self.staticLabel2.setText(_translate("PreprocessSettingDialog", "过滤器选项："))
        item = self.filterOptionsTable.verticalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "内核(滑动窗口)大小"))
        item = self.filterOptionsTable.verticalHeaderItem(1)
        item.setText(_translate("PreprocessSettingDialog", "标准差阈值"))
        item = self.filterOptionsTable.verticalHeaderItem(2)
        item.setText(_translate("PreprocessSettingDialog", "导数标准差阈值"))
        item = self.filterOptionsTable.verticalHeaderItem(3)
        item.setText(_translate("PreprocessSettingDialog", "过滤次数"))
        item = self.filterOptionsTable.verticalHeaderItem(4)
        item.setText(_translate("PreprocessSettingDialog", "删除虚部小于0的点"))
        item = self.filterOptionsTable.horizontalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "值"))
        __sortingEnabled = self.filterOptionsTable.isSortingEnabled()
        self.filterOptionsTable.setSortingEnabled(False)
        item = self.filterOptionsTable.item(0, 0)
        item.setText(_translate("PreprocessSettingDialog", "5"))
        item = self.filterOptionsTable.item(1, 0)
        item.setText(_translate("PreprocessSettingDialog", "1"))
        item = self.filterOptionsTable.item(2, 0)
        item.setText(_translate("PreprocessSettingDialog", "1"))
        item = self.filterOptionsTable.item(3, 0)
        item.setText(_translate("PreprocessSettingDialog", "-1"))
        self.filterOptionsTable.setSortingEnabled(__sortingEnabled)
        self.staticLabel3.setText(_translate("PreprocessSettingDialog", "截断器选项："))
        item = self.cutofferOptionsTable.verticalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "截断距离"))
        item = self.cutofferOptionsTable.verticalHeaderItem(1)
        item.setText(_translate("PreprocessSettingDialog", "截断左端点"))
        item = self.cutofferOptionsTable.verticalHeaderItem(2)
        item.setText(_translate("PreprocessSettingDialog", "截断右端点"))
        item = self.cutofferOptionsTable.horizontalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "值"))
        __sortingEnabled = self.cutofferOptionsTable.isSortingEnabled()
        self.cutofferOptionsTable.setSortingEnabled(False)
        item = self.cutofferOptionsTable.item(0, 0)
        item.setText(_translate("PreprocessSettingDialog", "0.2"))
        item = self.cutofferOptionsTable.item(1, 0)
        item.setText(_translate("PreprocessSettingDialog", "0.1"))
        item = self.cutofferOptionsTable.item(2, 0)
        item.setText(_translate("PreprocessSettingDialog", "0.9"))
        self.cutofferOptionsTable.setSortingEnabled(__sortingEnabled)
        self.staticLabel4.setText(_translate("PreprocessSettingDialog", "插值器选项："))
        item = self.interpolaterOptionsTable.verticalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "插值公式"))
        item = self.interpolaterOptionsTable.verticalHeaderItem(1)
        item.setText(_translate("PreprocessSettingDialog", "f起点"))
        item = self.interpolaterOptionsTable.verticalHeaderItem(2)
        item.setText(_translate("PreprocessSettingDialog", "f终点"))
        item = self.interpolaterOptionsTable.verticalHeaderItem(3)
        item.setText(_translate("PreprocessSettingDialog", "点个数"))
        item = self.interpolaterOptionsTable.horizontalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "值"))
        __sortingEnabled = self.interpolaterOptionsTable.isSortingEnabled()
        self.interpolaterOptionsTable.setSortingEnabled(False)
        item = self.interpolaterOptionsTable.item(1, 0)
        item.setText(_translate("PreprocessSettingDialog", "0.6"))
        item = self.interpolaterOptionsTable.item(2, 0)
        item.setText(_translate("PreprocessSettingDialog", "4.5"))
        item = self.interpolaterOptionsTable.item(3, 0)
        item.setText(_translate("PreprocessSettingDialog", "100"))
        self.interpolaterOptionsTable.setSortingEnabled(__sortingEnabled)
        self.staticLabel5.setText(_translate("PreprocessSettingDialog", "平滑器选项："))
        item = self.smootherOptionsTable.verticalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "内核(滑动窗口)大小"))
        item = self.smootherOptionsTable.verticalHeaderItem(1)
        item.setText(_translate("PreprocessSettingDialog", "多项式阶数"))
        item = self.smootherOptionsTable.horizontalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "值"))
        __sortingEnabled = self.smootherOptionsTable.isSortingEnabled()
        self.smootherOptionsTable.setSortingEnabled(False)
        item = self.smootherOptionsTable.item(0, 0)
        item.setText(_translate("PreprocessSettingDialog", "4"))
        item = self.smootherOptionsTable.item(1, 0)
        item.setText(_translate("PreprocessSettingDialog", "3"))
        self.smootherOptionsTable.setSortingEnabled(__sortingEnabled)
        self.staticLabel6.setText(
            _translate("PreprocessSettingDialog", "降采样器选项：")
        )
        item = self.downsamplerOptionsTable.verticalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "融合距离"))
        item = self.downsamplerOptionsTable.horizontalHeaderItem(0)
        item.setText(_translate("PreprocessSettingDialog", "值"))
        __sortingEnabled = self.downsamplerOptionsTable.isSortingEnabled()
        self.downsamplerOptionsTable.setSortingEnabled(False)
        item = self.downsamplerOptionsTable.item(0, 0)
        item.setText(_translate("PreprocessSettingDialog", "0.01"))
        self.downsamplerOptionsTable.setSortingEnabled(__sortingEnabled)
        self.saveButton.setText(_translate("PreprocessSettingDialog", "保存配置"))
        self.cancelButton.setText(_translate("PreprocessSettingDialog", "返回"))

    def setupComponents(self):
        self.initalizeTables()
        self.updateEnableStates()

    def emitPreprocessorInfo(self):
        # print("Info emitted!")
        self.preprocessorInfoSignal.emit(self.preprocessorInfo)

    def readPreprocessorInfo(self):
        config = configparser.ConfigParser()
        config.read(configFilePath)

        if len(config.sections()) != 0:
            self.preprocessorSwitch = config["Preprocessor Info"][
                "Preprocessor Switch"
            ].split(",")
            self.filterOptions = config["Preprocessor Info"]["Filter Options"].split(
                ","
            )
            self.cutofferOptions = config["Preprocessor Info"][
                "Cutoffer Options"
            ].split(",")
            self.interpolaterOptions = config["Preprocessor Info"][
                "Interpolater Options"
            ].split(",")
            self.smootherOptions = config["Preprocessor Info"][
                "Smoother Options"
            ].split(",")
            self.downSamplerOptions = config["Preprocessor Info"][
                "DownSampler Options"
            ].split(",")

            self.changeOptionsFormat()
        else:
            self.invaildRead = True

    def writePreprocessorInfo(self):
        splitText = ","
        preprocessorSwitchText = splitText.join(
            [str(item) for item in self.preprocessorSwitch]
        )
        filterOptionsText = splitText.join([str(item) for item in self.filterOptions])
        cutofferList = [self.cutofferOptions[0]] + list(self.cutofferOptions[1])
        cutofferOptionsText = splitText.join([str(item) for item in cutofferList])
        interpolaterOptionsText = splitText.join(
            [str(item) for item in self.interpolaterOptions]
        )
        smootherOptionsText = splitText.join(
            [str(item) for item in self.smootherOptions]
        )
        downsamplerOptionsText = splitText.join(
            [str(item) for item in self.downSamplerOptions]
        )

        config = configparser.ConfigParser()
        config["Preprocessor Info"] = {
            "Preprocessor Switch": preprocessorSwitchText,
            "Filter Options": filterOptionsText,
            "Cutoffer Options": cutofferOptionsText,
            "Interpolater Options": interpolaterOptionsText,
            "Smoother Options": smootherOptionsText,
            "DownSampler Options": downsamplerOptionsText,
        }
        with open(configFilePath, "w") as configfile:
            config.write(configfile)

    def initalizeTables(self):
        self.readPreprocessorInfo()

        # Preprocess Switch
        empty = len(self.preprocessorSwitch) == 0
        isEnable = [False for i in range(5)] if empty else self.preprocessorSwitch
        for col in range(5):
            checkbox = QtWidgets.QCheckBox()
            self.preprocessSwitchTable.setCellWidget(0, col, checkbox)
            checkbox.setChecked(isEnable[col])
            checkbox.clicked.connect(self.updateEnableStates)

        # Filter
        empty = len(self.filterOptions) == 0
        filterInit = [5, 1, 1, -1] if empty else self.filterOptions[:-1]
        for row, val in enumerate(filterInit):
            valItem = QtWidgets.QTableWidgetItem(str(val))
            self.filterOptionsTable.setItem(row, 0, valItem)

        checkbox = QtWidgets.QCheckBox()
        self.filterOptionsTable.setCellWidget(4, 0, checkbox)
        checkbox.setChecked(False if empty else self.filterOptions[-1])

        # Cutoffer
        empty = len(self.cutofferOptions) == 0
        cutofferInit = (
            [0.2, 0.1, 0.9]
            if empty
            else [self.cutofferOptions[0]] + list(self.cutofferOptions[1])
        )
        for row, val in enumerate(cutofferInit):
            valItem = QtWidgets.QTableWidgetItem(str(val))
            self.cutofferOptionsTable.setItem(row, 0, valItem)

        # Interpolater
        empty = len(self.interpolaterOptions) == 0
        combobox = QtWidgets.QComboBox()
        combobox.addItems(self.interpModes)
        combobox.setCurrentText("10^x" if empty else self.interpolaterOptions[0])
        self.interpolaterOptionsTable.setCellWidget(0, 0, combobox)

        interpolaterInit = [0.6, 4.5, 100] if empty else self.interpolaterOptions[1:]
        for row, val in enumerate(interpolaterInit):
            valItem = QtWidgets.QTableWidgetItem(str(val))
            self.interpolaterOptionsTable.setItem(row + 1, 0, valItem)

        # Smoother
        empty = len(self.smootherOptions) == 0
        smootherInit = [4, 3] if empty else self.smootherOptions
        for row, val in enumerate(smootherInit):
            valItem = QtWidgets.QTableWidgetItem(str(val))
            self.smootherOptionsTable.setItem(row, 0, valItem)

        # Downsampler
        empty = len(self.downSamplerOptions) == 0
        downsamplerInit = [0.01] if empty else self.downSamplerOptions
        for row, val in enumerate(downsamplerInit):
            valItem = QtWidgets.QTableWidgetItem(str(val))
            self.downsamplerOptionsTable.setItem(row, 0, valItem)

        if self.invaildRead:
            self.saveOptions()

    def readPreprocessSwitch(self):
        preprocessorSwitch = []
        for col in range(5):
            checkbox = self.preprocessSwitchTable.cellWidget(0, col)
            preprocessorSwitch.append(checkbox.isChecked())
        self.preprocessorSwitch = preprocessorSwitch

    def convertTextList(
        self,
        textList: list,
        ints: list[int] = [],
        floats: list[int] = [],
        bools: list[int] = [],
    ) -> list:
        for i in range(len(textList)):
            if i in ints:
                textList[i] = int(textList[i])
            elif i in floats:
                textList[i] = float(textList[i])
            elif i in bools:
                textList[i] = textList[i] == "True"

        return textList

    def changeOptionsFormat(self):
        # Preprocess Switch
        bools = [i for i in range(5)]
        textList = self.preprocessorSwitch
        self.preprocessorSwitch = self.convertTextList(textList=textList, bools=bools)

        # Filter
        ints = [0, 3]
        floats = [1, 2]
        bools = [4]
        self.filterOptions = self.convertTextList(
            self.filterOptions, ints=ints, floats=floats, bools=bools
        )

        # Cutoffer
        floats = [i for i in range(3)]
        self.cutofferOptions = self.convertTextList(self.cutofferOptions, floats=floats)

        cutSection = (self.cutofferOptions[1], self.cutofferOptions[2])
        self.cutofferOptions = [self.cutofferOptions[0], cutSection]

        # Interpolater
        ints = [3]
        floats = [1, 2]
        self.interpolaterOptions = self.convertTextList(
            self.interpolaterOptions, ints=ints, floats=floats
        )

        # Smoother
        ints = [0, 1]
        self.smootherOptions = self.convertTextList(self.smootherOptions, ints=ints)

        # Downsampler
        floats = [0]
        self.downSamplerOptions = self.convertTextList(
            self.downSamplerOptions, floats=floats
        )

        # Preprocessor Info
        self.preprocessorInfo = [
            self.preprocessorSwitch,
            self.filterOptions,
            self.cutofferOptions,
            self.interpolaterOptions,
            self.smootherOptions,
            self.downSamplerOptions,
        ]

    def readUIOptions(self):
        # Preprocess Switch
        self.readPreprocessSwitch()

        # Filter
        filterOptions = []
        for row in range(4):
            item = self.filterOptionsTable.item(row, 0)
            filterOptions.append(item.text())
        checkbox = self.filterOptionsTable.cellWidget(4, 0)
        filterOptions.append(checkbox.isChecked())

        ints = [0, 3]
        floats = [1, 2]
        self.filterOptions = self.convertTextList(
            filterOptions, ints=ints, floats=floats
        )

        # Cutoffer
        cutofferOptions = []
        for row in range(3):
            item = self.cutofferOptionsTable.item(row, 0)
            cutofferOptions.append(item.text())

        floats = [i for i in range(3)]
        cutofferOptions = self.convertTextList(cutofferOptions, floats=floats)

        cutSection = (cutofferOptions[1], cutofferOptions[2])
        self.cutofferOptions = [cutofferOptions[0], cutSection]

        # Interpolater
        interpolaterOptions = []
        combobox = self.interpolaterOptionsTable.cellWidget(0, 0)
        interpolaterOptions.append(combobox.currentText())
        for row in range(3):
            item = self.interpolaterOptionsTable.item(row + 1, 0)
            interpolaterOptions.append(item.text())

        ints = [3]
        floats = [1, 2]
        self.interpolaterOptions = self.convertTextList(
            interpolaterOptions, ints=ints, floats=floats
        )

        # Smoother
        smootherOptions = []
        for row in range(2):
            item = self.smootherOptionsTable.item(row, 0)
            smootherOptions.append(item.text())

        ints = [0, 1]
        self.smootherOptions = self.convertTextList(smootherOptions, ints=ints)

        # Downsampler
        downSamplerOptions = []
        for row in range(1):
            item = self.downsamplerOptionsTable.item(row, 0)
            downSamplerOptions.append(item.text())

        floats = [0]
        self.downSamplerOptions = self.convertTextList(
            downSamplerOptions, floats=floats
        )

        # Preprocessor Info
        self.preprocessorInfo = [
            self.preprocessorSwitch,
            self.filterOptions,
            self.cutofferOptions,
            self.interpolaterOptions,
            self.smootherOptions,
            self.downSamplerOptions,
        ]

    def saveOptions(self):
        self.readUIOptions()
        self.writePreprocessorInfo()
        self.emitPreprocessorInfo()
        self.close()

    def updateEnableStates(self):
        self.readPreprocessSwitch()

        switches = self.preprocessorSwitch
        tables = [
            self.filterOptionsTable,
            self.cutofferOptionsTable,
            self.interpolaterOptionsTable,
            self.smootherOptionsTable,
            self.downsamplerOptionsTable,
        ]

        for i, isEnable in enumerate(switches):
            tables[i].setDisabled(not isEnable)


class PreprocessSettingDialog(QtWidgets.QDialog, PreprocessSettingDialog):
    def __init__(self):
        super(PreprocessSettingDialog, self).__init__()
        self.setupUi(self)
        self.setupComponents()
