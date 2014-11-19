#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

import wx
from wx import LC_REPORT
from wx import LC_HRULES
from wx import ClientDC
from wx.html import HtmlWindow
from wx.html import HW_SCROLLBAR_AUTO
from wx.lib.wordwrap import wordwrap


REPORT_FORMATS = ['.xml', '.json', '.txt']


class ReportPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        self.directory_path = "."
        self.index = 0
        self.input_list = wx.ListCtrl(self, size=(0, 0),
                                      style=LC_REPORT | LC_HRULES)
        self.input_list.InsertColumn(0, 'List of Inputs', width=0)
        self.input_list.SetMinSize(minSize=(100, 100))
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_col_click,
                  self.input_list)

        self.focus_doc = HtmlWindow(self, style=HW_SCROLLBAR_AUTO)
        self.comparison_doc = HtmlWindow(self, style=HW_SCROLLBAR_AUTO)

        document_sizer = wx.BoxSizer(wx.HORIZONTAL)
        document_sizer.Add(self.input_list, 1, wx.EXPAND, 1)
        document_sizer.Add(self.focus_doc, 2, wx.EXPAND | wx.ALL, 1)
        document_sizer.Add(self.comparison_doc, 2, wx.EXPAND | wx.ALL, 1)

        self.SetSizer(document_sizer)
        self.Layout()
        self.Fit()

    def _populate_input_list(self, dir):
        print "Current dir:" + dir
        files = [os.path.join(dir, f) for f in os.listdir(dir)]
        for f in files:
            print "Looking at " + f
            if os.path.isfile(f):
                print f + " is file!"
                if os.path.splitext(f)[1] in REPORT_FORMATS:
                    print(f)
                    self.input_list.InsertStringItem(self.index, f)
                    self.index += 1
        self.input_list.SetColumnWidth(0, width=wx.LIST_AUTOSIZE)
        self.input_list.PostSizeEventToParent()

    def _on_col_click(self, event):
        selected_item = event.m_itemIndex
        document_path = self.input_list.GetItem(itemId=selected_item,
                                                col=0).GetText()
        with codecs.open(document_path, 'r', encoding='utf8') as selected_doc:
            self.focus_doc.SetPage(
                wordwrap(selected_doc.read(), 50, ClientDC(self)))
        event.Skip()

    def set_directory_path(self, directory_path):
        self.directory_path = directory_path
        self._populate_input_list(self.directory_path)

    def set_focus_doc(self, file_path):
        with codecs.open(file_path, 'r', encoding='utf8') as focus:
            self.focus_doc.SetPage(wordwrap(focus.read(), 50, ClientDC(self)))

    def set_comparison_doc(self, file_path):
        with codecs.open(file_path, 'r', encoding='utf8') as comparison:
            self.comparison_doc.SetPage(
                wordwrap(comparison.read(), 50, ClientDC(self)))

    def add_input(self, file_path):
        if os.path.isfile(file_path):
            self.input_list.InsertStringItem(self.index, file_path)
            self.index += 1
        else:
            print file_path + " is not a file"
        self.input_list.SetColumnWidth(0, width=wx.LIST_AUTOSIZE)
        self.input_list.PostSizeEventToParent()