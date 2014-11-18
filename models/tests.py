# -*- coding: utf-8 -*-
import unittest

import cjson
import codecs
import mock

from processing.processor import Processor
from models.document import Document
from models.document import InvalidDocumentException
import models.match_set_factory as match_set_factory
from models.match import Match
from models.match_singlet import MatchSinglet
from models.match_set import MatchSet
from utilities.fuzzer import is_fuzzy_match


class DocumentTest(unittest.TestCase):
    file_name = u'models/test_data/lorem.json'
    meta = {'title': u'test 稢綌',
            'author': u'gorden 胇赲'
            }
    body = u'In id tristique orci. 痵痽 犵艿邔 疿疶砳 齸圞趲.'
    pre_file_name = file_name + '_PRE.json'
    raw_file_name = file_name

    def setUp(self):
        self.doc = Document(file_name=self.file_name,
                            metadata=self.meta,
                            pre_file_name=self.pre_file_name,
                            raw_file_name=self.raw_file_name)

    def test_clone(self):
        """
        Test cloning a document
        """
        doc_cloned = self.doc.clone()
        self.assertEqual(doc_cloned.file_name, self.doc.file_name)
        self.assertEqual(doc_cloned.pre_file_name, self.doc.pre_file_name)
        self.assertEqual(doc_cloned.raw_file_name, self.doc.raw_file_name)
        self.assertEqual(doc_cloned.metadata, self.doc.metadata)
        self.assertEqual(doc_cloned.raw_body, self.doc.raw_body)
        self.assertEqual(self.doc, doc_cloned)

        # using assertFalse instead of assertNotEqual in order to
        # test __eq__
        doc_cloned.file_name = u'nope'
        self.assertFalse(self.doc == doc_cloned)

        doc_cloned.file_name = self.doc.file_name
        doc_cloned.metadata = None
        self.assertFalse(self.doc == doc_cloned)

        doc_cloned.metadata = self.doc.metadata
        doc_cloned.raw_file_name = ''
        self.assertFalse(self.doc == doc_cloned)

        doc_cloned.raw_file_name = self.doc.raw_file_name
        doc_cloned.pre_file_name = ''
        self.assertFalse(self.doc == doc_cloned)

    def test_to_dict(self):
        """
        Test conversion to dictionary (for json serialization)
        """
        doc_dict = self.doc.to_dict()
        self.assertEqual(doc_dict['file_name'], self.doc.file_name)
        self.assertEqual(doc_dict['metadata'], self.doc.metadata)
        self.assertEqual(doc_dict['pre_file_name'], self.doc.pre_file_name)
        # TODO check raw

    def test_open(self):
        self.assertRaises(InvalidDocumentException,
                          Document.from_json,
                          'models/test_data/invalid.json')
        self.assertRaises(InvalidDocumentException,
                          Document.from_json,
                          'models/test_data/invalid.txt')


class MatchSingletTest(unittest.TestCase):

    def setUp(self):
        self.file_name = u'models/test_data/lorem.json'
        self.doc = mock.Mock
        self.context_pad = u' context垥娀 '
        self.match = u'this is 檦 the match'
        self.with_context = u'{pad}{match}{pad}'.format(pad=self.context_pad,
                                                        match=self.match)
        fmt = u'duck goose raccoon{}鬐鶤鶐膗,觾韄煔垥'
        self.doc.body = fmt.format(self.with_context)
        self.doc.file_name = self.file_name
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
        self.assertTrue(is_fuzzy_match(match_with_context, self.with_context))

        # Test match at end of body
        loc = self.body.find(self.match)
        end_match = loc + len(self.match)
        self.doc.body = self.doc.body[:end_match]
        end_singlet = MatchSinglet(file_name=self.file_name,
                                   passage=self.match,
                                   document=self.doc)
        end_match_context = end_singlet.get_context(context_chars=pad_chars)
        self.assertIn(self.match, end_match_context)

        # Test match at start of body
        self.doc.body = self.body[loc:]
        beg_singlet = MatchSinglet(file_name=self.file_name,
                                   passage=self.match,
                                   document=self.doc)
        beg_match_context = beg_singlet.get_context(context_chars=pad_chars)
        self.assertIn(self.match, beg_match_context)

    def test_to_dict(self):
        """
        Test conversion to dict representation
        """
        sing_dict = self.singlet.to_dict()
        self.assertEqual(sing_dict['file_name'], self.file_name)
        self.assertEqual(sing_dict['passage'], self.match)

    def test_document(self):
        """
        Test getting document
        """
        sing = MatchSinglet(file_name='models/test_data/lorem.json',
                            passage=u'청춘의 피가 심장의 많이')
        doc = sing.document
        self.assertEqual(doc.file_name, 'models/test_data/lorem.json')
        self.assertEqual(doc.raw_file_name, 'models/test_data/raw/lorem.txt')
        body = u'품에 원대하고, 무엇을 무한한 사막이다. 청춘의 피가 심장의 많이 열락의 무엇을 아니다.'
        self.assertEqual(doc.raw_body, body)
        meta = {}
        self.assertEqual(doc.metadata, meta)

    # TODO: test eq


class MatchTest(unittest.TestCase):

    def setUp(self):
        self.alpha_name = 'a_name'
        self.alpha_passage = 'a_passage'
        self.alpha_indices = (0, 12)
        self.beta_name = 'b_name'
        self.beta_passage = 'b_passage'
        self.beta_indices = (12, 24)
        self.match = Match(alpha_passage=self.alpha_passage,
                           alpha_indices=self.alpha_indices,
                           beta_passage=self.beta_passage,
                           beta_indices=self.beta_indices)

    def test_to_dict(self):
        """
        Test dict conversion for JSON serialization
        """
        match_dict = self.match.to_dict()
        self.assertEqual(self.alpha_passage, match_dict['alpha_passage'])
        self.assertEqual(self.alpha_indices, match_dict['alpha_indices'])
        self.assertEqual(self.beta_passage, match_dict['beta_passage'])
        self.assertEqual(self.beta_indices, match_dict['beta_indices'])

        # todo: test eq


class MatchSetTest(unittest.TestCase):

    def setUp(self):
        self.passages_a = [chr(i + ord('a')) for i in xrange(10)]
        self.passages_b = [chr(i + ord('A')) for i in xrange(10)]
        self.file_a = 'models/test_data/match_set_test.json'
        self.document_a = Document.from_json(self.file_a)
        self.file_b = 'models/test_data/match_set_test2.json'
        self.document_b = Document.from_json(self.file_b)

        self.matches = []
        self.singlet_pairs = []
        for i in xrange(len(self.passages_a)):
            a = MatchSinglet(file_name=self.document_a,
                             passage=self.passages_a[i])
            b = MatchSinglet(file_name=self.document_b,
                             passage=self.passages_b[i])
            s_pair = (a, b)
            self.singlet_pairs.append(s_pair)
            # Alpha/beta need to be actual documents, not names
        self.matches = Processor.singlet_pairs_to_matches(alpha=self.document_a,
                                                          beta=self.document_b,
                                                          singlet_pairs=self.singlet_pairs)
        self.match_set = MatchSet(alpha_doc=self.document_a,
                                  beta_doc=self.document_b,
                                  matches=self.matches)

    def test_serialize(self):
        match_set_dict = self.match_set.to_dict()
        match_set_json = cjson.encode(match_set_dict)
        deserialized_dict = cjson.decode(match_set_json)
        deserialized_match_set = MatchSet.from_dict(deserialized_dict)

        match_count = len(self.match_set.matches)
        deserialized_match_count = len(deserialized_match_set.matches)
        self.assertEqual(match_count, deserialized_match_count)
        self.assertTrue(self.match_set == deserialized_match_set)

        test_file = 'test_output/match_set_test.json'

        with codecs.open(test_file, 'w+', encoding='utf8') as f:
            f.write(match_set_json)

        deserialized_ms2 = match_set_factory.from_json(test_file)
        ms2_count = len(deserialized_ms2.matches)
        self.assertEqual(match_count, ms2_count)
        self.assertTrue(self.match_set == deserialized_ms2)

        # Should test, more of a hack check for now
        fn = self.match_set.get_file_names()
        doc_a_name, doc_b_name = fn
        self.assertEqual(doc_a_name, self.file_a)
        self.assertEqual(doc_b_name, self.file_b)
        inds = self.match_set.get_indices()
        self.assertEqual(len(inds), len(self.matches))
    # TODO: test eq

    def test_percentage(self):
        a, b = self.match_set.get_match_percentage()
        self.assertEqual(a, 62.5)
        self.assertAlmostEqual(b, 58.823, places=1)
