from PyQt6 import QtCore, QtGui, QtWidgets


class ChangeCircuitNameDialog(object):
    existedSectionName = []

    names = {"Display Name": "", "Section Name": ""}
    namesSignal = QtCore.pyqtSignal(dict)

    def setupUi(self, ChangeCircuitNameDialog):
        ChangeCircuitNameDialog.setObjectName("ChangeCircuitNameDialog")
        ChangeCircuitNameDialog.resize(280, 200)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=ChangeCircuitNameDialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 160, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(parent=ChangeCircuitNameDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 251, 151))
        self.widget.setObjectName("widget")
        self.NamesLayout = QtWidgets.QVBoxLayout(self.widget)
        self.NamesLayout.setContentsMargins(0, 0, 0, 0)
        self.NamesLayout.setObjectName("NamesLayout")
        self.DisplayNameLayout = QtWidgets.QVBoxLayout()
        self.DisplayNameLayout.setSpacing(4)
        self.DisplayNameLayout.setObjectName("DisplayNameLayout")
        self.staticLabel1 = QtWidgets.QLabel(parent=self.widget)
        self.staticLabel1.setMaximumSize(QtCore.QSize(16777215, 15))
        self.staticLabel1.setObjectName("staticLabel1")
        self.DisplayNameLayout.addWidget(self.staticLabel1)
        self.displayNameLineEdit = QtWidgets.QLineEdit(parent=self.widget)
        self.displayNameLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.displayNameLineEdit.setText("")
        self.displayNameLineEdit.setObjectName("displayNameLineEdit")
        self.DisplayNameLayout.addWidget(self.displayNameLineEdit)
        self.NamesLayout.addLayout(self.DisplayNameLayout)
        self.SectionNameLayout = QtWidgets.QVBoxLayout()
        self.SectionNameLayout.setSpacing(4)
        self.SectionNameLayout.setObjectName("SectionNameLayout")
        self.staticLabel2 = QtWidgets.QLabel(parent=self.widget)
        self.staticLabel2.setMaximumSize(QtCore.QSize(16777215, 15))
        self.staticLabel2.setObjectName("staticLabel2")
        self.SectionNameLayout.addWidget(self.staticLabel2)
        self.sectionNameLineEdit = QtWidgets.QLineEdit(parent=self.widget)
        self.sectionNameLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.sectionNameLineEdit.setText("")
        self.sectionNameLineEdit.setObjectName("sectionNameLineEdit")
        self.SectionNameLayout.addWidget(self.sectionNameLineEdit)
        self.NamesLayout.addLayout(self.SectionNameLayout)

        self.retranslateUi(ChangeCircuitNameDialog)
        self.buttonBox.accepted.connect(ChangeCircuitNameDialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(ChangeCircuitNameDialog.reject)  # type: ignore
        self.displayNameLineEdit.editingFinished.connect(ChangeCircuitNameDialog.displayNameEditFinished)  # type: ignore
        self.sectionNameLineEdit.textChanged["QString"].connect(ChangeCircuitNameDialog.sectionNameTextChanged)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ChangeCircuitNameDialog)

    def retranslateUi(self, ChangeCircuitNameDialog):
        _translate = QtCore.QCoreApplication.translate
        ChangeCircuitNameDialog.setWindowTitle(
            _translate("ChangeCircuitNameDialog", "更改电路名称")
        )
        self.staticLabel1.setText(
            _translate("ChangeCircuitNameDialog", "电路显示名称：")
        )
        self.staticLabel2.setText(
            _translate(
                "ChangeCircuitNameDialog", "电路保存名称（不可重复，建议英文）："
            )
        )

    def accept(self):
        vaildName = True
        for name in self.names.values():
            if name == "":
                vaildName = False

        if not vaildName:
            QtWidgets.QMessageBox.warning(
                self, "有非法名称", "输入的名称不能为空！请改成其他名称！"
            )
        else:
            self.namesSignal.emit(self.names)
            self.close()

    def displayNameEditFinished(self):
        text = self.displayNameLineEdit.text()
        self.names["Display Name"] = text
        self.sectionNameLineEdit.setText(text)

    def sectionNameTextChanged(self, text: str):
        if text in self.existedSectionName:
            QtWidgets.QMessageBox.warning(
                self, "输入的保存名称已存在", "输入的保存名称已存在！请改成其他名称！"
            )
            self.sectionNameLineEdit.setText("")
        else:
            self.names["Section Name"] = text


class ChangeCircuitNameDialog(QtWidgets.QDialog, ChangeCircuitNameDialog):
    def __init__(self):
        super(ChangeCircuitNameDialog, self).__init__()
        self.setupUi(self)
