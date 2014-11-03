import unittest

from processing.comparators import simple


class SimpleComparatorTest(unittest.TestCase):

    def test_compare(self):
        a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        b = 'Lorem ipsum dolor derp derp consectetur adipiscing a elit.'
        name_a = 'namea'
        name_b = 'nameb'
        simple_comparator = simple.Comparator(a=a,
                                              b=b,
                                              name_a=name_a,
                                              name_b=name_b,
                                              gap_length=4)
        matches = simple_comparator.compare()
        match_1 = 'Lorem ipsum dolor '
        self.assertEqual(matches[0].alpha.passage, match_1)
        self.assertEqual(matches[0].beta.passage, match_1)

        match_2 = 'et, consectetur adipiscing elit.'
        self.assertEqual(matches[1].alpha.passage, match_2)

        mb_2 = ' consectetur adipiscing sfelit.'
        self.assertEqual(matches[1].beta.passage, mb_2)
