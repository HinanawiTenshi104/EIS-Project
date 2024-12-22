import configparser

from PyQt6 import QtCore, QtGui, QtWidgets

from Modules import Circuit, Components

from .ChangeCircuitNameDialog import ChangeCircuitNameDialog

configsDir = QtCore.QDir.currentPath() + r"/configs/"
configFileName = "Model Settings.ini"
configFilePath = configsDir + configFileName
modelSettingsSectionName = "Model Settings"

circuitsDir = QtCore.QDir.currentPath() + r"/Modules/"
circuitFileName = "Circuits.ini"
circuitConfigPath = circuitsDir + circuitFileName
circuitInfoSplitText = ","


class ModelSettingsDialog(object):
    #
    modelSettings = {"Last Used Circuit Name": None}

    availableCircuitComponents = {}
    # [Section Name: circuitPrototype]
    circuitPrototypes: dict[str, Circuit.Circuit] = {}
    # [Display Name : Section Name]
    # Mainly For getCurrentCircuit
    circuitPrototypeSectionNames: dict[str, str] = {}

    dataNames: list[str] = []
    ringCounts: list[int] = []

    circuitIndex = 0
    circuits: list[Circuit.Circuit] = []
    circuitsSignal = QtCore.pyqtSignal(list)

    def setupUi(self, ModelSettings):
        ModelSettings.setObjectName("ModelSettings")
        ModelSettings.resize(800, 600)
        self.ModelSettingDataNameLabel = QtWidgets.QLabel(parent=ModelSettings)
        self.ModelSettingDataNameLabel.setGeometry(QtCore.QRect(10, 10, 291, 61))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.ModelSettingDataNameLabel.setFont(font)
        self.ModelSettingDataNameLabel.setScaledContents(True)
        self.ModelSettingDataNameLabel.setObjectName("ModelSettingDataNameLabel")
        self.ModelSettingFrame = QtWidgets.QFrame(parent=ModelSettings)
        self.ModelSettingFrame.setGeometry(QtCore.QRect(20, 80, 591, 451))
        self.ModelSettingFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ModelSettingFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.ModelSettingFrame.setObjectName("ModelSettingFrame")
        self.ModelSettingScrollArea = QtWidgets.QScrollArea(parent=ModelSettings)
        self.ModelSettingScrollArea.setGeometry(QtCore.QRect(620, 10, 171, 521))
        self.ModelSettingScrollArea.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.ModelSettingScrollArea.setWidgetResizable(True)
        self.ModelSettingScrollArea.setObjectName("ModelSettingScrollArea")
        self.ModelSettingScrollAreaContents = QtWidgets.QWidget()
        self.ModelSettingScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 169, 519))
        self.ModelSettingScrollAreaContents.setObjectName(
            "ModelSettingScrollAreaContents"
        )
        self.ModelSettingScrollArea.setWidget(self.ModelSettingScrollAreaContents)
        self.layoutWidget_5 = QtWidgets.QWidget(parent=ModelSettings)
        self.layoutWidget_5.setGeometry(QtCore.QRect(520, 530, 271, 61))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.ModelSettingBottomButtons = QtWidgets.QHBoxLayout(self.layoutWidget_5)
        self.ModelSettingBottomButtons.setContentsMargins(0, 0, 0, 0)
        self.ModelSettingBottomButtons.setObjectName("ModelSettingBottomButtons")
        self.ModelSettingBackButton = QtWidgets.QPushButton(parent=self.layoutWidget_5)
        self.ModelSettingBackButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ModelSettingBackButton.setObjectName("ModelSettingBackButton")
        self.ModelSettingBottomButtons.addWidget(self.ModelSettingBackButton)
        self.ModelSettingSaveButton = QtWidgets.QPushButton(parent=self.layoutWidget_5)
        self.ModelSettingSaveButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ModelSettingSaveButton.setObjectName("ModelSettingSaveButton")
        self.ModelSettingBottomButtons.addWidget(self.ModelSettingSaveButton)
        self.layoutWidget_6 = QtWidgets.QWidget(parent=ModelSettings)
        self.layoutWidget_6.setGeometry(QtCore.QRect(230, 540, 151, 32))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.ModelSettingSwitchDataButtons = QtWidgets.QHBoxLayout(self.layoutWidget_6)
        self.ModelSettingSwitchDataButtons.setContentsMargins(0, 0, 0, 0)
        self.ModelSettingSwitchDataButtons.setSpacing(0)
        self.ModelSettingSwitchDataButtons.setObjectName(
            "ModelSettingSwitchDataButtons"
        )
        self.ModelSettingPreviousDataButton = QtWidgets.QToolButton(
            parent=self.layoutWidget_6
        )
        self.ModelSettingPreviousDataButton.setMinimumSize(QtCore.QSize(30, 30))
        self.ModelSettingPreviousDataButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.ModelSettingPreviousDataButton.setText("")
        self.ModelSettingPreviousDataButton.setArrowType(QtCore.Qt.ArrowType.LeftArrow)
        self.ModelSettingPreviousDataButton.setObjectName(
            "ModelSettingPreviousDataButton"
        )
        self.ModelSettingSwitchDataButtons.addWidget(
            self.ModelSettingPreviousDataButton
        )
        self.staticLabel = QtWidgets.QLabel(parent=self.layoutWidget_6)
        self.staticLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staticLabel.setObjectName("staticLabel")
        self.ModelSettingSwitchDataButtons.addWidget(self.staticLabel)
        self.ModelSettingNextDataButton = QtWidgets.QToolButton(
            parent=self.layoutWidget_6
        )
        self.ModelSettingNextDataButton.setMinimumSize(QtCore.QSize(30, 30))
        self.ModelSettingNextDataButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.ModelSettingNextDataButton.setText("")
        self.ModelSettingNextDataButton.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        self.ModelSettingNextDataButton.setObjectName("ModelSettingNextDataButton")
        self.ModelSettingSwitchDataButtons.addWidget(self.ModelSettingNextDataButton)
        self.layoutWidget = QtWidgets.QWidget(parent=ModelSettings)
        self.layoutWidget.setGeometry(QtCore.QRect(320, 10, 291, 64))
        self.layoutWidget.setObjectName("layoutWidget")
        self.ModelSettingTopButtons = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.ModelSettingTopButtons.setContentsMargins(0, 0, 0, 0)
        self.ModelSettingTopButtons.setSpacing(3)
        self.ModelSettingTopButtons.setObjectName("ModelSettingTopButtons")
        self.ModelSettingTopLeftButtons = QtWidgets.QVBoxLayout()
        self.ModelSettingTopLeftButtons.setSpacing(0)
        self.ModelSettingTopLeftButtons.setObjectName("ModelSettingTopLeftButtons")
        self.ModelSettingChangeCircuitNameButton = QtWidgets.QPushButton(
            parent=self.layoutWidget
        )
        self.ModelSettingChangeCircuitNameButton.setMinimumSize(QtCore.QSize(50, 25))
        self.ModelSettingChangeCircuitNameButton.setObjectName(
            "ModelSettingChangeCircuitNameButton"
        )
        self.ModelSettingTopLeftButtons.addWidget(
            self.ModelSettingChangeCircuitNameButton
        )
        self.ModelSettingClearAllComponentsBotton = QtWidgets.QPushButton(
            parent=self.layoutWidget
        )
        self.ModelSettingClearAllComponentsBotton.setMinimumSize(QtCore.QSize(50, 25))
        self.ModelSettingClearAllComponentsBotton.setObjectName(
            "ModelSettingClearAllComponentsBotton"
        )
        self.ModelSettingTopLeftButtons.addWidget(
            self.ModelSettingClearAllComponentsBotton
        )
        self.ModelSettingTopButtons.addLayout(self.ModelSettingTopLeftButtons)
        self.ModelSettingTopRightLayout = QtWidgets.QVBoxLayout()
        self.ModelSettingTopRightLayout.setSpacing(0)
        self.ModelSettingTopRightLayout.setObjectName("ModelSettingTopRightLayout")
        self.ModelSettingDiagramComboBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.ModelSettingDiagramComboBox.setMinimumSize(QtCore.QSize(0, 24))
        self.ModelSettingDiagramComboBox.setObjectName("ModelSettingDiagramComboBox")
        self.ModelSettingTopRightLayout.addWidget(self.ModelSettingDiagramComboBox)
        self.ModelSettingTopBottomRightButtons = QtWidgets.QHBoxLayout()
        self.ModelSettingTopBottomRightButtons.setObjectName(
            "ModelSettingTopBottomRightButtons"
        )
        self.CreateNewCircuitButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.CreateNewCircuitButton.setObjectName("CreateNewCircuitButton")
        self.ModelSettingTopBottomRightButtons.addWidget(self.CreateNewCircuitButton)
        self.ModelSettingApplyToAllDataButton = QtWidgets.QPushButton(
            parent=self.layoutWidget
        )
        self.ModelSettingApplyToAllDataButton.setObjectName(
            "ModelSettingApplyToAllDataButton"
        )
        self.ModelSettingTopBottomRightButtons.addWidget(
            self.ModelSettingApplyToAllDataButton
        )
        self.ModelSettingTopRightLayout.addLayout(
            self.ModelSettingTopBottomRightButtons
        )
        self.ModelSettingTopButtons.addLayout(self.ModelSettingTopRightLayout)

        self.retranslateUi(ModelSettings)
        self.ModelSettingDiagramComboBox.currentIndexChanged["int"].connect(ModelSettings.modelSettingDiagramComboBoxChanged)  # type: ignore
        self.ModelSettingPreviousDataButton.clicked.connect(ModelSettings.modelSettingPreviousDataButtonClicked)  # type: ignore
        self.ModelSettingNextDataButton.clicked.connect(ModelSettings.modelSettingNextDataButtonClicked)  # type: ignore
        self.ModelSettingBackButton.clicked.connect(ModelSettings.modelSettingBackButtonClicked)  # type: ignore
        self.ModelSettingSaveButton.clicked.connect(ModelSettings.modelSettingSaveButtonClicked)  # type: ignore
        self.ModelSettingApplyToAllDataButton.clicked.connect(ModelSettings.modelSettingApplyToAllDataButtonClicked)  # type: ignore
        self.ModelSettingChangeCircuitNameButton.clicked.connect(ModelSettings.modelSettingChangeCircuitNameButtonClicked)  # type: ignore
        self.ModelSettingClearAllComponentsBotton.clicked.connect(ModelSettings.modelSettingClearAllComponentsButtonClicked)  # type: ignore
        self.CreateNewCircuitButton.clicked.connect(ModelSettings.createNewCircuitButtonClicked)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ModelSettings)
        ModelSettings.setTabOrder(
            self.ModelSettingDiagramComboBox, self.CreateNewCircuitButton
        )
        ModelSettings.setTabOrder(
            self.CreateNewCircuitButton, self.ModelSettingApplyToAllDataButton
        )
        ModelSettings.setTabOrder(
            self.ModelSettingApplyToAllDataButton,
            self.ModelSettingChangeCircuitNameButton,
        )
        ModelSettings.setTabOrder(
            self.ModelSettingChangeCircuitNameButton,
            self.ModelSettingClearAllComponentsBotton,
        )
        ModelSettings.setTabOrder(
            self.ModelSettingClearAllComponentsBotton, self.ModelSettingScrollArea
        )
        ModelSettings.setTabOrder(
            self.ModelSettingScrollArea, self.ModelSettingPreviousDataButton
        )
        ModelSettings.setTabOrder(
            self.ModelSettingPreviousDataButton, self.ModelSettingNextDataButton
        )
        ModelSettings.setTabOrder(
            self.ModelSettingNextDataButton, self.ModelSettingBackButton
        )
        ModelSettings.setTabOrder(
            self.ModelSettingBackButton, self.ModelSettingSaveButton
        )

    def retranslateUi(self, ModelSettings):
        _translate = QtCore.QCoreApplication.translate
        ModelSettings.setWindowTitle(_translate("ModelSettings", "模型编辑器"))
        self.ModelSettingDataNameLabel.setText(
            _translate("ModelSettings", "*插入数据名称*:")
        )
        self.ModelSettingBackButton.setText(_translate("ModelSettings", "不保存返回"))
        self.ModelSettingSaveButton.setText(_translate("ModelSettings", "保存"))
        self.staticLabel.setText(_translate("ModelSettings", "切换数据"))
        self.ModelSettingChangeCircuitNameButton.setText(
            _translate("ModelSettings", "更改电路名称")
        )
        self.ModelSettingClearAllComponentsBotton.setText(
            _translate("ModelSettings", "清空组件")
        )
        self.CreateNewCircuitButton.setText(_translate("ModelSettings", "新建电路图"))
        self.ModelSettingApplyToAllDataButton.setText(
            _translate("ModelSettings", "应用到全部数据")
        )

    def customUIs(self):
        frame = self.ModelSettingFrame
        layout = QtWidgets.QVBoxLayout(frame)
        self.frameLabel = QtWidgets.QLabel(frame)
        self.frameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.frameLabel)

        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.ModelSettingScrollAreaContents.setLayout(self.buttonLayout)

        self.populateCircuitPrototypeComponents()
        self.setupCircuitPrototypeComponentsScrollArea()

        self.setupSubWidgets()

    def setupComponents(self):
        self.circuits = [None for _ in range(len(self.dataNames))]

        self.invaildRead = False
        setAllCircuitsToLastUsedCircuit = False
        self.readModelSettings()
        if self.invaildRead:
            print("未能正确读取Model Settings")
        else:
            setAllCircuitsToLastUsedCircuit = True

        self.invaildRead = False
        self.readCircuitPrototypes()
        if self.invaildRead:
            print("未能读取到Prototype Circuits")

        if setAllCircuitsToLastUsedCircuit:
            self.updateCircuitPrototypesComboBox()
            self.ModelSettingDiagramComboBox.setCurrentText(
                self.modelSettings["Last Used Circuit Name"]
            )
            circuit = self.getCurrentCircuitPrototype()
            self.circuits = [circuit for _ in range(len(self.dataNames))]

        self.updateUIs()

    def setupSubWidgets(self):
        self.changeCircuitNameDialog = ChangeCircuitNameDialog()
        self.changeCircuitNameDialog.namesSignal.connect(self.receiveCircuitName)

    def updateUIs(self):
        self.updateDataName()
        self.updateCircuitPrototypesComboBox()
        self.updateCircuitPrototypeDiagram()

        disable = False
        if self.getCurrentCircuitPrototype() is None:
            disable = True

        self.ModelSettingScrollArea.setDisabled(disable)
        self.ModelSettingChangeCircuitNameButton.setDisabled(disable)
        self.ModelSettingClearAllComponentsBotton.setDisabled(disable)
        if not disable:
            self.circuits[self.circuitIndex] = self.getCurrentCircuitPrototype()
            self.modelSettings["Last Used Circuit Name"] = (
                self.ModelSettingDiagramComboBox.currentText()
            )

        self.ModelSettingPreviousDataButton.setEnabled(self.circuitIndex > 0)
        self.ModelSettingNextDataButton.setEnabled(
            self.circuitIndex < len(self.dataNames) - 1
        )

    def populateCircuitPrototypeComponents(self):
        self.circuitPrototypeComponents = {}

        allAttributes = dir(Components)
        componentNames = [attr for attr in allAttributes if not attr.startswith("__")]
        componentNames.remove("ComponentBase")

        for componentName in componentNames:
            ref = getattr(Components, componentName)
            if isinstance(ref, type):
                self.circuitPrototypeComponents[componentName] = ref()
            else:
                print(f"Model Settings: The ref of {componentName} is not a type")

    def setupCircuitPrototypeComponentsScrollArea(self):
        buttonLayout = self.buttonLayout
        while buttonLayout.count() > 0:
            item = buttonLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for moduleName, component in self.circuitPrototypeComponents.items():
            if hasattr(component, "displayName"):
                displayName = getattr(component, "displayName")
            if not isinstance(displayName, str):
                displayName = moduleName

            button = QtWidgets.QPushButton(displayName, self)
            button.clicked.connect(
                lambda _, x=moduleName: self.componentsButtonClicked(x)
            )
            buttonLayout.addWidget(button)

    def getCurrentCircuitPrototype(self):
        currentCircuit = None

        displayName = self.ModelSettingDiagramComboBox.currentText()
        if displayName in self.circuitPrototypeSectionNames.keys():
            sectionName = self.circuitPrototypeSectionNames[displayName]
            currentCircuit = self.circuitPrototypes[sectionName]

        return currentCircuit

    def componentsButtonClicked(self, name: str):
        currentCircuit = self.getCurrentCircuitPrototype()
        currentCircuit.componentNames.append(name)
        currentCircuit.updateComponentInfos()

        self.updateCircuitPrototypeDiagram()

    def updateDataName(self):
        self.ModelSettingDataNameLabel.setText(self.dataNames[self.circuitIndex] + ":")

    def updateCircuitPrototypesComboBox(self):
        combobox = self.ModelSettingDiagramComboBox
        oldChoice = combobox.currentText()

        combobox.blockSignals(True)
        combobox.clear()
        for circuitPrototype in self.circuitPrototypes.values():
            combobox.addItem(circuitPrototype.displayName)

        combobox.setCurrentText(oldChoice)
        combobox.blockSignals(False)

    def updateCircuitPrototypeDiagram(self):
        currentCircuit = self.getCurrentCircuitPrototype()
        if currentCircuit == None:
            text = f"未选中任何电路，请新建一个电路"
        else:
            name = currentCircuit.displayName
            count = len(currentCircuit.components)

            text = f"电路{name}已经有{count}个组件：\n"
            componentNamesText = ", ".join(currentCircuit.componentDisplayNames)
            text += componentNamesText

        self.frameLabel.setText(text)

    def createNewCircuitPrototype(self):
        newCircuit = Circuit.Circuit()
        i = 1
        keys = self.circuitPrototypes.keys()
        while f"New Circuit {i}" in keys:
            i += 1
        displayName = f"New Circuit {i}"
        newCircuit.displayName = displayName

        sectionName = displayName
        self.circuitPrototypes[sectionName] = newCircuit
        self.circuitPrototypeSectionNames[newCircuit.displayName] = sectionName

        self.updateCircuitPrototypesComboBox()
        self.ModelSettingDiagramComboBox.setCurrentText(displayName)

        self.frameLabel.setText("已创建新电路图！")

        self.updateUIs()

    def readModelSettings(self):
        config = configparser.ConfigParser()
        config.read(configFilePath)

        if len(config.sections()) != 0:
            for key in self.modelSettings.keys():
                text = config[modelSettingsSectionName][key]
                if text != "":
                    self.modelSettings[key] = text
        else:
            self.invaildRead = True

    def writeModelSettings(self):
        config = configparser.ConfigParser()

        if not None in self.modelSettings.values():
            config[modelSettingsSectionName] = self.modelSettings

        with open(configFilePath, "w") as configfile:
            config.write(configfile)

    def transformCircuitInfo(self, circuitInfo: dict, direction: str):
        if direction == "config to use":
            circuitInfo["Component Names"] = circuitInfo["Component Names"].split(
                circuitInfoSplitText
            )
        if direction == "use to config":
            circuitInfo["Component Names"] = circuitInfoSplitText.join(
                circuitInfo["Component Names"]
            )

    def readCircuitPrototypes(self):
        self.circuitPrototypes = {}
        self.circuitPrototypeSectionNames = {}

        config = configparser.ConfigParser()
        config.read(circuitConfigPath)

        if len(config.sections()) != 0:
            atleastOneVaild = False
            for sectionName in config.sections():
                circuitInfo = {"Display Name": "", "Component Names": ""}

                vaildData = True
                for key in circuitInfo.keys():
                    text = config[sectionName][key]
                    if text != "":
                        circuitInfo[key] = text
                    else:
                        vaildData = False
                        break

                if vaildData:
                    atleastOneVaild = True

                    self.transformCircuitInfo(circuitInfo, "config to use")
                    circuitPrototype = Circuit.Circuit(circuitInfo)
                    self.circuitPrototypes[sectionName] = circuitPrototype
                    self.circuitPrototypeSectionNames[circuitPrototype.displayName] = (
                        sectionName
                    )

            if not atleastOneVaild:
                self.invaildRead = True
        else:
            self.invaildRead = True

    def writeCircuitPrototypes(self):
        config = configparser.ConfigParser()

        for sectionName, circuitPrototype in self.circuitPrototypes.items():
            if len(circuitPrototype.components) == 0:
                continue

            circuitInfo = {}
            circuitInfo["Display Name"] = circuitPrototype.displayName
            circuitInfo["Component Names"] = circuitPrototype.componentNames
            self.transformCircuitInfo(circuitInfo, "use to config")

            config[sectionName] = circuitInfo

        with open(circuitConfigPath, "w") as configfile:
            config.write(configfile)

    def emitCircuits(self):
        self.circuitsSignal.emit(self.circuits)

    def modelSettingDiagramComboBoxChanged(self):
        self.updateUIs()

    def modelSettingChangeCircuitNameButtonClicked(self):
        existedSectionName = list(self.circuitPrototypeSectionNames.values())

        currentCircuit = self.getCurrentCircuitPrototype()
        currentCircuitSectionName = self.circuitPrototypeSectionNames[
            currentCircuit.displayName
        ]
        existedSectionName.remove(currentCircuitSectionName)

        self.changeCircuitNameDialog.existedSectionName = existedSectionName
        self.changeCircuitNameDialog.displayNameLineEdit.setText(
            currentCircuit.displayName
        )
        self.changeCircuitNameDialog.sectionNameLineEdit.setText(
            currentCircuitSectionName
        )
        self.changeCircuitNameDialog.show()

    def receiveCircuitName(self, names: dict):
        currentCircuit = self.getCurrentCircuitPrototype()
        oldDisplayName = currentCircuit.displayName
        oldSectionName = self.circuitPrototypeSectionNames[oldDisplayName]

        displayName = names["Display Name"]
        sectionName = names["Section Name"]

        currentCircuit.displayName = displayName
        self.circuitPrototypes.pop(oldSectionName)
        self.circuitPrototypes[sectionName] = currentCircuit
        self.circuitPrototypeSectionNames.pop(oldDisplayName)
        self.circuitPrototypeSectionNames[displayName] = sectionName

        index = self.ModelSettingDiagramComboBox.currentIndex()
        self.ModelSettingDiagramComboBox.setItemText(index, displayName)

        self.updateUIs()

    def createNewCircuitButtonClicked(self):
        self.createNewCircuitPrototype()

    def modelSettingClearAllComponentsButtonClicked(self):
        currentCircuit = self.getCurrentCircuitPrototype()
        currentCircuit.componentNames = []
        currentCircuit.updateComponentInfos()
        self.updateCircuitPrototypeDiagram()

    def modelSettingApplyToAllDataButtonClicked(self):
        currentCircuit = self.getCurrentCircuitPrototype()

        length = len(self.dataNames)

        self.circuits = []
        for _ in range(length):
            self.circuits.append(currentCircuit)

    def modelSettingPreviousDataButtonClicked(self):
        if self.circuitIndex > 0:
            self.circuitIndex -= 1
            self.updateUIs()
            self.circuits[self.circuitIndex] = self.getCurrentCircuitPrototype()

    def modelSettingNextDataButtonClicked(self):
        if self.circuitIndex < len(self.dataNames) - 1:
            self.circuitIndex += 1
            self.updateUIs()
            self.circuits[self.circuitIndex] = self.getCurrentCircuitPrototype()

    def modelSettingBackButtonClicked(self):
        self.close()

    def modelSettingSaveButtonClicked(self):
        self.writeModelSettings()
        self.writeCircuitPrototypes()

        self.emitCircuits()
        self.close()


class ModelSettingsDialog(QtWidgets.QDialog, ModelSettingsDialog):
    def __init__(self):
        super(ModelSettingsDialog, self).__init__()
        self.setupUi(self)
        self.customUIs()
