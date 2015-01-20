# -*- coding: utf-8 -*-
import unittest

from utilities.suffix_array import applications as app
from utilities import file_ops


def strip_set(s):
    new_set = set()
    for i in s:
        strip = i.strip(u' \t\n\r')
        r = strip.replace(u'\n', u'')
        r = r.replace(u'.', u'')
        new_set.add(r)
    return new_set


class SuffixArrayApplicationTest(unittest.TestCase):

    def test_acs_small(self):
        a = u'jeffisacoolguywhoiscool'
        b = u'whoiscooljeffisacoolguy'
        acs = app.all_common_substrings(a, b)
        self.assertIn(u'jeffisacoolguy', acs)
        self.assertIn(u'whoiscool', acs)
        self.assertEqual(len(acs), 2)

        a = u'aabbccdefaabbcc'
        b = u'defabcc'
        acs = app.all_common_substrings(a, b)
        self.assertIn(u'defa', acs)
        self.assertIn(u'bcc', acs)
        self.assertIn(u'ab', acs)
        self.assertEqual(len(acs), 3)

        a = u'sallyjohndeer'
        b = u'johnnyrobinpear'
        c = u'chairlairjohn'
        ab = app.all_common_substrings(a, b)
        ac = app.all_common_substrings(a, c)
        bc = app.all_common_substrings(b, c)
        in_all = ab & ac & bc
        self.assertIn(u'john', in_all)

    def test_acs_except(self):
        a = u'dolla$bills'
        b = u'yo'
        should_raise = app.InvalidCharacterException
        to_call = app.all_common_substrings
        self.assertRaises(should_raise, to_call, a, b)

    def test_acs_large(self):
        f_one = 'test_data/full_test/one.txt'
        f_two = 'test_data/full_test/two.txt'
        f_three = 'test_data/full_test/three.txt'

        one = file_ops.read_utf8(f_one)
        two = file_ops.read_utf8(f_two)
        three = file_ops.read_utf8(f_three)

        one_two = app.all_common_substrings(one, two)
        one_three = app.all_common_substrings(one, three)
        two_three = app.all_common_substrings(two, three)

        # Strip is somewhat hacky
        strip_a = strip_set(one_two)
        strip_b = strip_set(one_three)
        strip_c = strip_set(two_three)

        in_all = strip_a & strip_b & strip_c
        self.assertGreaterEqual(len(in_all), 1)
