# -*- coding: utf-8 -*-
import unittest

import mock

from models.document import Document
from models.match_singlet import MatchSinglet


class DocumentTest(unittest.TestCase):
    file_name = u'this_is_a_file.txt'
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

        doc_cloned.file_name = u'nope'
        self.assertNotEqual(self.doc, doc_cloned)

        doc_cloned.file_name = self.doc.file_name
        doc_cloned.metadata = None
        self.assertNotEqual(self.doc, doc_cloned)

        doc_cloned.metadata = self.doc.metadata
        doc_cloned.body = ''
        self.assertNotEqual(self.doc, doc_cloned)

    def test_to_dict(self):
        """
        Test conversion to dictionary (for json serialization)
        """
        doc_dict = self.doc.to_dict()
        self.assertEqual(doc_dict['file_name'], self.doc.file_name)
        self.assertEqual(doc_dict['metadata'], self.doc.metadata)
        self.assertEqual(doc_dict['body'], self.doc.body)


class MatchSingletTest(unittest.TestCase):

    def setUp(self):
        self.file_name = u'name 璸瓁'
        self.doc = mock.Mock
        self.context_pad = u' context垥娀 '
        self.match = u'this is 檦 the match'
        self.with_context = u'{pad}{match}{pad}'.format(pad=self.context_pad,
                                                        match=self.match)
        fmt = u'duck goose raccoon{}鬐鶤鶐膗,觾韄煔垥'
        self.doc.body = fmt.format(self.with_context)
        self.body = self.doc.body
        self.singlet = MatchSinglet(file_name=self.file_name,
                                    passage=self.match,
                                    document=self.doc)

    def test_get_context(self):
        """
        Test that get_context returns the match and appropriate context
        """
        pad_chars = len(self.context_pad)
        match_with_context = self.singlet.get_context(context_chars=pad_chars)
        self.assertEqual(match_with_context, self.with_context)

        # Test match at end of body
        loc = self.body.find(self.match)
        end_match = loc + len(self.match)
        self.doc.body = self.doc.body[:end_match]
        end_singlet = MatchSinglet(file_name=self.file_name,
                                   passage=self.match,
                                   document=self.doc)
        end_match_context = end_singlet.get_context(context_chars=pad_chars)
        self.assertEqual(len(end_match_context), len(self.match)+pad_chars)

        # Test match at start of body
        self.doc.body = self.body[loc:]
        beg_singlet = MatchSinglet(file_name=self.file_name,
                                   passage=self.match,
                                   document=self.doc)
        beg_match_context = beg_singlet.get_context(context_chars=pad_chars)
        self.assertEqual(len(beg_match_context), len(self.match)+pad_chars)

    def test_to_dict(self):
        """
        Test conversion to dict representation
        """
        sing_dict = self.singlet.to_dict()
        self.assertEqual(sing_dict['file_name'], self.file_name)
        self.assertEqual(sing_dict['passage'], self.match)
