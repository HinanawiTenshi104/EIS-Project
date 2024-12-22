from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CustomDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Custom Dialog")

        # Layouts
        main_layout = QVBoxLayout()

        # Display Name LineEdit
        self.display_name_label = QLabel("Display Name:", self)
        main_layout.addWidget(self.display_name_label)

        self.display_name_edit = QLineEdit(
            self.main_window.displayName[0] if self.main_window.displayName else "",
            self,
        )
        self.display_name_edit.textChanged.connect(self.on_display_name_changed)
        main_layout.addWidget(self.display_name_edit)

        # Section Name LineEdit
        self.section_name_label = QLabel("Section Name:", self)
        main_layout.addWidget(self.section_name_label)

        self.section_name_edit = QLineEdit(
            self.main_window.sectionName[0] if self.main_window.sectionName else "",
            self,
        )
        main_layout.addWidget(self.section_name_edit)

        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def on_display_name_changed(self, text):
        # Automatically set section name to display name when display name changes
        self.section_name_edit.setText(text)

    def accept(self):
        # Update main window's arrays when OK is clicked
        if self.main_window.displayName:
            self.main_window.displayName[0] = self.display_name_edit.text()
        else:
            # Assuming you want to create a new entry if the list is empty
            self.main_window.displayName = [self.display_name_edit.text()]
            self.main_window.sectionName = [
                self.section_name_edit.text()
            ]  # Or use the display name if that's the default
        # Alternatively, if you always want to update both arrays regardless of their initial state:
        # self.main_window.displayName = [self.display_name_edit.text()]
        # self.main_window.sectionName = [self.section_name_edit.text()]

        # Call the custom method to validate section name change if needed
        # self.main_window.validate_section_name_change(self.section_name_edit.text())

        super().accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.displayName = ["Initial Display Name"]  # Example initial data
        self.sectionName = ["Initial Section Name"]  # Example initial data

        self.initUI()

    def initUI(self):
        # Create a button to open the dialog
        self.open_dialog_button = QPushButton("Open Dialog", self)
        self.open_dialog_button.clicked.connect(self.open_dialog)

        # Set the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.open_dialog_button)

    def open_dialog(self):
        dialog = CustomDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Dialog was accepted, update UI or perform other actions if needed
            print("Display Name:", self.displayName[0])
            print("Section Name:", self.sectionName[0])
            # Optionally, update other parts of the main window's UI here

    # Placeholder for custom section name validation logic
    # def validate_section_name_change(self, new_section_name):
    #     # Implement your validation logic here
    #     pass


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
