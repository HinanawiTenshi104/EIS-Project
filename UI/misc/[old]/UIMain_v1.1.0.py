import os
import random
import subprocess

import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets

try:
    from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
    from PyQt6.QtMultimediaWidgets import QVideoWidget

    hasMultiMedia = True
except:
    hasMultiMedia = False

import DataProcessor
import DrawDiagram
import IO
import Optimizer

from .PreprocessSetting import PreprocessSettingDialog
from .ProcessDataThread import ProcessDataThread
from .ProgramSettings import ProgramSettingsDialog
from .ReadDRTToolStateThread import ReadDRTToolStateThread

UIResourceBaseDir = QtCore.QDir.currentPath() + r"/UI/UI Elements/"
UIMainResourceDir = UIResourceBaseDir + r"Main/"
UIReadDatasResourceDir = UIResourceBaseDir + r"ReadDatas/"
UIProcessSettingsResourceDir = UIResourceBaseDir + r"ProcessSettings/"
UIProcessingResourceDir = UIResourceBaseDir + r"Processing/"
UIProcessingButtonIconDir = UIProcessingResourceDir + r"Button Icons/"
UISaveResultResourceDir = UIResourceBaseDir + r"SaveResult/"


class CenteredWidget(QtWidgets.QWidget):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.widget = widget
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.widget)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):
    pageIndexes = {
        "Main Menu": 0,
        "Read Data": 1,
        "Process Settings": 2,
        "Processing": 3,
        "Result": 4,
    }

    def __init__(self):
        super().__init__()

        icon = QtGui.QIcon(UIResourceBaseDir + "Icon.ico")
        self.setWindowIcon(icon)

        self.setupUi(self)
        self.setupComponents()

    def changeEvent(self, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowState.WindowMinimized:
                # print("Window has been minimized.")

                # Processing Page
                isProcessingPage = (
                    self.Widgets.currentIndex() == self.pageIndexes["Processing"]
                )
                if isProcessingPage and hasMultiMedia:
                    player = self.processingPlayer
                    audio = self.processingAudio

                    if (
                        player.playbackState()
                        == QMediaPlayer.PlaybackState.PlayingState
                    ):
                        self.processingPlayButtonClicked()

            elif self.windowState() == QtCore.Qt.WindowState.WindowNoState:
                # print("Window has been restored.")
                None

        super().changeEvent(event)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.mainWindowWidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainWindowWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWindowWidget.sizePolicy().hasHeightForWidth()
        )
        self.mainWindowWidget.setSizePolicy(sizePolicy)
        self.mainWindowWidget.setObjectName("mainWindowWidget")
        self.Widgets = QtWidgets.QStackedWidget(parent=self.mainWindowWidget)
        self.Widgets.setGeometry(QtCore.QRect(0, 0, 800, 600))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Widgets.sizePolicy().hasHeightForWidth())
        self.Widgets.setSizePolicy(sizePolicy)
        self.Widgets.setObjectName("Widgets")
        self.Start = QtWidgets.QWidget()
        self.Start.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Start.sizePolicy().hasHeightForWidth())
        self.Start.setSizePolicy(sizePolicy)
        self.Start.setObjectName("Start")
        self.TitlePic = QtWidgets.QLabel(parent=self.Start)
        self.TitlePic.setGeometry(QtCore.QRect(10, 10, 771, 221))
        self.TitlePic.setScaledContents(True)
        self.TitlePic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TitlePic.setObjectName("TitlePic")
        self.CornerPic = QtWidgets.QLabel(parent=self.Start)
        self.CornerPic.setGeometry(QtCore.QRect(30, 240, 371, 331))
        self.CornerPic.setScaledContents(True)
        self.CornerPic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CornerPic.setObjectName("CornerPic")
        self.VersionText = QtWidgets.QLabel(parent=self.Start)
        self.VersionText.setGeometry(QtCore.QRect(20, 575, 371, 21))
        self.VersionText.setObjectName("VersionText")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.Start)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(492, 250, 291, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.StartButtons = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.StartButtons.setContentsMargins(0, 0, 0, 0)
        self.StartButtons.setObjectName("StartButtons")
        self.ReadDataButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ReadDataButton.sizePolicy().hasHeightForWidth()
        )
        self.ReadDataButton.setSizePolicy(sizePolicy)
        self.ReadDataButton.setMinimumSize(QtCore.QSize(280, 80))
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(20)
        font.setBold(False)
        self.ReadDataButton.setFont(font)
        self.ReadDataButton.setObjectName("ReadDataButton")
        self.StartButtons.addWidget(
            self.ReadDataButton,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.ProgramSettingButton = QtWidgets.QPushButton(
            parent=self.verticalLayoutWidget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProgramSettingButton.sizePolicy().hasHeightForWidth()
        )
        self.ProgramSettingButton.setSizePolicy(sizePolicy)
        self.ProgramSettingButton.setMinimumSize(QtCore.QSize(280, 80))
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(20)
        self.ProgramSettingButton.setFont(font)
        self.ProgramSettingButton.setObjectName("ProgramSettingButton")
        self.StartButtons.addWidget(
            self.ProgramSettingButton,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.ExitButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExitButton.sizePolicy().hasHeightForWidth())
        self.ExitButton.setSizePolicy(sizePolicy)
        self.ExitButton.setMinimumSize(QtCore.QSize(280, 80))
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(20)
        self.ExitButton.setFont(font)
        self.ExitButton.setObjectName("ExitButton")
        self.StartButtons.addWidget(
            self.ExitButton,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.Widgets.addWidget(self.Start)
        self.ReadData = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ReadData.sizePolicy().hasHeightForWidth())
        self.ReadData.setSizePolicy(sizePolicy)
        self.ReadData.setObjectName("ReadData")
        self.ReadDataDiagramPic = QtWidgets.QLabel(parent=self.ReadData)
        self.ReadDataDiagramPic.setGeometry(QtCore.QRect(300, 10, 491, 451))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ReadDataDiagramPic.sizePolicy().hasHeightForWidth()
        )
        self.ReadDataDiagramPic.setSizePolicy(sizePolicy)
        self.ReadDataDiagramPic.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.ReadDataDiagramPic.setScaledContents(True)
        self.ReadDataDiagramPic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ReadDataDiagramPic.setObjectName("ReadDataDiagramPic")
        self.layoutWidget = QtWidgets.QWidget(parent=self.ReadData)
        self.layoutWidget.setGeometry(QtCore.QRect(510, 530, 271, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.ReadDataBottomButtons = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.ReadDataBottomButtons.setContentsMargins(0, 0, 0, 0)
        self.ReadDataBottomButtons.setObjectName("ReadDataBottomButtons")
        self.ReadDataBackButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.ReadDataBackButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ReadDataBackButton.setObjectName("ReadDataBackButton")
        self.ReadDataBottomButtons.addWidget(self.ReadDataBackButton)
        self.ReadDataNextButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.ReadDataNextButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ReadDataNextButton.setObjectName("ReadDataNextButton")
        self.ReadDataBottomButtons.addWidget(self.ReadDataNextButton)
        self.ReadDataTreeView = QtWidgets.QTreeView(parent=self.ReadData)
        self.ReadDataTreeView.setGeometry(QtCore.QRect(10, 10, 271, 571))
        self.ReadDataTreeView.setObjectName("ReadDataTreeView")
        self.ReadDataHighlightFileName = QtWidgets.QLabel(parent=self.ReadData)
        self.ReadDataHighlightFileName.setGeometry(QtCore.QRect(290, 510, 201, 81))
        self.ReadDataHighlightFileName.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.ReadDataHighlightFileName.setWordWrap(True)
        self.ReadDataHighlightFileName.setObjectName("ReadDataHighlightFileName")
        self.ReadDataProcessingDRTLabel = QtWidgets.QLabel(parent=self.ReadData)
        self.ReadDataProcessingDRTLabel.setGeometry(QtCore.QRect(300, 470, 481, 31))
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(20)
        self.ReadDataProcessingDRTLabel.setFont(font)
        self.ReadDataProcessingDRTLabel.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.ReadDataProcessingDRTLabel.setWordWrap(True)
        self.ReadDataProcessingDRTLabel.setObjectName("ReadDataProcessingDRTLabel")
        self.Widgets.addWidget(self.ReadData)
        self.ProcessSettings = QtWidgets.QWidget()
        self.ProcessSettings.setObjectName("ProcessSettings")
        self.DRTDiagramPic = QtWidgets.QLabel(parent=self.ProcessSettings)
        self.DRTDiagramPic.setGeometry(QtCore.QRect(300, 10, 491, 451))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.DRTDiagramPic.sizePolicy().hasHeightForWidth()
        )
        self.DRTDiagramPic.setSizePolicy(sizePolicy)
        self.DRTDiagramPic.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.DRTDiagramPic.setScaledContents(True)
        self.DRTDiagramPic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.DRTDiagramPic.setObjectName("DRTDiagramPic")
        self.layoutWidget_2 = QtWidgets.QWidget(parent=self.ProcessSettings)
        self.layoutWidget_2.setGeometry(QtCore.QRect(510, 530, 271, 61))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.ProcessSettingBottomButtons = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.ProcessSettingBottomButtons.setContentsMargins(0, 0, 0, 0)
        self.ProcessSettingBottomButtons.setObjectName("ProcessSettingBottomButtons")
        self.ProcessSettingBackButton = QtWidgets.QPushButton(
            parent=self.layoutWidget_2
        )
        self.ProcessSettingBackButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ProcessSettingBackButton.setObjectName("ProcessSettingBackButton")
        self.ProcessSettingBottomButtons.addWidget(self.ProcessSettingBackButton)
        self.ProcessSettingNextButton = QtWidgets.QPushButton(
            parent=self.layoutWidget_2
        )
        self.ProcessSettingNextButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ProcessSettingNextButton.setObjectName("ProcessSettingNextButton")
        self.ProcessSettingBottomButtons.addWidget(self.ProcessSettingNextButton)
        self.DataNameLabel = QtWidgets.QLabel(parent=self.ProcessSettings)
        self.DataNameLabel.setGeometry(QtCore.QRect(10, 10, 271, 41))
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(20)
        self.DataNameLabel.setFont(font)
        self.DataNameLabel.setScaledContents(True)
        self.DataNameLabel.setObjectName("DataNameLabel")
        self.staticLabel3 = QtWidgets.QLabel(parent=self.ProcessSettings)
        self.staticLabel3.setGeometry(QtCore.QRect(10, 130, 101, 21))
        self.staticLabel3.setObjectName("staticLabel3")
        self.ProcessSettingInfoTextBoxPic = QtWidgets.QLabel(
            parent=self.ProcessSettings
        )
        self.ProcessSettingInfoTextBoxPic.setGeometry(QtCore.QRect(10, 470, 471, 121))
        self.ProcessSettingInfoTextBoxPic.setScaledContents(True)
        self.ProcessSettingInfoTextBoxPic.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.ProcessSettingInfoTextBoxPic.setWordWrap(False)
        self.ProcessSettingInfoTextBoxPic.setObjectName("ProcessSettingInfoTextBoxPic")
        self.BoundsTable = QtWidgets.QTableWidget(parent=self.ProcessSettings)
        self.BoundsTable.setGeometry(QtCore.QRect(10, 150, 281, 91))
        self.BoundsTable.setLineWidth(1)
        self.BoundsTable.setMidLineWidth(0)
        self.BoundsTable.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.BoundsTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        self.BoundsTable.setAutoScrollMargin(16)
        self.BoundsTable.setTextElideMode(QtCore.Qt.TextElideMode.ElideMiddle)
        self.BoundsTable.setShowGrid(True)
        self.BoundsTable.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.BoundsTable.setCornerButtonEnabled(True)
        self.BoundsTable.setObjectName("BoundsTable")
        self.BoundsTable.setColumnCount(2)
        self.BoundsTable.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.BoundsTable.setItem(0, 1, item)
        self.BoundsTable.horizontalHeader().setVisible(True)
        self.BoundsTable.horizontalHeader().setCascadingSectionResizes(True)
        self.BoundsTable.horizontalHeader().setDefaultSectionSize(100)
        self.BoundsTable.horizontalHeader().setMinimumSectionSize(30)
        self.BoundsTable.horizontalHeader().setStretchLastSection(True)
        self.BoundsTable.verticalHeader().setVisible(True)
        self.BoundsTable.verticalHeader().setCascadingSectionResizes(True)
        self.BoundsTable.verticalHeader().setDefaultSectionSize(30)
        self.BoundsTable.verticalHeader().setSortIndicatorShown(False)
        self.staticLabel1 = QtWidgets.QLabel(parent=self.ProcessSettings)
        self.staticLabel1.setGeometry(QtCore.QRect(10, 60, 101, 21))
        self.staticLabel1.setObjectName("staticLabel1")
        self.ProcessSettingInfoText = QtWidgets.QLabel(parent=self.ProcessSettings)
        self.ProcessSettingInfoText.setGeometry(QtCore.QRect(40, 490, 411, 81))
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(12)
        self.ProcessSettingInfoText.setFont(font)
        self.ProcessSettingInfoText.setScaledContents(False)
        self.ProcessSettingInfoText.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.ProcessSettingInfoText.setWordWrap(True)
        self.ProcessSettingInfoText.setObjectName("ProcessSettingInfoText")
        self.RingCountSpinBox = QtWidgets.QSpinBox(parent=self.ProcessSettings)
        self.RingCountSpinBox.setGeometry(QtCore.QRect(10, 90, 121, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        self.RingCountSpinBox.setFont(font)
        self.RingCountSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RingCountSpinBox.setPrefix("")
        self.RingCountSpinBox.setMaximum(10)
        self.RingCountSpinBox.setProperty("value", 0)
        self.RingCountSpinBox.setObjectName("RingCountSpinBox")
        self.PreprocessDataCheckBox = QtWidgets.QCheckBox(parent=self.ProcessSettings)
        self.PreprocessDataCheckBox.setGeometry(QtCore.QRect(10, 250, 91, 21))
        self.PreprocessDataCheckBox.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.PreprocessDataCheckBox.setChecked(True)
        self.PreprocessDataCheckBox.setObjectName("PreprocessDataCheckBox")
        self.ShowPreprocessOptionsButton = QtWidgets.QPushButton(
            parent=self.ProcessSettings
        )
        self.ShowPreprocessOptionsButton.setGeometry(QtCore.QRect(10, 280, 131, 41))
        self.ShowPreprocessOptionsButton.setObjectName("ShowPreprocessOptionsButton")
        self.MethodsTable = QtWidgets.QTableWidget(parent=self.ProcessSettings)
        self.MethodsTable.setGeometry(QtCore.QRect(10, 330, 281, 131))
        self.MethodsTable.setLineWidth(1)
        self.MethodsTable.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.MethodsTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        self.MethodsTable.setAutoScrollMargin(16)
        self.MethodsTable.setTextElideMode(QtCore.Qt.TextElideMode.ElideMiddle)
        self.MethodsTable.setShowGrid(True)
        self.MethodsTable.setCornerButtonEnabled(True)
        self.MethodsTable.setObjectName("MethodsTable")
        self.MethodsTable.setColumnCount(0)
        self.MethodsTable.setRowCount(0)
        self.MethodsTable.horizontalHeader().setVisible(True)
        self.MethodsTable.horizontalHeader().setCascadingSectionResizes(True)
        self.MethodsTable.horizontalHeader().setDefaultSectionSize(100)
        self.MethodsTable.horizontalHeader().setMinimumSectionSize(30)
        self.MethodsTable.horizontalHeader().setStretchLastSection(True)
        self.MethodsTable.verticalHeader().setVisible(True)
        self.MethodsTable.verticalHeader().setCascadingSectionResizes(True)
        self.MethodsTable.verticalHeader().setDefaultSectionSize(30)
        self.MethodsTable.verticalHeader().setSortIndicatorShown(False)
        self.MethodSelectAllCheckBox = QtWidgets.QCheckBox(parent=self.ProcessSettings)
        self.MethodSelectAllCheckBox.setGeometry(QtCore.QRect(180, 300, 111, 21))
        self.MethodSelectAllCheckBox.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.MethodSelectAllCheckBox.setChecked(False)
        self.MethodSelectAllCheckBox.setObjectName("MethodSelectAllCheckBox")
        self.layoutWidget_4 = QtWidgets.QWidget(parent=self.ProcessSettings)
        self.layoutWidget_4.setGeometry(QtCore.QRect(490, 470, 151, 32))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.ProcessSettingSwitchDataButtons = QtWidgets.QHBoxLayout(
            self.layoutWidget_4
        )
        self.ProcessSettingSwitchDataButtons.setContentsMargins(0, 0, 0, 0)
        self.ProcessSettingSwitchDataButtons.setSpacing(0)
        self.ProcessSettingSwitchDataButtons.setObjectName(
            "ProcessSettingSwitchDataButtons"
        )
        self.ProcessSettingPreviousDataButton = QtWidgets.QToolButton(
            parent=self.layoutWidget_4
        )
        self.ProcessSettingPreviousDataButton.setMinimumSize(QtCore.QSize(30, 30))
        self.ProcessSettingPreviousDataButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.ProcessSettingPreviousDataButton.setText("")
        self.ProcessSettingPreviousDataButton.setArrowType(
            QtCore.Qt.ArrowType.LeftArrow
        )
        self.ProcessSettingPreviousDataButton.setObjectName(
            "ProcessSettingPreviousDataButton"
        )
        self.ProcessSettingSwitchDataButtons.addWidget(
            self.ProcessSettingPreviousDataButton
        )
        self.staticLabel2 = QtWidgets.QLabel(parent=self.layoutWidget_4)
        self.staticLabel2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.staticLabel2.setObjectName("staticLabel2")
        self.ProcessSettingSwitchDataButtons.addWidget(self.staticLabel2)
        self.ProcessSettingNextDataButton = QtWidgets.QToolButton(
            parent=self.layoutWidget_4
        )
        self.ProcessSettingNextDataButton.setMinimumSize(QtCore.QSize(30, 30))
        self.ProcessSettingNextDataButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.ProcessSettingNextDataButton.setText("")
        self.ProcessSettingNextDataButton.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        self.ProcessSettingNextDataButton.setObjectName("ProcessSettingNextDataButton")
        self.ProcessSettingSwitchDataButtons.addWidget(
            self.ProcessSettingNextDataButton
        )
        self.Widgets.addWidget(self.ProcessSettings)
        self.Processing = QtWidgets.QWidget()
        self.Processing.setObjectName("Processing")
        self.ProcessingNextButton = QtWidgets.QPushButton(parent=self.Processing)
        self.ProcessingNextButton.setEnabled(False)
        self.ProcessingNextButton.setGeometry(QtCore.QRect(660, 460, 121, 51))
        self.ProcessingNextButton.setObjectName("ProcessingNextButton")
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.Processing)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 520, 761, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.ProcessingProgressBars = QtWidgets.QFormLayout(self.layoutWidget1)
        self.ProcessingProgressBars.setContentsMargins(0, 0, 0, 0)
        self.ProcessingProgressBars.setObjectName("ProcessingProgressBars")
        self.staticLabel4 = QtWidgets.QLabel(parent=self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(12)
        self.staticLabel4.setFont(font)
        self.staticLabel4.setObjectName("staticLabel4")
        self.ProcessingProgressBars.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.staticLabel4
        )
        self.CurrentMethodProgressBar = QtWidgets.QProgressBar(
            parent=self.layoutWidget1
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.CurrentMethodProgressBar.sizePolicy().hasHeightForWidth()
        )
        self.CurrentMethodProgressBar.setSizePolicy(sizePolicy)
        self.CurrentMethodProgressBar.setProperty("value", 50)
        self.CurrentMethodProgressBar.setObjectName("CurrentMethodProgressBar")
        self.ProcessingProgressBars.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.CurrentMethodProgressBar
        )
        self.staticLabel5 = QtWidgets.QLabel(parent=self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(12)
        self.staticLabel5.setFont(font)
        self.staticLabel5.setObjectName("staticLabel5")
        self.ProcessingProgressBars.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.staticLabel5
        )
        self.TotalProgressBar = QtWidgets.QProgressBar(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.TotalProgressBar.sizePolicy().hasHeightForWidth()
        )
        self.TotalProgressBar.setSizePolicy(sizePolicy)
        self.TotalProgressBar.setProperty("value", 50)
        self.TotalProgressBar.setObjectName("TotalProgressBar")
        self.ProcessingProgressBars.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.TotalProgressBar
        )
        self.ProcessingVideoFrame = QtWidgets.QFrame(parent=self.Processing)
        self.ProcessingVideoFrame.setGeometry(QtCore.QRect(100, 10, 601, 401))
        self.ProcessingVideoFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ProcessingVideoFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.ProcessingVideoFrame.setObjectName("ProcessingVideoFrame")
        self.layoutWidget2 = QtWidgets.QWidget(parent=self.Processing)
        self.layoutWidget2.setGeometry(QtCore.QRect(300, 420, 191, 61))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.ProcessingVideoButtons = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.ProcessingVideoButtons.setContentsMargins(0, 0, 0, 0)
        self.ProcessingVideoButtons.setObjectName("ProcessingVideoButtons")
        self.ProcessingPreviousVideoButton = QtWidgets.QPushButton(
            parent=self.layoutWidget2
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProcessingPreviousVideoButton.sizePolicy().hasHeightForWidth()
        )
        self.ProcessingPreviousVideoButton.setSizePolicy(sizePolicy)
        self.ProcessingPreviousVideoButton.setMaximumSize(QtCore.QSize(41, 41))
        self.ProcessingPreviousVideoButton.setText("")
        self.ProcessingPreviousVideoButton.setIconSize(QtCore.QSize(20, 20))
        self.ProcessingPreviousVideoButton.setObjectName(
            "ProcessingPreviousVideoButton"
        )
        self.ProcessingVideoButtons.addWidget(self.ProcessingPreviousVideoButton)
        self.ProcessingPlayButton = QtWidgets.QPushButton(parent=self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProcessingPlayButton.sizePolicy().hasHeightForWidth()
        )
        self.ProcessingPlayButton.setSizePolicy(sizePolicy)
        self.ProcessingPlayButton.setMaximumSize(QtCore.QSize(41, 41))
        self.ProcessingPlayButton.setText("")
        self.ProcessingPlayButton.setIconSize(QtCore.QSize(20, 20))
        self.ProcessingPlayButton.setObjectName("ProcessingPlayButton")
        self.ProcessingVideoButtons.addWidget(self.ProcessingPlayButton)
        self.ProcessingNextVideoButton = QtWidgets.QPushButton(
            parent=self.layoutWidget2
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProcessingNextVideoButton.sizePolicy().hasHeightForWidth()
        )
        self.ProcessingNextVideoButton.setSizePolicy(sizePolicy)
        self.ProcessingNextVideoButton.setMaximumSize(QtCore.QSize(41, 41))
        self.ProcessingNextVideoButton.setText("")
        self.ProcessingNextVideoButton.setIconSize(QtCore.QSize(20, 20))
        self.ProcessingNextVideoButton.setObjectName("ProcessingNextVideoButton")
        self.ProcessingVideoButtons.addWidget(self.ProcessingNextVideoButton)
        self.ProcessingVolumeButton = QtWidgets.QPushButton(parent=self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProcessingVolumeButton.sizePolicy().hasHeightForWidth()
        )
        self.ProcessingVolumeButton.setSizePolicy(sizePolicy)
        self.ProcessingVolumeButton.setMaximumSize(QtCore.QSize(41, 41))
        self.ProcessingVolumeButton.setText("")
        self.ProcessingVolumeButton.setIconSize(QtCore.QSize(20, 20))
        self.ProcessingVolumeButton.setObjectName("ProcessingVolumeButton")
        self.ProcessingVideoButtons.addWidget(self.ProcessingVolumeButton)
        self.layoutWidget3 = QtWidgets.QWidget(parent=self.Processing)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 428, 271, 91))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.ProcessingInfoLabels = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.ProcessingInfoLabels.setContentsMargins(0, 0, 0, 0)
        self.ProcessingInfoLabels.setObjectName("ProcessingInfoLabels")
        self.ProcessingTimeUsageLabel = QtWidgets.QLabel(parent=self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(12)
        self.ProcessingTimeUsageLabel.setFont(font)
        self.ProcessingTimeUsageLabel.setObjectName("ProcessingTimeUsageLabel")
        self.ProcessingInfoLabels.addWidget(self.ProcessingTimeUsageLabel)
        self.ProcessingCurrentMethodLabel = QtWidgets.QLabel(parent=self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(12)
        self.ProcessingCurrentMethodLabel.setFont(font)
        self.ProcessingCurrentMethodLabel.setObjectName("ProcessingCurrentMethodLabel")
        self.ProcessingInfoLabels.addWidget(self.ProcessingCurrentMethodLabel)
        self.ProcessingCurrentDataLabel = QtWidgets.QLabel(parent=self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(12)
        self.ProcessingCurrentDataLabel.setFont(font)
        self.ProcessingCurrentDataLabel.setObjectName("ProcessingCurrentDataLabel")
        self.ProcessingInfoLabels.addWidget(self.ProcessingCurrentDataLabel)
        self.Widgets.addWidget(self.Processing)
        self.Results = QtWidgets.QWidget()
        self.Results.setObjectName("Results")
        self.ResultTextBrowser = QtWidgets.QTextBrowser(parent=self.Results)
        self.ResultTextBrowser.setGeometry(QtCore.QRect(10, 60, 351, 531))
        self.ResultTextBrowser.setObjectName("ResultTextBrowser")
        self.ResultTitle = QtWidgets.QLabel(parent=self.Results)
        self.ResultTitle.setGeometry(QtCore.QRect(10, 10, 271, 41))
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        font.setPointSize(14)
        self.ResultTitle.setFont(font)
        self.ResultTitle.setScaledContents(True)
        self.ResultTitle.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.ResultTitle.setWordWrap(True)
        self.ResultTitle.setObjectName("ResultTitle")
        self.layoutWidget_3 = QtWidgets.QWidget(parent=self.Results)
        self.layoutWidget_3.setGeometry(QtCore.QRect(390, 530, 404, 61))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.ResultBottomButtons = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.ResultBottomButtons.setContentsMargins(0, 0, 0, 0)
        self.ResultBottomButtons.setObjectName("ResultBottomButtons")
        self.ResultPreviousDataButton = QtWidgets.QPushButton(
            parent=self.layoutWidget_3
        )
        self.ResultPreviousDataButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ResultPreviousDataButton.setObjectName("ResultPreviousDataButton")
        self.ResultBottomButtons.addWidget(self.ResultPreviousDataButton)
        self.ResultNextDataButton = QtWidgets.QPushButton(parent=self.layoutWidget_3)
        self.ResultNextDataButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ResultNextDataButton.setObjectName("ResultNextDataButton")
        self.ResultBottomButtons.addWidget(self.ResultNextDataButton)
        self.ResultNextButton = QtWidgets.QPushButton(parent=self.layoutWidget_3)
        self.ResultNextButton.setMinimumSize(QtCore.QSize(130, 50))
        self.ResultNextButton.setObjectName("ResultNextButton")
        self.ResultBottomButtons.addWidget(self.ResultNextButton)
        self.ResultDiagram = QtWidgets.QLabel(parent=self.Results)
        self.ResultDiagram.setEnabled(True)
        self.ResultDiagram.setGeometry(QtCore.QRect(370, 20, 421, 377))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ResultDiagram.sizePolicy().hasHeightForWidth()
        )
        self.ResultDiagram.setSizePolicy(sizePolicy)
        self.ResultDiagram.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.ResultDiagram.setScaledContents(True)
        self.ResultDiagram.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ResultDiagram.setObjectName("ResultDiagram")
        self.layoutWidget4 = QtWidgets.QWidget(parent=self.Results)
        self.layoutWidget4.setGeometry(QtCore.QRect(370, 400, 421, 90))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.ResultDiagramControl = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.ResultDiagramControl.setContentsMargins(0, 0, 0, 0)
        self.ResultDiagramControl.setSpacing(0)
        self.ResultDiagramControl.setObjectName("ResultDiagramControl")
        self.ResultDiagramMethodLabel = QtWidgets.QLabel(parent=self.layoutWidget4)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.ResultDiagramMethodLabel.setFont(font)
        self.ResultDiagramMethodLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ResultDiagramMethodLabel.setObjectName("ResultDiagramMethodLabel")
        self.ResultDiagramControl.addWidget(self.ResultDiagramMethodLabel)
        self.ResultDiagramULayout = QtWidgets.QHBoxLayout()
        self.ResultDiagramULayout.setSpacing(0)
        self.ResultDiagramULayout.setObjectName("ResultDiagramULayout")
        self.ResultDiagramUpButton = QtWidgets.QToolButton(parent=self.layoutWidget4)
        self.ResultDiagramUpButton.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setFamily("3ds")
        self.ResultDiagramUpButton.setFont(font)
        self.ResultDiagramUpButton.setText("")
        self.ResultDiagramUpButton.setAutoRaise(False)
        self.ResultDiagramUpButton.setArrowType(QtCore.Qt.ArrowType.UpArrow)
        self.ResultDiagramUpButton.setObjectName("ResultDiagramUpButton")
        self.ResultDiagramULayout.addWidget(self.ResultDiagramUpButton)
        self.ResultDiagramControl.addLayout(self.ResultDiagramULayout)
        self.ResultDiagramMLayout = QtWidgets.QHBoxLayout()
        self.ResultDiagramMLayout.setSpacing(5)
        self.ResultDiagramMLayout.setObjectName("ResultDiagramMLayout")
        self.ResultDiagramLeftButton = QtWidgets.QToolButton(parent=self.layoutWidget4)
        self.ResultDiagramLeftButton.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setFamily("3ds")
        self.ResultDiagramLeftButton.setFont(font)
        self.ResultDiagramLeftButton.setText("")
        self.ResultDiagramLeftButton.setAutoRaise(False)
        self.ResultDiagramLeftButton.setArrowType(QtCore.Qt.ArrowType.LeftArrow)
        self.ResultDiagramLeftButton.setObjectName("ResultDiagramLeftButton")
        self.ResultDiagramMLayout.addWidget(self.ResultDiagramLeftButton)
        self.ResultDiagramTitle = QtWidgets.QLabel(parent=self.layoutWidget4)
        self.ResultDiagramTitle.setFrameShape(QtWidgets.QFrame.Shape.WinPanel)
        self.ResultDiagramTitle.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.ResultDiagramTitle.setScaledContents(True)
        self.ResultDiagramTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ResultDiagramTitle.setObjectName("ResultDiagramTitle")
        self.ResultDiagramMLayout.addWidget(self.ResultDiagramTitle)
        self.ResultDiagramRightButton = QtWidgets.QToolButton(parent=self.layoutWidget4)
        self.ResultDiagramRightButton.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setFamily("3ds")
        self.ResultDiagramRightButton.setFont(font)
        self.ResultDiagramRightButton.setText("")
        self.ResultDiagramRightButton.setAutoRaise(False)
        self.ResultDiagramRightButton.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        self.ResultDiagramRightButton.setObjectName("ResultDiagramRightButton")
        self.ResultDiagramMLayout.addWidget(self.ResultDiagramRightButton)
        self.ResultDiagramControl.addLayout(self.ResultDiagramMLayout)
        self.ResultDiagramDLayout = QtWidgets.QHBoxLayout()
        self.ResultDiagramDLayout.setSpacing(0)
        self.ResultDiagramDLayout.setObjectName("ResultDiagramDLayout")
        self.ResultDiagramDownButton = QtWidgets.QToolButton(parent=self.layoutWidget4)
        self.ResultDiagramDownButton.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setFamily("3ds")
        self.ResultDiagramDownButton.setFont(font)
        self.ResultDiagramDownButton.setText("")
        self.ResultDiagramDownButton.setAutoRaise(False)
        self.ResultDiagramDownButton.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        self.ResultDiagramDownButton.setObjectName("ResultDiagramDownButton")
        self.ResultDiagramDLayout.addWidget(self.ResultDiagramDownButton)
        self.ResultDiagramControl.addLayout(self.ResultDiagramDLayout)
        self.ResultStandardComboBox = QtWidgets.QComboBox(parent=self.Results)
        self.ResultStandardComboBox.setGeometry(QtCore.QRect(290, 30, 68, 22))
        self.ResultStandardComboBox.setObjectName("ResultStandardComboBox")
        self.staticLabel6 = QtWidgets.QLabel(parent=self.Results)
        self.staticLabel6.setGeometry(QtCore.QRect(290, 10, 71, 16))
        self.staticLabel6.setObjectName("staticLabel6")
        self.Widgets.addWidget(self.Results)
        MainWindow.setCentralWidget(self.mainWindowWidget)

        self.retranslateUi(MainWindow)
        self.Widgets.setCurrentIndex(0)
        self.ProgramSettingButton.clicked.connect(MainWindow.openProgramSettingDialog)  # type: ignore
        self.ReadDataTreeView.clicked["QModelIndex"].connect(MainWindow.readDataTreeViewClicked)  # type: ignore
        self.ShowPreprocessOptionsButton.clicked.connect(MainWindow.openPreprocessSettingDialog)  # type: ignore
        self.ResultNextButton.clicked.connect(MainWindow.returnToMainMenu)  # type: ignore
        self.ReadDataButton.clicked.connect(MainWindow.readDataButtonClicked)  # type: ignore
        self.ExitButton.clicked.connect(MainWindow.close)  # type: ignore
        self.ReadDataNextButton.clicked.connect(MainWindow.readDataNextButtonClicked)  # type: ignore
        self.ProcessSettingNextButton.clicked.connect(MainWindow.processSettingNextButtonClicked)  # type: ignore
        self.ProcessingPreviousVideoButton.clicked.connect(MainWindow.previousVideo)  # type: ignore
        self.ProcessingNextVideoButton.clicked.connect(MainWindow.nextVideo)  # type: ignore
        self.ProcessingPlayButton.clicked.connect(MainWindow.processingPlayButtonClicked)  # type: ignore
        self.ProcessingVolumeButton.clicked.connect(MainWindow.processingVolumeButtonClicked)  # type: ignore
        self.ProcessingNextButton.clicked.connect(MainWindow.processingNextButtonClicked)  # type: ignore
        self.ResultDiagramRightButton.clicked.connect(MainWindow.resultDiagramRightButtonClicked)  # type: ignore
        self.ResultDiagramLeftButton.clicked.connect(MainWindow.resultDiagramLeftButtonClicked)  # type: ignore
        self.ResultDiagramUpButton.clicked.connect(MainWindow.resultDiagramUpButtonClicked)  # type: ignore
        self.ResultDiagramDownButton.clicked.connect(MainWindow.resultDiagramDownButtonClicked)  # type: ignore
        self.ResultStandardComboBox.currentIndexChanged["int"].connect(MainWindow.resultStandardComboboxChanged)  # type: ignore
        self.ResultPreviousDataButton.clicked.connect(MainWindow.resultPreviousDataButtonClicked)  # type: ignore
        self.ResultNextDataButton.clicked.connect(MainWindow.resultNextDataButtonClicked)  # type: ignore
        self.ReadDataBackButton.clicked.connect(MainWindow.readDataBackButtonClicked)  # type: ignore
        self.ProcessSettingBackButton.clicked.connect(MainWindow.processSettingBackButtonClicked)  # type: ignore
        self.ProcessSettingPreviousDataButton.clicked.connect(MainWindow.processSettingPreviousDataButtonClicked)  # type: ignore
        self.ProcessSettingNextDataButton.clicked.connect(MainWindow.processSettingNextDataButtonClicked)  # type: ignore
        self.RingCountSpinBox.valueChanged["int"].connect(MainWindow.updateRingCount)  # type: ignore
        self.BoundsTable.cellChanged["int", "int"].connect(MainWindow.updateBoundType)  # type: ignore
        self.MethodSelectAllCheckBox.clicked.connect(MainWindow.processSettingMethodSelectAllCheckBoxClicked)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.ReadDataButton, self.ProgramSettingButton)
        MainWindow.setTabOrder(self.ProgramSettingButton, self.ExitButton)
        MainWindow.setTabOrder(self.ExitButton, self.ReadDataTreeView)
        MainWindow.setTabOrder(self.ReadDataTreeView, self.ReadDataBackButton)
        MainWindow.setTabOrder(self.ReadDataBackButton, self.ReadDataNextButton)
        MainWindow.setTabOrder(self.ReadDataNextButton, self.RingCountSpinBox)
        MainWindow.setTabOrder(self.RingCountSpinBox, self.BoundsTable)
        MainWindow.setTabOrder(self.BoundsTable, self.PreprocessDataCheckBox)
        MainWindow.setTabOrder(
            self.PreprocessDataCheckBox, self.ShowPreprocessOptionsButton
        )
        MainWindow.setTabOrder(
            self.ShowPreprocessOptionsButton, self.MethodSelectAllCheckBox
        )
        MainWindow.setTabOrder(self.MethodSelectAllCheckBox, self.MethodsTable)
        MainWindow.setTabOrder(self.MethodsTable, self.ProcessSettingPreviousDataButton)
        MainWindow.setTabOrder(
            self.ProcessSettingPreviousDataButton, self.ProcessSettingNextDataButton
        )
        MainWindow.setTabOrder(
            self.ProcessSettingNextDataButton, self.ProcessSettingBackButton
        )
        MainWindow.setTabOrder(
            self.ProcessSettingBackButton, self.ProcessSettingNextButton
        )
        MainWindow.setTabOrder(
            self.ProcessSettingNextButton, self.ProcessingPreviousVideoButton
        )
        MainWindow.setTabOrder(
            self.ProcessingPreviousVideoButton, self.ProcessingPlayButton
        )
        MainWindow.setTabOrder(
            self.ProcessingPlayButton, self.ProcessingNextVideoButton
        )
        MainWindow.setTabOrder(
            self.ProcessingNextVideoButton, self.ProcessingVolumeButton
        )
        MainWindow.setTabOrder(self.ProcessingVolumeButton, self.ProcessingNextButton)
        MainWindow.setTabOrder(self.ProcessingNextButton, self.ResultTextBrowser)
        MainWindow.setTabOrder(self.ResultTextBrowser, self.ResultStandardComboBox)
        MainWindow.setTabOrder(
            self.ResultStandardComboBox, self.ResultDiagramLeftButton
        )
        MainWindow.setTabOrder(
            self.ResultDiagramLeftButton, self.ResultDiagramRightButton
        )
        MainWindow.setTabOrder(
            self.ResultDiagramRightButton, self.ResultDiagramUpButton
        )
        MainWindow.setTabOrder(self.ResultDiagramUpButton, self.ResultDiagramDownButton)
        MainWindow.setTabOrder(
            self.ResultDiagramDownButton, self.ResultPreviousDataButton
        )
        MainWindow.setTabOrder(self.ResultPreviousDataButton, self.ResultNextDataButton)
        MainWindow.setTabOrder(self.ResultNextDataButton, self.ResultNextButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EIS程序嘻嘻"))
        self.TitlePic.setText(_translate("MainWindow", "Title Here"))
        self.CornerPic.setText(_translate("MainWindow", "Corner Gif Here"))
        self.VersionText.setText(_translate("MainWindow", "Version 1.1.0"))
        self.ReadDataButton.setText(_translate("MainWindow", "读取数据"))
        self.ProgramSettingButton.setText(_translate("MainWindow", "程序设置"))
        self.ExitButton.setText(_translate("MainWindow", "退出"))
        self.ReadDataDiagramPic.setText(
            _translate("MainWindow", "ReadData Diagram Here")
        )
        self.ReadDataBackButton.setText(_translate("MainWindow", "返回"))
        self.ReadDataNextButton.setText(_translate("MainWindow", "下一步"))
        self.ReadDataHighlightFileName.setText(_translate("MainWindow", "选中的文件："))
        self.ReadDataProcessingDRTLabel.setText(
            _translate("MainWindow", "正在生成所选数据的DRT数据")
        )
        self.DRTDiagramPic.setText(
            _translate("MainWindow", "ProcessSetting Diagram Here")
        )
        self.ProcessSettingBackButton.setText(_translate("MainWindow", "返回"))
        self.ProcessSettingNextButton.setText(_translate("MainWindow", "下一步"))
        self.DataNameLabel.setText(_translate("MainWindow", "*插入数据名称*:"))
        self.staticLabel3.setText(_translate("MainWindow", "拟合参数范围："))
        self.ProcessSettingInfoTextBoxPic.setText(
            _translate("MainWindow", "InFoTextBox Here")
        )
        self.BoundsTable.setSortingEnabled(False)
        item = self.BoundsTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "RCircuit"))
        item = self.BoundsTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Rs"))
        item = self.BoundsTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "L"))
        item = self.BoundsTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Beta"))
        item = self.BoundsTable.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "R"))
        item = self.BoundsTable.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "C"))
        item = self.BoundsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "最小值"))
        item = self.BoundsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "最大值"))
        __sortingEnabled = self.BoundsTable.isSortingEnabled()
        self.BoundsTable.setSortingEnabled(False)
        self.BoundsTable.setSortingEnabled(__sortingEnabled)
        self.staticLabel1.setText(_translate("MainWindow", "反应环数量："))
        self.ProcessSettingInfoText.setText(
            _translate(
                "MainWindow", "这是测试文字，用来测试长度非常非常非常长的时候会怎么样。"
            )
        )
        self.PreprocessDataCheckBox.setText(_translate("MainWindow", "数据预处理："))
        self.ShowPreprocessOptionsButton.setText(
            _translate("MainWindow", "查看预处理选项")
        )
        self.MethodsTable.setSortingEnabled(False)
        self.MethodSelectAllCheckBox.setText(_translate("MainWindow", "拟合算法：全选"))
        self.staticLabel2.setText(_translate("MainWindow", "切换数据"))
        self.ProcessingNextButton.setText(_translate("MainWindow", "下一步"))
        self.staticLabel4.setText(_translate("MainWindow", "当前数据进度："))
        self.staticLabel5.setText(_translate("MainWindow", "总进度："))
        self.ProcessingTimeUsageLabel.setText(
            _translate("MainWindow", "已用时：99:99:99")
        )
        self.ProcessingCurrentMethodLabel.setText(
            _translate("MainWindow", "当前算法：BRUTE FORCE ALL THE WAY")
        )
        self.ProcessingCurrentDataLabel.setText(
            _translate("MainWindow", "当前数据：HinanawiTenshi.txt")
        )
        self.ResultTitle.setText(_translate("MainWindow", "XXX拟合结果："))
        self.ResultPreviousDataButton.setText(_translate("MainWindow", "上一个数据"))
        self.ResultNextDataButton.setText(_translate("MainWindow", "下一个数据"))
        self.ResultNextButton.setText(_translate("MainWindow", "返回主界面"))
        self.ResultDiagram.setText(_translate("MainWindow", "Result Diagram Here"))
        self.ResultDiagramMethodLabel.setText(
            _translate("MainWindow", "排名999: 瞪眼法")
        )
        self.ResultDiagramTitle.setText(_translate("MainWindow", "图片名字"))
        self.staticLabel6.setText(_translate("MainWindow", "排序标准："))

    def customUIs(self):
        # Main Menu
        self.TitlePic.setText("")
        self.TitlePic.setPixmap(QtGui.QPixmap(UIMainResourceDir + "MainTitle.jpg"))
        self.CornerPic.setText("")
        movie = QtGui.QMovie()
        movie.setFileName(UIMainResourceDir + "MainCorner.gif")
        self.CornerPic.setMovie(movie)
        movie.start()

        # Read Data
        self.ReadDataDiagramPic.setText("")
        self.ReadDataDiagramPic.setPixmap(
            QtGui.QPixmap(UIReadDatasResourceDir + "DataDiagramTemplate.jpg")
        )

        # Process Settings
        self.DRTDiagramPic.setText("")
        self.DRTDiagramPic.setPixmap(
            QtGui.QPixmap(UIProcessSettingsResourceDir + "DRTTemplate.jpg")
        )
        self.ProcessSettingInfoTextBoxPic.setText("")
        self.ProcessSettingInfoTextBoxPic.setPixmap(
            QtGui.QPixmap(UIProcessSettingsResourceDir + "InfoTextBox.png")
        )

        # Processing
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(UIProcessingButtonIconDir + "previous.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.ProcessingPreviousVideoButton.setIcon(icon)
        self.playIcon = QtGui.QIcon()
        self.playIcon.addPixmap(
            QtGui.QPixmap(UIProcessingButtonIconDir + "play.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.pauseIcon = QtGui.QIcon()
        self.pauseIcon.addPixmap(
            QtGui.QPixmap(UIProcessingButtonIconDir + "pause.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.ProcessingPlayButton.setIcon(self.pauseIcon)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(UIProcessingButtonIconDir + "next.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.ProcessingNextVideoButton.setIcon(icon)
        self.muteIcon = QtGui.QIcon()
        self.muteIcon.addPixmap(
            QtGui.QPixmap(UIProcessingButtonIconDir + "mute.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.unmuteIcon = QtGui.QIcon()
        self.unmuteIcon.addPixmap(
            QtGui.QPixmap(UIProcessingButtonIconDir + "unmute.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.ProcessingVolumeButton.setIcon(self.unmuteIcon)

        # Result
        self.ResultDiagram.setText("")
        self.ResultDiagram.setPixmap(
            QtGui.QPixmap(UISaveResultResourceDir + "DataDiagramTemplate.jpg")
        )

    def setupComponents(self):
        self.customUIs()

        # Have To Do This In Here(AKA After The Signals Connected)
        # Not To Do It In The Classes' Initialize
        # Welp, Moved To The Beginning Of Each Pages

        self.ProcessingVideoLayout = QtWidgets.QVBoxLayout(self.ProcessingVideoFrame)
        self.ProcessingVideoLayout.setContentsMargins(0, 0, 0, 0)

        self.returnToMainMenu()

    def setupSubWidgets(self):
        self.programSettingDialog = ProgramSettingsDialog()
        self.preprocessSettingDialog = PreprocessSettingDialog()
        self.processDataThread = ProcessDataThread()

        self.programSettingDialog.settingsSignal.connect(self.receiveSettings)
        self.preprocessSettingDialog.preprocessorInfoSignal.connect(
            self.receivePreprocessInfo
        )
        self.processDataThread.progressBarUpdateSignal.connect(self.updateProgressBars)
        self.processDataThread.currentDataNameUpdateSignal.connect(
            self.updateCurrentDataName
        )
        self.processDataThread.currentMethodNameUpdateSignal.connect(
            self.updateCurrentMethodName
        )
        self.processDataThread.finishedProcessingSignal.connect(self.finishedProcessing)

    # Window Controls
    def raiseWindowToFront(self):
        if self.isMinimized():
            self.showNormal()
        self.activateWindow()

    # Pages Controls
    def changePage(self, index: int):
        self.Widgets.setCurrentIndex(index)

    def changeToNextPage(self):
        index = self.Widgets.currentIndex()
        self.changePage(index + 1)

    def changeToPreviousPage(self):
        index = self.Widgets.currentIndex()
        self.changePage(index - 1)

    def returnToMainMenu(self):
        self.initializeMainMenu()
        self.changePage(0)

    # Main Menu
    def initializeMainMenu(self):
        self.setupSubWidgets()

        print("\n---Switching To Main Menu Page---")
        self.programSettingDialog.emitSettings()
        self.CornerPic.movie().jumpToFrame(0)

    def openProgramSettingDialog(self):
        self.programSettingDialog.setupComponents()
        self.programSettingDialog.show()

    def receiveSettings(self, settings):
        print("Settings Received by Main!")
        dirs, multiThread, DRTSettings = settings

        IO.dirs = dirs
        if DRTSettings["Overwrite DRT Data"] == "Yes":
            self.overwriteDRTData = True
        else:
            self.overwriteDRTData = False

    def readDataButtonClicked(self):
        invalidDir = False

        dialog = self.programSettingDialog
        dirSetting = dialog.settings[0]
        for key, dir in IO.dirs.items():
            if not os.path.isdir(dir):
                invalidDir = True

                defaultDir = IO.defaultDirs[key]
                dirSetting[key] = defaultDir
                if not os.path.exists(defaultDir):
                    os.makedirs(defaultDir)

        if invalidDir:
            QtWidgets.QMessageBox.warning(
                self, "小提示", "程序设置里有无效路径，已重置为默认路径"
            )
            dialog.emitSettings()
            dialog.writeSettings()
            dialog.updateUIs()

        self.initializeReadDataPage()
        self.changeToNextPage()

    # Read Data
    def initializeReadDataPage(self):
        print("\n---Switching To Read Data Page---")
        self.hasValidData = False

        self.ReadDataBackButton.setEnabled(True)
        self.ReadDataNextButton.setEnabled(True)
        self.ReadDataTreeView.setEnabled(True)
        self.ReadDataProcessingDRTLabel.setText("")
        self.ReadDataHighlightFileName.setText(
            "小贴士：点击文件夹可以快速选择里面的所有文件"
        )
        self.ReadDataDiagramPic.setPixmap(
            QtGui.QPixmap(UIReadDatasResourceDir + "DataDiagramTemplate.jpg")
        )

        self.initializeDataTreeView()

    def initializeDataTreeView(self):
        self.dataModel = QtGui.QFileSystemModel()
        self.dataModel.setRootPath("")
        self.ReadDataTreeView.setModel(self.dataModel)
        self.ReadDataTreeView.setRootIndex(self.dataModel.index(IO.dirs["Data Dir"]))
        self.ReadDataTreeView.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
        )

    def readDataTreeViewClicked(self, index):
        tree = self.ReadDataTreeView
        model = self.dataModel

        path = model.filePath(index)
        name = os.path.basename(path)
        text = f"点击的项目：{name}\n"

        # Deselect Folder And Select Its Child
        for i in tree.selectedIndexes():
            if model.isDir(i):
                tree.selectionModel().select(
                    i, QtCore.QItemSelectionModel.SelectionFlag.Deselect
                )

                childCount = model.rowCount(i)
                for row in range(childCount):
                    childIndex = model.index(row, 0, i)
                    if not model.isDir(childIndex):
                        tree.selectionModel().select(
                            childIndex, QtCore.QItemSelectionModel.SelectionFlag.Select
                        )

        # Deselect Invaild Data
        for i in tree.selectedIndexes():
            filePath = model.filePath(i)
            fileName = os.path.basename(filePath)
            dataName, ext = os.path.splitext(fileName)

            if ext not in IO.supportedDataExts:
                print(f"Unsupport Extension：{fileName}")
                tree.selectionModel().select(
                    i, QtCore.QItemSelectionModel.SelectionFlag.Deselect
                )

        # Get File Paths
        filePaths = []
        for i in tree.selectedIndexes():
            filePaths.append(model.filePath(i))
        filePaths = set(filePaths)

        # Get Datas And Prepare Paths For DRT Tool
        datas = []
        dataNames = []
        DRTInputPaths = []
        for filePath in filePaths:
            if os.path.isfile(filePath):
                fileName = os.path.basename(filePath)
                dataName, ext = os.path.splitext(fileName)
                relativePath = os.path.relpath(filePath, IO.dirs["Data Dir"])

                data = IO.ReadData(relativePath)

                datas.append(data)
                dataNames.append(dataName)
                DRTInputPaths.append(filePath)

        DRTOutputPaths = []
        for dataName in dataNames:
            outputName = dataName + ".txt"
            basePath = os.path.abspath(IO.dirs["DRT Data Dir"])
            outputPath = os.path.join(basePath, outputName)
            DRTOutputPaths.append(outputPath)

        # Fail Safe
        dataCounts = len(datas)
        if dataCounts == 0:
            text += "请选择有效的文件\n"
            self.ReadDataHighlightFileName.setText(text)
            self.ReadDataDiagramPic.setPixmap(
                QtGui.QPixmap(UIReadDatasResourceDir + "DataDiagramTemplate.jpg")
            )
            self.hasValidData = False
            return

        # Draw Latest Clicked Data's Diagram
        lastData = np.copy(datas[-1])
        lastDataName = dataNames[-1]

        if (index in tree.selectedIndexes()) and (not model.isDir(index)):
            filePath = model.filePath(index)
            fileName = os.path.basename(filePath)
            dataName, ext = os.path.splitext(fileName)

            if ext in IO.supportedDataExts:
                relativePath = os.path.relpath(filePath, IO.dirs["Data Dir"])

                lastData = IO.ReadData(relativePath)
                lastDataName = dataName

        try:
            picPath = DrawDiagram.DrawNyquistDigram(
                dataImpedances=[lastData["impedance"]],
                title=lastDataName,
                temp=True,
            )
            self.ReadDataDiagramPic.setPixmap(QtGui.QPixmap(picPath))
        except Exception as e:
            text += f"绘图失败: {str(e)}\n"
            self.ReadDataDiagramPic.setPixmap(
                QtGui.QPixmap(UIReadDatasResourceDir + "DataDiagramTemplate.jpg")
            )

        if dataCounts > 1:
            text += f"选中{dataCounts}个文件\n小提示：选择多个文件后会禁用预处理（因为效果不好（而且我懒得修了））"

        self.ReadDataHighlightFileName.setText(text)

        self.hasValidData = True
        self.processDataThread.datas = datas
        self.processDataThread.dataNames = dataNames

        IO.runDRT(DRTInputPaths, DRTOutputPaths, self.overwriteDRTData)

    def runDRTTool(self):
        DRTToolScriptPath = os.path.abspath(IO.dirs["DRT Tool Dir"])
        DRTToolScriptPath = os.path.join(DRTToolScriptPath, "DRTtools.m")
        try:
            matlabCommand = (
                f"matlab -nosplash -nodesktop -r \"run('{DRTToolScriptPath}'); exit;\""
            )
            print(f"Running MATLAB command: {matlabCommand}")
            result = subprocess.run(
                matlabCommand.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

            if result.stderr:
                print("DRT Tool Script Errors:")
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the DRT Tool Script: {e}")
            print(e.stderr)

    def readDataBackButtonClicked(self):
        self.returnToMainMenu()

    def readDataNextButtonClicked(self):
        if self.hasValidData:
            datas = self.processDataThread.datas
            dataNames = self.processDataThread.dataNames

            dataNames, datas = zip(*sorted(zip(dataNames, datas)))

            self.processDataThread.datas = datas
            self.processDataThread.dataNames = dataNames
            self.processDataThread.ogDatas = datas

            self.ReadDataBackButton.setEnabled(False)
            self.ReadDataNextButton.setEnabled(False)
            self.ReadDataTreeView.setEnabled(False)
            self.ReadDataProcessingDRTLabel.setText("生成所选数据的DRT数据...")
            self.ReadDataHighlightFileName.setText("启动Matlab巨慢无比，请耐心等待")
            movie = QtGui.QMovie()
            movie.setFileName(UIReadDatasResourceDir + "DRTLoading.gif")
            self.ReadDataDiagramPic.setMovie(movie)
            movie.start()

            flagPath = os.path.abspath(IO.dirs["DRT Tool Dir"])
            flagPath = os.path.join(flagPath, "flag.txt")

            # Read Flag To See If Need To Run The Tool
            with open(flagPath, "r") as file:
                flag = file.readline().strip()

            print(flag)
            if flag == "Rejected Takeoff!":
                self.changeToProcessSettingPage()
            else:
                self.runDRTTool()

                self.readDRTToolStateThread = ReadDRTToolStateThread(flagPath, 0.1)
                self.readDRTToolStateThread.DRTToolFinishedSignal.connect(
                    self.changeToProcessSettingPage
                )

                # Because That Thing's So Slow And Pathetic
                # It Can't Even Clean The Flag Itself Before My Python Code
                # So We Gotta Wipe Its Ass For It
                with open(flagPath, "w") as file:
                    file.write("Processing")

                self.readDRTToolStateThread.start()
        else:
            QtWidgets.QMessageBox.warning(
                self, "出错了", "未选择有效的实验数据！(有效的话右边会有示意图)"
            )
            # print("Pick a card, any card")

    def changeToProcessSettingPage(self):
        print("DRT Tool Finished!")

        self.initializeProcessSettingsPage()
        self.changeToNextPage()

        self.raiseWindowToFront()

    # Process Settings
    def initializeProcessSettingsPage(self):
        print("\n---Switching To Process Settings Page---")
        self.preprocessSettingDialog.emitPreprocessorInfo()

        thread = self.processDataThread

        constCounts = 3
        variableBeta = True
        thread.paraFormat = [constCounts, None, variableBeta]

        self.populateDRTDatas()
        self.populateRingCounts()
        self.populateBoundTypes()

        if len(thread.datas) > 1:
            self.PreprocessDataCheckBox.setChecked(False)
            self.PreprocessDataCheckBox.setEnabled(False)
            self.ShowPreprocessOptionsButton.setEnabled(False)

        self.setupMethodsTable()
        self.DRTDiagramPic.setPixmap(
            QtGui.QPixmap(UIProcessSettingsResourceDir + "DRTTemplate.jpg")
        )

        self.processSettingDataIndex = 0
        self.updateProcessSettingsPage()

    def updateProcessSettingsPage(self):
        self.pageUpdating = True

        thread = self.processDataThread
        index = self.processSettingDataIndex
        dataName = thread.dataNames[index]

        self.DataNameLabel.setText(f"{dataName}：")

        infoText = ""
        if len(thread.datas) > 1:
            infoText += f"处理多个数据就没法太细节了，交给我搞定吧\n（其实也不是没法，只是太累了）\n"
        infoText += f"我觉得这个数据有{thread.ringCounts[index]}个反应环，你觉得呢？\n"
        try:
            picPath = DrawDiagram.DrawDRTDiagram(
                DRTData=thread.DRTDatas[index],
                title=dataName,
                temp=True,
            )
            self.DRTDiagramPic.setPixmap(QtGui.QPixmap(picPath))
        except Exception as e:
            infoText += f"绘图失败: {str(e)}\n"
            self.DRTDiagramPic.setPixmap(
                QtGui.QPixmap(UIProcessSettingsResourceDir + "DRTTemplate.jpg")
            )
        self.ProcessSettingInfoText.setText(infoText)

        self.updateRingCountSpinBox()
        self.updateBoundsTable()

        # Button Logics
        self.ProcessSettingPreviousDataButton.setEnabled(
            self.processSettingDataIndex > 0
        )
        self.ProcessSettingNextDataButton.setEnabled(
            self.processSettingDataIndex < len(thread.datas) - 1
        )

        self.pageUpdating = False

    def populateDRTDatas(self):
        thread = self.processDataThread

        thread.DRTDatas = []
        DRTDatas = thread.DRTDatas
        for dataName in thread.dataNames:
            try:
                DRTData = IO.ReadDRTData(dataName)
                DRTDatas.append(DRTData)
            except:
                print(f"{dataName}读取DRT数据失败")
                DRTDatas.append(None)

    def populateRingCounts(self):
        thread = self.processDataThread

        thread.ringCounts = []
        ringCounts = thread.ringCounts
        for dataName, DRTData in zip(thread.dataNames, thread.DRTDatas):
            if DRTData is not None:
                ringCounts.append(DataProcessor.GenerateRingCount(DRTData))
            else:
                print(f"{dataName}读取DRT数据失败，使用默认反应环数")
                ringCounts.append(Optimizer.defaultRingCount)

    def populateBoundTypes(self):
        thread = self.processDataThread

        thread.boundTypes = []
        boundTypes = thread.boundTypes
        for data in thread.datas:
            boundTypes.append(DataProcessor.GenerateBoundType(data))

    def setupMethodsTable(self):
        self.MethodsTable.setColumnCount(1)
        self.MethodsTable.setHorizontalHeaderLabels(["拟合算法"])
        self.MethodsTable.setRowCount(len(Optimizer.methodFullList) + 4)

        self.setupMethodCheckBoxes()
        self.methodSections["Fast"]["Check Box"].setChecked(True)

        self.updateMethodsTable()

    def setupMethodCheckBoxes(self):
        self.methodSections = {}

        methodDict = Optimizer.methodListDict
        titles = [
            "速度很快的算法",
            "速度一般的算法",
            "速度很慢的算法",
            "效果很烂的算法",
        ]
        row = 0
        for key, category, title in zip(methodDict.keys(), methodDict.values(), titles):
            sectionLength = len(category)

            checkbox = QtWidgets.QCheckBox(title)
            checkbox.clicked.connect(self.updateMethodsTable)

            centerWidget = CenteredWidget(checkbox)

            self.MethodsTable.setCellWidget(row, 0, centerWidget)
            self.methodSections[key] = {
                "Row": row,
                "Section Length": sectionLength,
                "Check Box": checkbox,
            }

            for method in category:
                row += 1
                checkbox = QtWidgets.QCheckBox(method)
                self.MethodsTable.setCellWidget(row, 0, checkbox)

                checkbox.setChecked(False)

            row += 1

    def readTableData(self, table: QtWidgets.QTableWidget) -> list[list]:
        rows = table.rowCount()
        cols = table.columnCount()

        data = []
        for row in range(rows):
            rowData = []
            for col in range(cols):
                item = table.item(row, col)
                if item:
                    rowData.append(item.text())
                else:
                    rowData.append("")  # 如果单元格为空，则添加空字符串
            data.append(rowData)

        return data

    def updateRingCountSpinBox(self):
        self.RingCountSpinBox.setValue(
            self.processDataThread.ringCounts[self.processSettingDataIndex]
        )

    def updateRingCount(self):
        if not self.pageUpdating:
            self.processDataThread.ringCounts[self.processSettingDataIndex] = (
                self.RingCountSpinBox.value()
            )
            # print(self.ringCounts)

    def updateBoundsTable(self):
        boundType = self.processDataThread.boundTypes[self.processSettingDataIndex]
        for row, (min, max) in enumerate(boundType.values()):
            minText = f"{min}"
            maxText = f"{max}"
            itemMin = QtWidgets.QTableWidgetItem(minText)
            itemMax = QtWidgets.QTableWidgetItem(maxText)
            self.BoundsTable.setItem(row, 0, itemMin)
            self.BoundsTable.setItem(row, 1, itemMax)

    def updateBoundType(self):
        if not self.pageUpdating:
            data = self.readTableData(self.BoundsTable)
            boundType = {}
            boundType["RCircuit"] = tuple([float(num) for num in data[0]])
            boundType["Rs"] = tuple([float(num) for num in data[1]])
            boundType["L"] = tuple([float(num) for num in data[2]])
            boundType["beta"] = tuple([float(num) for num in data[3]])
            boundType["R"] = tuple([float(num) for num in data[4]])
            boundType["C"] = tuple([float(num) for num in data[5]])

            self.processDataThread.boundTypes[self.processSettingDataIndex] = boundType
            # print(boundType)

    def processSettingMethodSelectAllCheckBoxClicked(self):
        state = self.MethodSelectAllCheckBox.isChecked()
        for methodSection in self.methodSections.values():
            checkBox = methodSection["Check Box"]
            checkBox.setChecked(state)

        self.updateMethodsTable()

    def updateMethodsTable(self):
        for methodSection in self.methodSections.values():
            row = methodSection["Row"] + 1
            length = methodSection["Section Length"]
            checkBox = methodSection["Check Box"]

            rows = [row + i for i in range(length)]
            state = checkBox.isChecked()

            self.selectMethods(rows, state)

    def selectMethods(self, rows: list[int], state: bool):
        for row in rows:
            checkbox = self.MethodsTable.cellWidget(row, 0)
            if isinstance(checkbox, QtWidgets.QCheckBox):
                checkbox.setChecked(state)

    def updateMethods(self):
        methods = []
        for row in range(self.MethodsTable.rowCount()):
            checkbox = self.MethodsTable.cellWidget(row, 0)
            if isinstance(checkbox, QtWidgets.QCheckBox) and checkbox.isChecked():
                method = checkbox.text()
                if method in Optimizer.methodFullList:
                    methods.append(method)

        self.processDataThread.hyperParameters[1] = methods
        # print("Methods:", self.methodList)

    def updateIsPreprocessData(self):
        self.processDataThread.preprocessData = self.PreprocessDataCheckBox.isChecked()

    def openPreprocessSettingDialog(self):
        self.preprocessSettingDialog.show()

    def receivePreprocessInfo(self, infos):
        # print("Received Preprocess Infos!")
        self.processDataThread.preprocessorInfo = infos

    def processSettingPreviousDataButtonClicked(self):
        if self.processSettingDataIndex > 0:
            self.processSettingDataIndex -= 1
            self.updateProcessSettingsPage()

    def processSettingNextDataButtonClicked(self):
        thread = self.processDataThread

        if self.processSettingDataIndex < len(thread.datas) - 1:
            self.processSettingDataIndex += 1
            self.updateProcessSettingsPage()

    def processSettingBackButtonClicked(self):
        self.initializeReadDataPage()
        self.changeToPreviousPage()

    def processSettingNextButtonClicked(self):
        self.updateMethods()
        self.updateIsPreprocessData()

        self.initializeProcessingPage()
        self.changeToNextPage()

    # Processing
    def initializeProcessingPage(self):
        print("\n---Switching To Processing Page---")

        self.pageInitializing = True

        self.updateProgressBars([0, 0])
        self.ProcessingNextButton.setEnabled(False)

        self.processingTimer = QtCore.QTimer(self)
        self.processingTimer.timeout.connect(self.updateProcessingTimeUsage)
        self.processingTime = 0

        # CRAZY FRICKING ICY VIDEOS!
        self.mediaPaths = []
        self.processingPlayer = None
        if hasMultiMedia:
            self.populateMediaPathsWithExtensions((".mp4", ".mkv", ".avi", ".mpg"))

            if len(self.mediaPaths) != 0:
                if self.ProcessingVideoLayout.count() != 0:
                    self.ProcessingVideoLayout.removeWidget(self.videoWidget)

                self.videoWidget = QVideoWidget()
                self.processingPlayer = QMediaPlayer()
                self.processingAudio = QAudioOutput()
                self.processingPlayer.setVideoOutput(self.videoWidget)
                self.processingPlayer.setAudioOutput(self.processingAudio)

                self.processingPlayer.mediaStatusChanged.connect(
                    self.processingPlayerMediaStatusChanged
                )

                self.ProcessingVideoLayout.addWidget(self.videoWidget)
        else:
            self.ProcessingVolumeButton.setEnabled(False)
            # Less crazy gifs
            self.populateMediaPathsWithExtensions((".gif"))

            if len(self.mediaPaths) != 0:
                if self.ProcessingVideoLayout.count() != 0:
                    self.ProcessingVideoLayout.removeWidget(self.processingVideoLabel)

                self.processingPlayer = QtGui.QMovie()
                self.processingVideoLabel = QtWidgets.QLabel()
                self.processingVideoLabel.setMovie(self.processingPlayer)
                self.processingVideoLabel.setScaledContents(True)

                self.ProcessingVideoLayout.addWidget(self.processingVideoLabel)

        if len(self.mediaPaths) == 0:
            print("没有找到多媒体文件:(")

            layout = self.ProcessingVideoButtons
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.widget() is not None:
                    if isinstance(item.widget(), QtWidgets.QPushButton):
                        item.widget().setEnabled(False)
        else:
            self.mediaIndex = random.randint(0, len(self.mediaPaths) - 1)
            self.updateMedia()

        # Backend stuff
        print()
        IO.cleanupDirectory(IO.dirs["Result Dir"])

        if not self.processDataThread.isRunning():
            self.processDataThread.start()
        print("\nProcess Thread Started:")

        # Update Every 10ms
        self.processingTimer.start(10)

        self.pageInitializing = False

    def populateMediaPathsWithExtensions(self, extensions: tuple[str]):
        dir = UIProcessingResourceDir
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                if file.endswith(extensions):
                    self.mediaPaths.append(os.path.join(dir, file))
        else:
            print("media folder not existed!")

    def updateProcessingTimeUsage(self):
        self.processingTime += 0.01
        timeUsageText = f"已用时：{self.processingTime:.2f}s"
        self.ProcessingTimeUsageLabel.setText(timeUsageText)

    def processingPlayerMediaStatusChanged(self):
        if self.processingPlayer.mediaStatus() == QMediaPlayer.MediaStatus.EndOfMedia:
            self.nextVideo()

    def updateMedia(self):
        mediaPath = self.mediaPaths[self.mediaIndex]
        player = self.processingPlayer
        if hasMultiMedia:
            playerOGState = player.playbackState()

            player.setSource(QtCore.QUrl(mediaPath))

            if self.pageInitializing:
                player.play()
                return

            if playerOGState == QMediaPlayer.PlaybackState.PausedState:
                player.pause()
            else:
                player.play()
        else:
            playerOGState = player.state()

            player.setPaused(True)
            player.setFileName(mediaPath)
            player.setPaused(False)

            if self.pageInitializing:
                player.setPaused(False)
                return

            if playerOGState == QtGui.QMovie.MovieState.Paused:
                player.setPaused(True)
            else:
                player.setPaused(False)

    def previousVideo(self):
        self.mediaIndex = (self.mediaIndex - 1) % len(self.mediaPaths)
        self.updateMedia()

    def nextVideo(self):
        self.mediaIndex = (self.mediaIndex + 1) % len(self.mediaPaths)
        self.updateMedia()

    def processingPlayButtonClicked(self):
        player = self.processingPlayer
        button = self.ProcessingPlayButton

        if hasMultiMedia:
            if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                player.pause()
                button.setIcon(self.playIcon)
            else:
                player.play()
                button.setIcon(self.pauseIcon)
        else:
            if player.state() == QtGui.QMovie.MovieState.Running:
                player.setPaused(True)
                button.setIcon(self.playIcon)
            else:
                player.setPaused(False)
                button.setIcon(self.pauseIcon)

    def processingVolumeButtonClicked(self):
        if not hasMultiMedia:
            return

        audio = self.processingAudio
        button = self.ProcessingVolumeButton

        if audio.isMuted():
            audio.setMuted(False)
            button.setIcon(self.unmuteIcon)
        else:
            audio.setMuted(True)
            button.setIcon(self.muteIcon)

    def updateProgressBars(self, progresses: list):
        # print("Receive ProgressBar Updates!")
        methodProgress, totalProgress = progresses

        self.CurrentMethodProgressBar.setValue(methodProgress)
        self.TotalProgressBar.setValue(totalProgress)

    def updateCurrentDataName(self, dataName: str):
        self.ProcessingCurrentDataLabel.setText(f"当前数据：{dataName}")

    def updateCurrentMethodName(self, methodName: str):
        self.ProcessingCurrentMethodLabel.setText(f"当前方法：{methodName}")

    def finishedProcessing(self):
        self.ProcessingNextButton.setEnabled(True)
        self.processingTimer.stop()

        self.raiseWindowToFront()

    def processingNextButtonClicked(self):
        player = self.processingPlayer
        if player is not None:
            if hasMultiMedia:
                if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                    player.pause()
            else:
                if player.state() == QtGui.QMovie.MovieState.Running:
                    player.setPaused(True)

        self.initializeResultPage()
        self.changeToNextPage()

    # Result
    def initializeResultPage(self):
        print("\n---Switching To Result Page---")

        self.pageInitializing = True

        thread = self.processDataThread
        resultDir = IO.dirs["Result Dir"]

        self.resultDatas = {}
        # Populate Result Datas
        for dataName in thread.dataNames:
            self.resultDatas[dataName] = {"Method TierList": ""}
            resultData = self.resultDatas[dataName]
            resultDataFolder = os.path.join(resultDir, dataName)

            for method in thread.methodList:
                resultData[method] = {"Info Path": "", "Diagram Paths": {}, "Costs": {}}

            for fileName in os.listdir(resultDataFolder):
                filePath = os.path.join(resultDataFolder, fileName)
                fileBase, fileExt = os.path.splitext(fileName)

                if fileExt == ".txt":
                    method = fileBase

                    if method not in Optimizer.methodFullList:
                        raise Warning("提取到的方法名不在Optimizer的方法列表里")

                    if method not in thread.methodList:
                        continue

                    resultData[method]["Info Path"] = filePath
                elif fileExt == ".png":
                    if fileBase == "DRT":
                        for method in thread.methodList:
                            resultData[method]["Diagram Paths"]["DRT"] = filePath
                    else:
                        diagramType, method = fileBase.split("@")

                        if method not in thread.methodList:
                            continue
                        if diagramType not in DrawDiagram.diagramTypes:
                            raise Warning("提取到的图片类型不在DrawDiagram的图片类型里")

                        resultData[method]["Diagram Paths"][diagramType] = filePath

            self.populateResultCosts(resultData)

        # Setup Standard ComboBox
        self.ResultStandardComboBox.clear()
        self.ResultStandardComboBox.addItems(IO.resultStandards)
        self.ResultStandardComboBox.setCurrentText(IO.resultDefaultStandard)

        # Setup Result Diagram
        self.resultStandardIndex = 0
        self.populateResultMethodTierLists()

        self.resultDataIndex = 0
        self.resultMethodTierListIndex = 0
        self.resultDiagramTypeIndex = 0
        self.updateResultPage()

        self.pageInitializing = False

    def updateResultPage(self):
        self.pageUpdating = True

        thread = self.processDataThread
        dataName = thread.dataNames[self.resultDataIndex]
        resultData = self.resultDatas[dataName]
        method = resultData["Method TierList"][self.resultMethodTierListIndex]
        diagramType = DrawDiagram.diagramTypes[self.resultDiagramTypeIndex]

        # Setup Some Text Labels
        self.ResultTitle.setText(f"{dataName}拟合结果：")
        self.ResultDiagramMethodLabel.setText(
            f"排名{self.resultMethodTierListIndex+1}: {method}"
        )
        self.ResultDiagramTitle.setText(diagramType)

        # Setup Result Info
        infoPath = resultData[method]["Info Path"]
        try:
            with open(infoPath, "r", encoding="utf-8") as file:
                infoText = file.read()
            self.ResultTextBrowser.setText(infoText)
        except Exception as e:
            print(f"Error reading file: {e}")

        # Setup Result Diagram
        diagramPath = resultData[method]["Diagram Paths"][diagramType]
        diagramImage = QtGui.QPixmap(diagramPath)
        self.ResultDiagram.setPixmap(diagramImage)

        # Button Logics
        self.ResultDiagramUpButton.setEnabled(self.resultDiagramTypeIndex > 0)
        self.ResultDiagramDownButton.setEnabled(
            self.resultDiagramTypeIndex < len(resultData[method]["Diagram Paths"]) - 1
        )
        self.ResultDiagramLeftButton.setEnabled(self.resultMethodTierListIndex > 0)
        self.ResultDiagramRightButton.setEnabled(
            self.resultMethodTierListIndex < len(thread.methodList) - 1
        )
        self.ResultPreviousDataButton.setEnabled(self.resultDataIndex > 0)
        self.ResultNextDataButton.setEnabled(
            self.resultDataIndex < len(thread.datas) - 1
        )

        self.pageUpdating = False

    def populateResultCosts(self, resultData: dict):
        methodList = self.processDataThread.methodList

        for method in methodList:
            infoPath = resultData[method]["Info Path"]
            costs = resultData[method]["Costs"]

            try:
                with open(infoPath, "r", encoding="utf-8") as file:
                    for line in file:
                        if line.startswith("Optimized Costs: "):
                            line = line.strip("Optimized Costs: ")
                            pairs = line.split(",")

                            for pair in pairs:
                                metric, value = pair.split(":")
                                metric = metric.strip()
                                value = float(value.strip())

                                costs[metric] = value

            except Exception as e:
                print(f"Error reading file: {e}")

    def populateResultMethodTierLists(self):
        thread = self.processDataThread
        methodList = thread.methodList
        index = self.resultStandardIndex

        standard = IO.resultStandards[index]
        reverse = IO.resultStandardsReverse[index]

        for dataName in thread.dataNames:
            cost = {}
            resultData = self.resultDatas[dataName]

            for method in methodList:
                cost[method] = resultData[method]["Costs"][standard]

            resultData["Method TierList"] = [
                key
                for key, _ in sorted(
                    cost.items(), key=lambda item: item[1], reverse=reverse
                )
            ]

    def resultStandardComboboxChanged(self, index: int):
        if not self.pageInitializing:
            self.resultStandardIndex = index
            self.populateResultMethodTierLists()
            self.updateResultPage()

    def resultDiagramUpButtonClicked(self):
        thread = self.processDataThread
        dataName = thread.dataNames[self.resultDataIndex]
        resultData = self.resultDatas[dataName]
        method = resultData["Method TierList"][self.resultMethodTierListIndex]

        if self.resultDiagramTypeIndex > 0:
            while True:
                self.resultDiagramTypeIndex -= 1
                if (
                    DrawDiagram.diagramTypes[self.resultDiagramTypeIndex]
                    in resultData[method]["Diagram Paths"]
                ):
                    break
            self.updateResultPage()

    def resultDiagramDownButtonClicked(self):
        thread = self.processDataThread
        dataName = thread.dataNames[self.resultDataIndex]
        resultData = self.resultDatas[dataName]
        method = resultData["Method TierList"][self.resultMethodTierListIndex]

        if self.resultDiagramTypeIndex < len(resultData[method]["Diagram Paths"]) - 1:
            while True:
                self.resultDiagramTypeIndex += 1
                if (
                    DrawDiagram.diagramTypes[self.resultDiagramTypeIndex]
                    in resultData[method]["Diagram Paths"]
                ):
                    break
            self.updateResultPage()

    def resultDiagramLeftButtonClicked(self):
        if self.resultMethodTierListIndex > 0:
            self.resultMethodTierListIndex -= 1
            self.updateResultPage()

    def resultDiagramRightButtonClicked(self):
        thread = self.processDataThread

        if self.resultMethodTierListIndex < len(thread.methodList) - 1:
            self.resultMethodTierListIndex += 1
            self.updateResultPage()

    def resultPreviousDataButtonClicked(self):
        if self.resultDataIndex > 0:
            self.resultDataIndex -= 1
            self.updateResultPage()

    def resultNextDataButtonClicked(self):
        thread = self.processDataThread

        if self.resultDataIndex < len(thread.datas) - 1:
            self.resultDataIndex += 1
            self.updateResultPage()
