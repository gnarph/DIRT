# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Documents/LearnPythonTheHardWay/projects/QT_Dirt/Dirt_Document_Comparison.ui'
#
# Created: Wed Jan 21 12:30:39 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import document_util

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

        self.set_focus_doc()
        self.set_comp_doc()

    def retranslateUi(self, documentPanel):
        documentPanel.setWindowTitle(_translate("DocumentPanel", "Form", None))
        self.previous_button.setText(_translate("DocumentPanel", "Previous", None))
        self.next_button.setText(_translate("DocumentPanel", "Next", None))
        self.next_button.clicked.connect(self.next_match)
        self.previous_button.clicked.connect(self.prev_match)

    def set_focus_doc(self):
        document_util.focus_doc(self.doc_focus,
                                    "../dirt_preprocessed/pre/lorem.txt",
                                    "../dirt_output/lorem__lorem2__CMP.json")

    def set_comp_doc(self):
        document_util.comp_doc(self.doc_comparison,
                                    "../dirt_preprocessed/pre/lorem2.txt",
                                    "../dirtoutput/lorem__lorem2__CMP.json")

    def next_match(self):
        focus_cursor = self.doc_focus.textCursor()
        self.move_cursor(self.doc_focus, focus_cursor.position() + 50)
        comp_cursor = self.doc_comparison.textCursor()
        self.move_cursor(self.doc_comparison, comp_cursor.position() + 50)

    def prev_match(self):
        pass

    def move_cursor(self, doc, pos):
        text_cursor = doc.textCursor()
        text_cursor.setPosition(pos, QtGui.QTextCursor.MoveAnchor)
        print text_cursor.position()
        doc.setTextCursor(text_cursor)
        doc.ensureCursorVisible()