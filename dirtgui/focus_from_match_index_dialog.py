from PyQt4.QtGui import *
from PyQt4.QtCore import *


class FocusIndexSelectDialog(QDialog):
    def __init__(self, match_index, parent=None):
        super(FocusIndexSelectDialog, self).__init__(parent)
        self.match_index = match_index
        layout = QVBoxLayout(self)

        # nice widget for editing the date
        self.selector = QListWidget(self)
        focus_candidates = list(match_index.get_all_file_names())
        self.selector.addItems(focus_candidates)
        layout.addWidget(self.selector)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_focus_name(self):
        items = self.selector.selectedItems()
        q_text = items[0].text()
        return str(q_text)

    @staticmethod
    def get_focus(match_index, parent=None):
        dialog = FocusIndexSelectDialog(match_index, parent)
        result = dialog.exec_()
        focus = dialog.get_focus_name()
        return focus, result == QDialog.Accepted
