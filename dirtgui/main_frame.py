from PyQt4 import QtGui
from dirtgui.main_grid import MainGrid


class MainFrame(QtGui.QFrame):
    """
    Creates a frame from a grid layout
    Param: self, title of the frame
    """
    def __init__(self, parent, header):
        super(MainFrame, self).__init__(parent)

        if header == 'FOCUS':
            passage_type = 'alpha_passage'
        elif header == 'MATCH':
            passage_type = 'beta_passage'

        self.grid = MainGrid(self, header, passage_type)

        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setLayout(self.grid)