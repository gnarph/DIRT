#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

class DocumentPanel():
    """
    DocumentPanel
    Holds and displays two documents in comparison
    """
    def __init__(self, parent):
        """
        Initializes text document widgets
        :param parent:
        :return:
        """
        pass

    def _set_focus_doc(self, file_path):
        """
        Set the focus document given a file path
        :param dir:
        :return:
        """
        with codecs.open(file_path, 'r', encoding='utf8') as focus:
            pass
        pass

    def _set_comp_doc(self,file_path):
        """
        Set the comparison document given a file path
        :param self:
        :param dir:
        :return:
        """
        with codecs.open(file_path, 'r', encoding='utf8') as comparison:
            pass
        pass

