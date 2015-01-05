# -*- coding: utf-8 -*-

# ##########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext
import wx.grid

###########################################################################
## Class MyFrame1
###########################################################################


class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"DIRT: Dynamic Identification of Reused Text",
                          pos=wx.DefaultPosition, size=wx.Size(-1, -1),
                          style=wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.Size(-1, -1), wx.DefaultSize)
        self.SetFont(wx.Font(14, 71, 90, 90, False, wx.EmptyString))

        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.Open = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.AppendItem(self.Open)

        self.Save = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.AppendItem(self.Save)

        self.Exit = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.AppendItem(self.Exit)

        self.m_menubar1.Append(self.m_menu1, u"Menu")

        self.m_menu2 = wx.Menu()
        self.Preference = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Preferences", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.AppendItem(self.Preference)

        self.m_menubar1.Append(self.m_menu2, u"Options")

        self.SetMenuBar(self.m_menubar1)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        bSizer103 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText10 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText10.Wrap(-1)
        self.m_staticText10.SetFont(wx.Font(11, 70, 90, 92, False, wx.EmptyString))

        bSizer103.Add(self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticline71 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.LI_VERTICAL)
        bSizer103.Add(self.m_staticline71, 0, wx.EXPAND | wx.ALL, 5)

        self.m_radioBtn9 = wx.RadioButton(self.m_panel1, wx.ID_ANY, u"Traditional Chinese", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        bSizer103.Add(self.m_radioBtn9, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_radioBtn10 = wx.RadioButton(self.m_panel1, wx.ID_ANY, u"Simplified Chinese", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        bSizer103.Add(self.m_radioBtn10, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticline41 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.LI_VERTICAL)
        bSizer103.Add(self.m_staticline41, 0, wx.ALL | wx.EXPAND, 5)

        self.m_checkBox1 = wx.CheckBox(self.m_panel1, wx.ID_ANY, u"Punctuation", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_checkBox1.SetValue(True)
        bSizer103.Add(self.m_checkBox1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_checkBox2 = wx.CheckBox(self.m_panel1, wx.ID_ANY, u"Spacing", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer103.Add(self.m_checkBox2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticline5 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        bSizer103.Add(self.m_staticline5, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Match Length :", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        bSizer103.Add(self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        m_comboBox3Choices = []
        self.m_comboBox3 = wx.ComboBox(self.m_panel1, wx.ID_ANY, u"Fixed Lengths", wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox3Choices, 0)
        bSizer103.Add(self.m_comboBox3, 0, wx.ALL, 5)

        bSizer6.Add(bSizer103, 0, wx.EXPAND, 5)

        self.m_staticline6 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LI_HORIZONTAL)
        bSizer6.Add(self.m_staticline6, 0, wx.EXPAND | wx.ALL, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        Focus = wx.BoxSizer(wx.VERTICAL)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        fgSizer9 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer9.SetFlexibleDirection(wx.BOTH)
        fgSizer9.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText17 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Document :", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText17.Wrap(-1)
        self.m_staticText17.SetFont(wx.Font(11, 70, 90, 92, False, wx.EmptyString))

        fgSizer9.Add(self.m_staticText17, 1, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl16 = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_textCtrl16.SetMinSize(wx.Size(220, -1))

        fgSizer9.Add(self.m_textCtrl16, 0, wx.ALL, 5)

        self.m_staticText18 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Author :", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText18.Wrap(-1)
        self.m_staticText18.SetFont(wx.Font(11, 70, 90, 92, False, wx.EmptyString))

        fgSizer9.Add(self.m_staticText18, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl17 = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_textCtrl17.SetMinSize(wx.Size(220, -1))

        fgSizer9.Add(self.m_textCtrl17, 0, wx.ALL, 5)

        bSizer10.Add(fgSizer9, 1, 0, 5)

        self.m_button1 = wx.Button(self.m_panel1, wx.ID_ANY, u"&Search", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        Focus.Add(bSizer10, 0, wx.EXPAND, 5)

        self.Focus_text = wx.richtext.RichTextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                   wx.DefaultSize,
                                                   0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        Focus.Add(self.Focus_text, 1, wx.EXPAND | wx.ALL, 5)

        bSizer9.Add(Focus, 1, wx.EXPAND | wx.RIGHT, 5)

        self.m_staticline7 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        bSizer9.Add(self.m_staticline7, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        Matches = wx.BoxSizer(wx.VERTICAL)

        bSizer101 = wx.BoxSizer(wx.HORIZONTAL)

        fgSizer91 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer91.SetFlexibleDirection(wx.BOTH)
        fgSizer91.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText171 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Match #1 :", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.m_staticText171.Wrap(-1)
        self.m_staticText171.SetFont(wx.Font(11, 70, 90, 92, False, wx.EmptyString))

        fgSizer91.Add(self.m_staticText171, 1, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl161 = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         0)
        self.m_textCtrl161.SetMinSize(wx.Size(220, -1))

        fgSizer91.Add(self.m_textCtrl161, 0, wx.ALL, 5)

        self.m_staticText181 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Author :", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        self.m_staticText181.Wrap(-1)
        self.m_staticText181.SetFont(wx.Font(11, 70, 90, 92, False, wx.EmptyString))

        fgSizer91.Add(self.m_staticText181, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl171 = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         0)
        self.m_textCtrl171.SetMinSize(wx.Size(220, -1))

        fgSizer91.Add(self.m_textCtrl171, 0, wx.ALL, 5)

        bSizer101.Add(fgSizer91, 1, 0, 5)

        self.m_button2 = wx.Button(self.m_panel1, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer101.Add(self.m_button2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        Matches.Add(bSizer101, 0, wx.EXPAND, 5)

        self.m_richText5 = wx.richtext.RichTextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                    wx.Size(-1, 200),
                                                    0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        Matches.Add(self.m_richText5, 1, wx.EXPAND | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LI_HORIZONTAL)
        Matches.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        bSizer102 = wx.BoxSizer(wx.HORIZONTAL)

        fgSizer92 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer92.SetFlexibleDirection(wx.BOTH)
        fgSizer92.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText172 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Match #2 :", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.m_staticText172.Wrap(-1)
        self.m_staticText172.SetFont(wx.Font(11, 70, 90, 92, False, wx.EmptyString))

        fgSizer92.Add(self.m_staticText172, 1, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl162 = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         0)
        self.m_textCtrl162.SetMinSize(wx.Size(220, -1))

        fgSizer92.Add(self.m_textCtrl162, 0, wx.ALL, 5)

        self.m_staticText182 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Author :", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        self.m_staticText182.Wrap(-1)
        self.m_staticText182.SetFont(wx.Font(11, 70, 90, 92, False, wx.EmptyString))

        fgSizer92.Add(self.m_staticText182, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl172 = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         0)
        self.m_textCtrl172.SetMinSize(wx.Size(220, -1))

        fgSizer92.Add(self.m_textCtrl172, 0, wx.ALL, 5)

        bSizer102.Add(fgSizer92, 1, 0, 5)

        self.m_button3 = wx.Button(self.m_panel1, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer102.Add(self.m_button3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        Matches.Add(bSizer102, 0, wx.EXPAND, 5)

        self.m_richText6 = wx.richtext.RichTextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                    wx.Size(-1, 200),
                                                    0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        Matches.Add(self.m_richText6, 1, wx.EXPAND | wx.ALL, 5)

        bSizer9.Add(Matches, 1, wx.EXPAND | wx.LEFT, 5)

        bSizer6.Add(bSizer9, 1, wx.EXPAND, 5)

        self.m_staticline4 = wx.StaticLine(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LI_HORIZONTAL)
        bSizer6.Add(self.m_staticline4, 0, wx.EXPAND | wx.ALL, 5)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText7 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Results", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        self.m_staticText7.SetFont(wx.Font(12, 70, 90, 92, False, wx.EmptyString))

        bSizer8.Add(self.m_staticText7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_grid2 = wx.grid.Grid(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid2.CreateGrid(5, 5)
        self.m_grid2.EnableEditing(True)
        self.m_grid2.EnableGridLines(True)
        self.m_grid2.EnableDragGridSize(False)
        self.m_grid2.SetMargins(0, 0)

        # Columns
        self.m_grid2.SetColSize(0, 380)
        self.m_grid2.SetColSize(1, 155)
        self.m_grid2.SetColSize(2, 80)
        self.m_grid2.SetColSize(3, 80)
        self.m_grid2.SetColSize(4, 80)
        self.m_grid2.EnableDragColMove(False)
        self.m_grid2.EnableDragColSize(True)
        self.m_grid2.SetColLabelSize(30)
        self.m_grid2.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid2.EnableDragRowSize(True)
        self.m_grid2.SetRowLabelSize(80)
        self.m_grid2.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid2.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer8.Add(self.m_grid2, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer6.Add(bSizer8, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_panel1.SetSizer(bSizer6)
        self.m_panel1.Layout()
        bSizer6.Fit(self.m_panel1)
        bSizer3.Add(self.m_panel1, 1, wx.TOP | wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.SetSizer(bSizer3)
        self.Layout()
        bSizer3.Fit(self)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
#refer manual for details
app = wx.App(False)

#create an object of CalcFrame
frame = MyFrame1(None)
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()
