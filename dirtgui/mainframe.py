#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import os
import sys
import codecs

import wx


# noinspection PyUnresolvedReferences

import reportpanels.html_panel as html_panel
import reportpanels.filemenu_panel as filemenu_panel

root = ""


class MainFrame(wx.Frame):
    def __init__(self, parent, dir):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                          pos=wx.DefaultPosition,
                          size=wx.Size(500, 300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.lines = []

        # sets file menu
        self.file_menu = filemenu_panel.FileMenuPanel(parent=self)

        # main panel which holds reports and results
        self.main_panel = wx.Panel(self)

        # layout for main panel
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(main_sizer)

        # report panel
        self.m_panel2 = html_panel.ReportPanel(self.main_panel)
        main_sizer.Add(self.m_panel2, 1, flag=wx.EXPAND)

        if os.path.isfile(dir):
            self._parse_text(dir)

        # result panel
        # self.m_panel3 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
        # wx.DefaultSize, wx.TAB_TRAVERSAL)
        # main_sizer.Add(self.m_panel3, 1, wx.EXPAND, 5)

        # button to close frame - temporary
        button = wx.Button(self.main_panel, wx.ID_OK, "Okay")
        button.Bind(wx.EVT_BUTTON, self._close)
        main_sizer.Add(button, 0, flag=wx.BOTTOM | wx.EXPAND)

        self.Bind(wx.EVT_SIZE, self._window_size)
        self.Layout()
        self.Show()

        self.Centre(wx.BOTH)

    def _close(self, event):
        """
        Closes gui application - temporary implementation
        :param event:
        """
        self.Close()

    def _window_size(self, event):
        self.main_panel.SetSize(size=self.GetClientSizeTuple())
        self.m_panel2.SetSize(size=self.main_panel.GetClientSizeTuple())
        self.Layout()

    def _parse_text(self, input_list):
        with codecs.open(input_list, 'r', encoding='utf8') as fin:
            for line in fin:
                file_path = os.path.join(root, line.strip())
                self.lines.append(file_path)
                self.m_panel2.add_input(file_path)
        if os.path.isfile(self.lines[0]):
            self.m_panel2.set_focus_doc(self.lines[0])
        if self.m_panel2.index >= 2:
            if os.path.isfile(self.lines[1]):
                self.m_panel2.set_comparison_doc(self.lines[1])

    def __del__(self):
        pass


class App(wx.App):
    def __init__(self,input_list):
        wx.App.__init__(self)
        self.top_frame = MainFrame(parent=None, dir=input_list)
        self.top_frame.Show()
        self.SetTopWindow(self.top_frame)

    def OnInit(self):

        return True

    def OnExit(self):
        print "OnExit"


# Required to run wxpython
def main():
    app = App(sys.argv[1])
    app.MainLoop()


if __name__ == '__main__':
    main()

