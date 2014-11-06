import unittest

from processing.comparators import simple


class ComparatorTestCase(unittest.TestCase):
    """
    General test for comparators
    """

    name_a = 'namea'
    name_b = 'nameb'

    def setUp(self):
        self.Comparator = simple.Comparator

    def test_compare(self):
        a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        b = 'Lorem ipsum dolor derp derp consectetur adipiscing a elit.'
        comparator = self.Comparator(a=a,
                                            b=b,
                                            name_a=self.name_a,
                                            name_b=self.name_b,
                                            gap_length=2,
                                            match_length=1)
        matches = comparator.compare()
        self.assertEqual(len(matches), 2)

        match_1 = 'Lorem ipsum dolor '
        self.assertEqual(matches[0].alpha.passage, match_1)
        self.assertEqual(matches[0].beta.passage, match_1)

        match_2 = ' consectetur adipiscing elit.'
        self.assertEqual(matches[1].alpha.passage, match_2)

        mb_2 = ' consectetur adipiscing a elit.'
        self.assertEqual(matches[1].beta.passage, mb_2)

    def test_compare_match_len(self):
        a = 'Lorem xxxxx dolor sit amet, consectetur adipiscing xxxx.'
        b = 'Lorem ipsum dolor xxx xxxxx consectetur xxxxxxxxxx a.'
        comparator = self.Comparator(a=a,
                                            b=b,
                                            name_a=self.name_a,
                                            name_b=self.name_b,
                                            gap_length=0,
                                            match_length=10)
        matches = comparator.compare()
        self.assertEqual(len(matches), 1)

        m = ' consectetur '
        match = matches[0]
        self.assertEqual(match.alpha.passage, m)
        self.assertEqual(match.beta.passage, m)

    def test_compare_gap_len_b(self):
        a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        b = 'Lorem xxipsum dolor xxxsit amet, xconsectetur xxxadipiscing xelit.'
        simple_comparator = self.Comparator(a=a,
                                            b=b,
                                            name_a=self.name_a,
                                            name_b=self.name_b,
                                            gap_length=5,
                                            match_length=1)
        matches = simple_comparator.compare()
        self.assertEqual(len(matches), 1)

        match = matches[0]
        self.assertEqual(match.alpha.passage, a)
        self.assertEqual(match.beta.passage, b)

    def test_compare_gap_len_a(self):
        a = 'Lorem xxipsum dolor xxxsit amet, xconsectetur xxxadipiscing xelit.'
        b = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        comparator = self.Comparator(a=a,
                                            b=b,
                                            name_a=self.name_a,
                                            name_b=self.name_b,
                                            gap_length=5,
                                            match_length=1)
        matches = comparator.compare()
        self.assertEqual(len(matches), 1)

        match = matches[0]
        self.assertEqual(match.alpha.passage, a)
        self.assertEqual(match.beta.passage, b)


# Example of how to make a test for another comparator
# class SimpleComparatorTestCase(ComparatorTestCase):
#     def setUp(self):
#         super(ComparatorTestCase, self).setUp()
#         self.Comparator = simple.Comparator
