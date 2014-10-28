import unittest

import mock

from models.document import Document
from models.match_singlet import MatchSinglet


class DocumentTest(unittest.TestCase):
    file_name = 'this_is_a_file.txt'
    meta = {'title': 'test yeah',
            'author': 'gord'
           }
    body = 'In id tristique orci. Aenean.'

    def test_clone(self):
        doc = Document(file_name=self.file_name,
                       body=self.body,
                       metadata=self.meta)
        doc_cloned = doc.clone()
        self.assertEqual(doc_cloned.file_name, doc.file_name)
        self.assertEqual(doc_cloned.metadata, doc.metadata)
        self.assertEqual(doc_cloned.body, doc.body)
        self.assertEqual(doc, doc_cloned)

        doc_cloned.file_name = 'nope'
        self.assertNotEqual(doc, doc_cloned)

        doc_cloned.file_name = doc.file_name
        doc_cloned.metadata = None
        self.assertNotEqual(doc, doc_cloned)

        doc_cloned.metadata = doc.metadata
        doc_cloned.body = ''
        self.assertNotEqual(doc, doc_cloned)


class MatchSingletTest(unittest.TestCase):

    def setUp(self):
        self.file_name = 'name of file'
        self.doc = mock.Mock
        self.context_pad = ' context '
        self.match = 'this is the match'
        self.with_context = '{pad}{match}{pad}'.format(pad=self.context_pad,
                                                       match=self.match)
        fmt = 'asdfalakjvlzx{}cvowvkjzoxijoidsjfq'
        self.doc.body = fmt.format(self.with_context)

    def test_get_context(self):
        singlet = MatchSinglet(filename=self.file_name,
                               passage=self.match,
                               document=self.doc)
        pad_chars = len(self.context_pad)
        match_with_context = singlet.get_context(context_chars=pad_chars)
        self.assertEqual(match_with_context, self.with_context)
