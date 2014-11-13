import unittest
from mock import Mock

from processing.comparators import simple
from processing.processor import Processor


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
        tups = comparator.compare()
        alpha = Mock()
        alpha.body = a
        beta = Mock()
        beta.body = b
        matches = Processor.singlet_pairs_to_matches(alpha=alpha,
                                                     beta=beta,
                                                     singlet_pairs=tups)
        return matches

    def test_compare(self):
        a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        b = 'Lorem ipsum dolor xxxxxxxxx consectetur adipiscing a elit.'
        matches = self.match(a=a,
                             b=b,
                             gap_length=2,
                             match_length=3)
        self.assertEqual(len(matches), 2)

        match_1 = 'Lorem ipsum dolor '
        self.assertEqual(matches[0].alpha_passage, match_1)
        self.assertEqual(matches[0].beta_passage, match_1)

        match_2 = ' consectetur adipiscing elit.'
        self.assertEqual(matches[1].alpha_passage, match_2)

        mb_2 = ' consectetur adipiscing a elit.'
        self.assertEqual(matches[1].beta_passage, mb_2)

    def test_compare_match_len(self):
        a = 'Lorem xxxxx dolor sit amet, consectetur adipiscing ddd.'
        b = 'Lorem ipsum dolor xxxxxxxxx consectetur xxxxxxxxxx a.'
        matches = self.match(a, b, gap_length=0, match_length=9)
        self.assertEqual(len(matches), 1)

        m = ' consectetur '
        match = matches[0]
        # print match.alpha_passage
        # print match.beta_passage
        self.assertEqual(match.alpha_passage, m)
        self.assertEqual(match.beta_passage, m)

    def test_compare_gap_len_b(self):
        a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        b = 'Lorem xxipsum dolorxxxxsit amet, xconsectetur xxxadipiscing xelit.'
        matches = self.match(a, b, gap_length=5, match_length=1)
        self.assertEqual(len(matches), 1)

        match = matches[0]
        self.assertEqual(match.alpha_passage, a)
        self.assertEqual(match.beta_passage, b)

    def test_compare_gap_len_a(self):
        a = 'Lorem xxipsum dolor xxxsit amet, xconsectetur xxxadipiscing xelit.'
        b = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        matches = self.match(a, b, gap_length=5, match_length=1)
        self.assertEqual(len(matches), 1)

        match = matches[0]
        self.assertEqual(match.alpha_passage, a)
        self.assertEqual(match.beta_passage, b)

    def test_compare_gap(self):
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

# Example of how to make a test for another comparator
# class SimpleComparatorTestCase(ComparatorTestCase):
#     def setUp(self):
#         super(ComparatorTestCase, self).setUp()
#         self.Comparator = simple.Comparator
