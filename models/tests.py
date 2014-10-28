# -*- coding: utf-8 -*-
import unittest

import mock

from models.document import Document
from models.match_singlet import MatchSinglet


class DocumentTest(unittest.TestCase):
    file_name = 'this_is_a_file.txt'
    meta = {'title': u'test 稢綌',
            'author': u'gorden 胇赲'
            }
    body = u'In id tristique orci. 痵痽 犵艿邔 疿疶砳 齸圞趲.'

    def setUp(self):
        self.doc = Document(file_name=self.file_name,
                            body=self.body,
                            metadata=self.meta)

    def test_clone(self):
        """
        Test cloning a document
        """
        doc_cloned = self.doc.clone()
        self.assertEqual(doc_cloned.file_name, self.doc.file_name)
        self.assertEqual(doc_cloned.metadata, self.doc.metadata)
        self.assertEqual(doc_cloned.body, self.doc.body)
        self.assertEqual(self.doc, doc_cloned)

        doc_cloned.file_name = 'nope'
        self.assertNotEqual(self.doc, doc_cloned)

        doc_cloned.file_name = self.doc.file_name
        doc_cloned.metadata = None
        self.assertNotEqual(self.doc, doc_cloned)

        doc_cloned.metadata = self.doc.metadata
        doc_cloned.body = ''
        self.assertNotEqual(self.doc, doc_cloned)

    def test_to_dict(self):
        doc_dict = self.doc.to_dict()
        self.assertEqual(doc_dict['file_name'], self.doc.file_name)
        self.assertEqual(doc_dict['metadata'], self.doc.metadata)
        self.assertEqual(doc_dict['body'], self.doc.body)


class MatchSingletTest(unittest.TestCase):

    def setUp(self):
        self.file_name = 'name 璸瓁'
        self.doc = mock.Mock
        self.context_pad = ' context垥娀 '
        self.match = 'this is 檦 the match'
        self.with_context = '{pad}{match}{pad}'.format(pad=self.context_pad,
                                                       match=self.match)
        fmt = 'asdfalakjvlzx{}鬐鶤鶐膗,觾韄煔垥'
        self.doc.body = fmt.format(self.with_context)

    def test_get_context(self):
        """
        Test that get_context returns the match and appropriate context
        """
        singlet = MatchSinglet(file_name=self.file_name,
                               passage=self.match,
                               document=self.doc)
        pad_chars = len(self.context_pad)
        match_with_context = singlet.get_context(context_chars=pad_chars)
        self.assertEqual(match_with_context, self.with_context)
