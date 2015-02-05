"""
Thanks to
https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
"""

from PyQt4.QtGui import QDialog, QVBoxLayout, QDialogButtonBox, QListWidget
from PyQt4.QtCore import Qt


class SelectFromListDialog(QDialog):
    def __init__(self, options, parent=None):
        super(SelectFromListDialog, self).__init__(parent)
        layout = QVBoxLayout(self)

        # nice widget for editing the date
        self.selector = QListWidget(self)
        self.selector.addItems(list(options))
        layout.addWidget(self.selector)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def selected(self):
        items = self.selector.selectedItems()
        q_text = items[0].text()
        return str(q_text)

    @staticmethod
    def get_selected(options, parent=None):
        dialog = SelectFromListDialog(options, parent)
        result = dialog.exec_()
        focus = dialog.selected()
        return focus, result == QDialog.Accepted
