import unittest

from processing.comparators import simple


class SimpleComparatorTest(unittest.TestCase):

    def test_compare(self):
        a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        b = 'Lorem ipsum dolor derp derp consectetur adipiscing sfelit'
        simple_comparator = simple.Comparator(a=a,
                                              b=b,
                                              gap_length=3)
        matches = simple_comparator.compare()
        match_1 = 'Lorem ipsum dolor '
        self.assertEqual(matches[0].alpha.passage, match_1)

        match_2 = ' consectetur adipiscing elit'
        self.assertEqual(matches[1].alpha.passage, match_2)
