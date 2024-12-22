import sys

from PyQt6 import QtWidgets

from UI.UIMain import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    mainWindow.raiseWindowToFront()

    sys.exit(app.exec())
