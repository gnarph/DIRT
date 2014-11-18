import wx


class FileMenuPanel(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.GetTopLevelParent().CreateStatusBar()  # A Statusbar in the bottom of the window

        self.createMenuBar()

    def createMenuBar(self):
        self.menuBar = wx.MenuBar()

        self.filemenu = wx.Menu()  # Setting up the menu.
        self.submenu = wx.Menu()
        self.filemenu.Append(100, "&Open File...", "Open a file")
        self.filemenu.AppendSubMenu(self.submenu, "&Options")
        self.filemenu.Append(101, "&About", "Information about this program")
        self.filemenu.AppendSeparator()
        self.filemenu.Append(102, "&Exit", "Terminate the program")

        # Creating the menubar
        self.menuBar.Append(menu=self.filemenu, title="&File",)
        self.GetTopLevelParent().SetMenuBar(self.menuBar)