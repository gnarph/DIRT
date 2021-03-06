# -*- coding: utf-8 -*-
import os
import unittest

import cjson
import codecs
import mock

from processing.processor import Processor
from models.document import Document
from models.document import InvalidDocumentException
import models.match_set_factory as match_set_factory
from models.match import Match
from models.match_singlet import MatchHalf
from models.match_set import MatchSet
from models.match_set_index import MatchSetIndex
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
        """
        Test opening a Document json
        """
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
        self.singlet = MatchHalf(passage=self.match)

    def test_eq(self):
        """
        Test MatchSinglet equality
        """
        singlet_a = MatchHalf(passage="test")
        singlet_b = MatchHalf(passage="test")
        singlet_c = MatchHalf(passage="nope")

        self.assertTrue(singlet_a == singlet_b)
        self.assertFalse(singlet_a == singlet_c)
        self.assertFalse(singlet_b == singlet_c)


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

    def test_eq(self):
        """
        Test match equality
        """
        a = Match(alpha_passage=u'one',
                  alpha_indices=(3, 5),
                  beta_passage=u'two',
                  beta_indices=(9, 11))
        b = Match(alpha_passage=u'two',
                  alpha_indices=(9, 11),
                  beta_passage=u'one',
                  beta_indices=(3, 5))
        c = Match(alpha_passage=u'five',
                  alpha_indices=(44, 47),
                  beta_passage=u'six',
                  beta_indices=(0, 3))

        self.assertTrue(a == b)
        self.assertFalse(a == c)
        self.assertFalse(b == c)

        # If objects are equal their hashes must also be equal
        hash_a = hash(a)
        hash_b = hash(b)
        hash_c = hash(c)
        self.assertTrue(hash_a == hash_b)
        self.assertFalse(hash_a == hash_c)
        self.assertFalse(hash_b == hash_c)

    def test_swap_alpha_beta(self):
        """
        Test swapping alpha and beta documents
        """
        alpha_passage = u'one'
        alpha_indices = (3, 5)
        beta_passage = u'two'
        beta_indices = (9, 11)
        a = Match(alpha_passage=alpha_passage,
                  alpha_indices=alpha_indices,
                  beta_passage=beta_passage,
                  beta_indices=beta_indices)
        a.swap_alpha_beta()

        self.assertEqual(a.beta_passage, alpha_passage)
        self.assertEqual(a.beta_indices, alpha_indices)
        self.assertEqual(a.alpha_passage, beta_passage)
        self.assertEqual(a.alpha_indices, beta_indices)


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
            a = MatchHalf(passage=self.passages_a[i])
            b = MatchHalf(passage=self.passages_b[i])
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
        """
        Test serialization i.e. to_dict
        """
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
        """
        Test get match percentage
        """
        a, b = self.match_set.get_match_percentage()
        self.assertEqual(a, 62.5)
        self.assertAlmostEqual(b, 58.823, places=1)

    def test_swap(self):
        """
        Test swapping alpha and beta docs
        """
        self.match_set.swap_alpha_beta()

        # Check passages have swapped
        a_passages = set(self.passages_a)
        b_passages = set(self.passages_b)

        ap = set(self.match_set.alpha_passages())
        bp = set(self.match_set.beta_passages())

        self.assertEqual(b_passages, ap)
        self.assertEqual(a_passages, bp)


class MatchSetIndexTest(unittest.TestCase):
    out_dir = 'models/test_data/out'

    def test_set_names_for_focus(self):
        """
        Test set names for focus
        """
        focus_name = 'focus'
        msi = MatchSetIndex(self.out_dir)

        gen_names = msi.set_names_for_focus(focus_name)
        names = set(gen_names)

        wanted_names = ['focus__otherdoc__CMP.json',
                        'nototherdoc__focus__CMP.json']

        def join_path(name):
            return os.path.join(self.out_dir, name)
        paths = map(join_path, wanted_names)
        self.assertEqual(names, set(paths))

    def test_get_all_match_sets(self):
        focus_name = 'focus'
        msi = MatchSetIndex(self.out_dir)

        match_sets = msi.get_all_match_sets(focus_name)
        self.assertEqual(len(match_sets), 2)

        for ms in match_sets:
            a = ms.alpha_doc
            self.assertIn(focus_name, a.file_name)

    def test_get_all_file_names(self):
        expected = {'focus', 'otherdoc', 'nototherdoc'}
        msi = MatchSetIndex(self.out_dir)

        files = msi.get_all_file_names()
        self.assertEqual(files, expected)

    def test_get_all_matched_documents(self):
        msi = MatchSetIndex(self.out_dir)
        all_docs = msi.get_all_matched_documents('focus')
        self.assertEqual(len(all_docs), 2)
