from PyQt6.QtCore import QMimeData, Qt, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class DragTargetIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            "QLabel { background-color: #ccc; border: 1px solid black; }"
        )


class DragItem(QLabel):
    vaildDrop = None
    deleteMe = pyqtSignal(QLabel)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        # Store data separately from display label, but use label for default.
        self.data = self.text()

    def setData(self, data):
        self.data = data

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            self.vaildDrop = False
            drag.exec(Qt.DropAction.MoveAction)
            # self.show()  # Show this widget again, if it's dropped outside.
            if not self.vaildDrop:
                self.deleteMe.emit(self)


class DragWidget(QWidget):
    """
    Generic list sorting handler.
    """

    orderChanged = pyqtSignal()
    itemDeleted = pyqtSignal()

    def __init__(self, *args, orientation=Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        # Store the orientation for drag checks later.
        self.orientation = orientation

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()

        self.blayout.setSpacing(0)

        # Add the drag target indicator. This is invisible by default,
        # we show it and move it around while the drag is active.
        self._dragTargetIndicator = DragTargetIndicator()
        self.blayout.addWidget(self._dragTargetIndicator)
        self._dragTargetIndicator.hide()

        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dragLeaveEvent(self, e):
        self._dragTargetIndicator.hide()
        e.accept()

    def dragMoveEvent(self, e):
        # Find the correct location of the drop target, so we can move it there.
        index = self._findDropLocation(e)
        if index is not None:
            # Inserting moves the item if its alreaady in the layout.
            self.blayout.insertWidget(index, self._dragTargetIndicator)
            # Hide the item being dragged.
            e.source().hide()
            # Show the target.
            self._dragTargetIndicator.show()

        e.accept()

    def dropEvent(self, e):
        widget = e.source()
        # Use drop target location for destination, then remove it.
        self._dragTargetIndicator.hide()
        index = self.blayout.indexOf(self._dragTargetIndicator)
        if index is not None:
            self.blayout.insertWidget(index, widget)
            self.orderChanged.emit()
            widget.vaildDrop = True
            widget.show()
            self.blayout.activate()
        e.accept()

    def _findDropLocation(self, e):
        pos = e.position()
        spacing = self.blayout.spacing() / 2

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()

            if self.orientation == Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = (
                    pos.y() >= w.y() - spacing
                    and pos.y() <= w.y() + w.size().height() + spacing
                )
            else:
                # Drag drop horizontally.
                drop_here = (
                    pos.x() >= w.x() - spacing
                    and pos.x() <= w.x() + w.size().width() + spacing
                )

            if drop_here:
                # Drop over this target.
                break

        return n

    def addItem(self, item):
        self.blayout.addWidget(item)
        item.deleteMe.connect(self.deleteItem)

    def deleteItem(self, w):
        self.blayout.removeWidget(w)
        self.itemDeleted.emit()

    def getItemCount(self):
        return self.blayout.count() - 1

    def clearAllItem(self):
        layout = self.blayout

        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if isinstance(widget, DragTargetIndicator):
                widget.hide()
                continue
            if widget is not None:
                widget.deleteLater()
            layout.removeItem(item)

    def getItemData(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if w != self._dragTargetIndicator:
                # The target indicator has no data.
                data.append(w.data)
        return data
