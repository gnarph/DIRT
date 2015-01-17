import unittest
from mock import Mock

from processing.comparators import simple
from processing.processor import Processor
from processing.comparators.match_concatenator import MatchConcatenator
from processing.comparators.match_concatenator import MatchTuple
from models.match_set import MatchSet


class MatchConcatenatorTestCase(unittest.TestCase):

    def test_no_matches(self):
        matches = []
        concatenator = MatchConcatenator(match_list=matches,
                                         gap_length=3)
        combined = concatenator.concatenate()
        self.assertEqual(combined, [])

    def test_combine_at_end(self):
        first = MatchTuple(a=0,
                           b=0,
                           a_end=4,
                           b_end=5)
        second = MatchTuple(a=6,
                            b=6,
                            a_end=8,
                            b_end=8)
        concatenator = MatchConcatenator(match_list=[first, second],
                                         gap_length=5)
        combined = concatenator.concatenate()
        self.assertEqual(len(combined), 1)


class ComparatorTestCase(unittest.TestCase):
    """
    General test for comparators
    """

    name_a = 'namea'
    name_b = 'nameb'

    def setUp(self):
        self.Comparator = simple.Comparator

    def match(self, a, b, gap_length, match_length):
        comparator = self.Comparator(a=a,
                                     b=b,
                                     name_a=self.name_a,
                                     name_b=self.name_b,
                                     gap_length=gap_length,
                                     match_length=match_length)
        singlet_pairs = comparator.compare()
        alpha = Mock()
        alpha.raw_body = a
        alpha.pre_body = a
        beta = Mock()
        beta.raw_body = b
        beta.pre_body = b
        matches = Processor.singlet_pairs_to_matches(alpha=alpha,
                                                     beta=beta,
                                                     singlet_pairs=singlet_pairs)
        return MatchSet(None, None, matches=matches)

    def test_compare(self):
        """
        Basic comparator test
        """
        a = 'Lorem ipsum dolor sit amet  consectetur adipiscing elit '
        b = 'Lorem ipsum dolor xxxxxxxxx consectetur adipiscing a elit '
        matches = self.match(a=a,
                             b=b,
                             gap_length=2,
                             match_length=3)
        self.assertEqual(len(matches), 2)
        matched_passages = matches.all_passages()
        # need to make matched passages into match set

        match_1 = 'Lorem ipsum dolor '
        self.assertIn(match_1, matched_passages)
        # self.assertEqual(matches[0].alpha_passage, match_1)
        # self.assertEqual(matches[0].beta_passage, match_1)

        match_2 = ' consectetur adipiscing elit.'
        self.assertIn(match_2, matched_passages)
        # self.assertEqual(matches[1].alpha_passage, match_2)

        mb_2 = ' consectetur adipiscing a elit.'
        self.assertIn(mb_2, matched_passages)
        # self.assertEqual(matches[1].beta_passage, mb_2)

    def test_compare_match_len(self):
        """
        Test match length criteria
        """
        a = 'Lorem xxxxx dolor sit amet, consectetur adipiscing ddd.'
        b = 'Lorem ipsum dolor zzzzzzzzz consectetur zzzzzzzzzz a.'
        matches = self.match(a, b, gap_length=0, match_length=9)
        self.assertEqual(len(matches), 1)

        m = ' consectetur '
        match = matches[0]
        self.assertEqual(match.alpha_passage, m)
        self.assertEqual(match.beta_passage, m)

    def test_compare_gap_len_b(self):
        """
        Test gap jumping, with gaps in b
        """
        a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        b = 'Lorem xxipsum dolorxxxxsit amet, xconsectetur xxxadipiscing xelit.'
        matches = self.match(a, b, gap_length=5, match_length=1)
        self.assertEqual(len(matches), 1)

        match = matches[0]
        self.assertEqual(match.alpha_passage, a)
        self.assertEqual(match.beta_passage, b)

    def test_compare_gap_len_a(self):
        """
        Test gap jumping, with gaps in a
        """
        a = 'Lorem xxipsum dolor xxxsit amet, xconsectetur xxxadipiscing xelit.'
        b = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        matches = self.match(a, b, gap_length=5, match_length=1)
        self.assertEqual(len(matches), 1)

        match = matches[0]
        self.assertEqual(match.alpha_passage, a)
        self.assertEqual(match.beta_passage, b)

    def test_compare_gap_long_b(self):
        """
        Something
        """
        a = 'Lorem ipsum'
        b = 'Lorem dolor amit ipsum'
        matches = self.match(a, b, gap_length=20, match_length=15)
        self.assertEqual(len(matches), 1)

        match = matches[0]
        self.assertEqual(match.alpha_passage, a)
        self.assertEqual(match.beta_passage, b)

    def test_compare_gap(self):
        """
        Test gap jumping, with different lengths of matches
        """
        a = 'Lorem xxipsum dolorxxxxxxsit amet, xconsectetur xxxadipiscing xelit.'
        b = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        matches = self.match(a, b, gap_length=3, match_length=2)
        self.assertEqual(len(matches), 2)

        match = matches[0]
        m1_a = 'Lorem xxipsum dolor'
        # TODO: fix gap based size adjust when a is bigger
        m1_b = 'Lorem ipsum dolor'
        self.assertEqual(match.alpha_passage, m1_a)
        self.assertEqual(match.beta_passage, m1_b)

        m2 = matches[1]
        m2_a = 'sit amet, xconsectetur xxxadipiscing xelit.'
        m2_b = 'sit amet, consectetur adipiscing elit.'
        self.assertEqual(m2.alpha_passage, m2_a)
        self.assertEqual(m2.beta_passage, m2_b)

    def test_out_of_order(self):
        """
        Check that the matcher is able to match up blocks
        where block x appears first in body a, second in
        body a, and block y appears first in body b,
        second in body a
        """
        a = 'Lorem ipsum dolor amit'
        b = 'dolor amit Lorem ipsum'
        matches = self.match(a, b, gap_length=3, match_length=3)
        self.assertEqual(len(matches), 2)

        m1 = matches[0]
        p1 = 'Lorem ipsum'
        self.assertEqual(m1.alpha_passage, p1)
        self.assertEqual(m1.beta_passage, p1)

        m2 = matches[1]
        p2 = 'dolor amit'
        self.assertEqual(m2.alpha_passage, p2)
        self.assertEqual(m2.beta_passage, p2)

# Example of how to make a test for another comparator
# class SimpleComparatorTestCase(ComparatorTestCase):
#     def setUp(self):
#         super(ComparatorTestCase, self).setUp()
#         self.Comparator = simple.Comparator
