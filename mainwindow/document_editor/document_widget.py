# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Documents/LearnPythonTheHardWay/projects/QT_Dirt/Dirt_Document_Comparison.ui'
#
# Created: Wed Jan 21 12:30:39 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import document_util
import utilities.file_ops as file_ops

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DocumentPanel(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

    def setupUi(self, documentPanel):
        documentPanel.setObjectName(_fromUtf8("DocumentPanel"))
        documentPanel.resize(588, 419)
        self.verticalLayout = QtGui.QVBoxLayout(documentPanel)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.document_holder = QtGui.QHBoxLayout()
        self.document_holder.setObjectName(_fromUtf8("document_holder"))
        self.doc_focus = QtGui.QTextEdit(documentPanel)
        self.doc_focus.setObjectName(_fromUtf8("doc_focus"))
        self.document_holder.addWidget(self.doc_focus)
        self.doc_comparison = QtGui.QTextEdit(documentPanel)
        self.doc_comparison.setObjectName(_fromUtf8("doc_comparison"))
        self.document_holder.addWidget(self.doc_comparison)
        self.verticalLayout.addLayout(self.document_holder)
        self.navigation_bar = QtGui.QHBoxLayout()
        self.navigation_bar.setObjectName(_fromUtf8("navigation_bar"))
        self.lineEdit = QtGui.QLineEdit(documentPanel)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.navigation_bar.addWidget(self.lineEdit)
        self.previous_button = QtGui.QPushButton(documentPanel)
        self.previous_button.setObjectName(_fromUtf8("previous_button"))
        self.navigation_bar.addWidget(self.previous_button)
        self.next_button = QtGui.QPushButton(documentPanel)
        self.next_button.setMinimumSize(QtCore.QSize(93, 32))
        self.next_button.setObjectName(_fromUtf8("next_button"))
        self.navigation_bar.addWidget(self.next_button)
        self.verticalLayout.addLayout(self.navigation_bar)

        self.retranslateUi(documentPanel)
        QtCore.QMetaObject.connectSlotsByName(documentPanel)
        documentPanel.setTabOrder(self.doc_focus, self.doc_comparison)

        #test
        focus = "../dirt_preprocessed/pre/lorem.txt"
        comp = "../dirt_preprocessed/pre/lorem2.txt"
        match = "../dirt_output/lorem__lorem2__CMP.json"
        self.set_focus_doc(focus, match)
        self.set_comp_doc(comp, match)
        self.number_of_matches = 0
        self.match_idx = 0
        self.json_data = ""
        self.alpha_list = []
        self.beta_list = []
        self.setup_matches(match)

    def retranslateUi(self, documentPanel):
        documentPanel.setWindowTitle(_translate("DocumentPanel", "Form", None))
        self.previous_button.setText(_translate("DocumentPanel", "Previous", None))
        self.next_button.setText(_translate("DocumentPanel", "Next", None))
        self.next_button.clicked.connect(self.next_match)
        self.previous_button.clicked.connect(self.prev_match)

    def set_focus_doc(self, doc, match_doc):
        """
        Displays the focus document with highlighted matches in focus
        document text area
        :param doc:
        :param match_doc:
        :return:
        """
        document_util.focus_doc(self.doc_focus, doc, match_doc)

    def set_comp_doc(self, comp_doc, match_doc):
        """
        Displays the comparison document with highlighted matches in
        comparison document text area
        :param comp_doc:
        :param match_doc:
        :return:
        """
        document_util.comp_doc(self.doc_comparison, comp_doc, match_doc)

    def setup_matches(self, match_file):
        with open(match_file) as json_file:
            self.json_data = file_ops.read_json_utf8(json_file.name)
            self.number_of_matches = len(self.json_data['matches'])
            for i in range (0, self.number_of_matches):
                self.alpha_list.append(self.json_data['matches'][i][
                    'alpha_indices'][0])
                self.beta_list.append(self.json_data['matches'][i][
                    'beta_indices'][0])
            print self.alpha_list
            print self.beta_list


    def next_match(self):
        """
        Moves cursor and scrolls view of focus and comparison text area to
        next match
        :return:
        """
        match_idx = self.match_idx

        focus_cursor = self.doc_focus.textCursor()
        # focus_cursor.position = self.alpha_list[match_idx]
        focus_cursor.setPosition(self.alpha_list[match_idx],
                                 QtGui.QTextCursor.KeepAnchor)
        self.move_cursor(self.doc_focus, focus_cursor.position())

        comp_cursor = self.doc_comparison.textCursor()
        comp_cursor.setPosition(self.beta_list[match_idx],
                                 QtGui.QTextCursor.KeepAnchor)
        self.move_cursor(self.doc_comparison, comp_cursor.position())

        self.match_idx = (self.match_idx + 1) % self.number_of_matches

    def prev_match(self):
        """
        Moves cursor and scrolls view of focus and comparison text area to
        previous match
        :return:
        """
        match_idx = self.match_idx

        focus_cursor = self.doc_focus.textCursor()
        # focus_cursor.position = self.alpha_list[match_idx]
        focus_cursor.setPosition(self.alpha_list[match_idx],
                                 QtGui.QTextCursor.KeepAnchor)
        self.move_cursor(self.doc_focus, focus_cursor.position())

        comp_cursor = self.doc_comparison.textCursor()
        comp_cursor.setPosition(self.beta_list[match_idx],
                                 QtGui.QTextCursor.KeepAnchor)
        self.move_cursor(self.doc_comparison, comp_cursor.position())

        self.match_idx = (self.match_idx - 1) % self.number_of_matches

    def move_cursor(self, doc, pos):
        """
        Moves cursor
        :param doc:
        :param pos:
        :return:
        """
        text_cursor = doc.textCursor()
        text_cursor.setPosition(pos, QtGui.QTextCursor.MoveAnchor)
        doc.setTextCursor(text_cursor)
        doc.ensureCursorVisible()