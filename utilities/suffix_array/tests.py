# -*- coding: utf-8 -*-
import unittest

from utilities.suffix_array import matcher as app
from utilities import file_ops


def strip_set(s):
    """
    Strips character we don't care about from the strings in
    a set
    :param s: set of strings
    :return: set of strings without unwanted characters
    """
    new_set = set()
    for i in s:
        strip = i.strip(u' \t\n\r')
        r = strip.replace(u'\n', u'')
        r = r.replace(u'.', u'')
        new_set.add(r)
    return new_set


class SuffixArrayAllTest(unittest.TestCase):

    def test_acs_small(self):
        """
        Test on small strings
        """
        a = u'jeffisacoolguywhoiscool'
        b = u'whoiscooljeffisacoolguy'
        acs = app.acs_all(a, b)
        self.assertIn(u'jeffisacoolguy', acs)
        self.assertIn(u'whoiscool', acs)

        a = u'aabbccdefaabbcc'
        b = u'defabcc'
        acs = app.acs_all(a, b)
        self.assertIn(u'defa', acs)
        self.assertIn(u'bcc', acs)
        self.assertIn(u'ab', acs)

        a = u'sallyjohndeer'
        b = u'johnnyrobinpear'
        c = u'chairlairjohn'
        ab = app.acs_all(a, b)
        ac = app.acs_all(a, c)
        bc = app.acs_all(b, c)
        in_all = set(ab) & set(ac) & set(bc)
        self.assertIn(u'john', in_all)

    def test_acs_except(self):
        """
        Test an exception is raised if the separator character
        is present in an input string
        """
        a = u'dolla$bills'
        b = u'yo'
        should_raise = app.InvalidCharacterException
        to_call = app.acs_all
        self.assertRaises(should_raise, to_call, a, b)

        a, b = b, a
        self.assertRaises(should_raise, to_call, a, b)

    # Skip this test as it is prohibitively slow
    @unittest.skip
    def test_acs_large(self):
        """
        Test on actual documents
        """
        f_one = 'test_data/full_test/one.txt'
        f_two = 'test_data/full_test/two.txt'
        f_three = 'test_data/full_test/three.txt'

        one = file_ops.read_utf8(f_one)
        two = file_ops.read_utf8(f_two)
        three = file_ops.read_utf8(f_three)

        one_two = app.acs_all(one, two)
        one_three = app.acs_all(one, three)
        two_three = app.acs_all(two, three)

        # TODO: replace with check for static string
        strip_a = strip_set(one_two)
        strip_b = strip_set(one_three)
        strip_c = strip_set(two_three)

        in_all = strip_a & strip_b & strip_c
        self.assertGreaterEqual(len(in_all), 1)


class SuffixArrayNoSubsTest(unittest.TestCase):

    def test_acs_small(self):
        """
        Test on small strings
        """
        a = u'jeffisacoolguywhoiscool'
        b = u'whoiscooljeffisacoolguy'
        acs = app.acs_no_substrings(a, b)
        self.assertIn(u'jeffisacoolguy', acs)
        self.assertIn(u'whoiscool', acs)

        a = u'aabbccdefaabbcc'
        b = u'defabcc'
        acs = app.acs_no_substrings(a, b)
        self.assertIn(u'defa', acs)
        self.assertIn(u'bcc', acs)
        self.assertIn(u'ab', acs)

        a = u'sallyjohndeer'
        b = u'johnnyrobinpear'
        c = u'chairlairjohn'
        ab = app.acs_no_substrings(a, b)
        ac = app.acs_no_substrings(a, c)
        bc = app.acs_no_substrings(b, c)
        in_all = set(ab) & set(ac) & set(bc)
        self.assertIn(u'john', in_all)

    def test_acs_except(self):
        """
        Test an exception is raised if the separator character
        is present in an input string
        """
        a = u'dolla$bills'
        b = u'yo'
        should_raise = app.InvalidCharacterException
        to_call = app.acs_no_substrings
        self.assertRaises(should_raise, to_call, a, b)

        a, b = b, a
        self.assertRaises(should_raise, to_call, a, b)

    def test_acs_large(self):
        """
        Test on actual documents
        """
        f_one = 'test_data/full_test/one.txt'
        f_two = 'test_data/full_test/two.txt'
        f_three = 'test_data/full_test/three.txt'

        one = file_ops.read_utf8(f_one)
        two = file_ops.read_utf8(f_two)
        three = file_ops.read_utf8(f_three)

        one_two = app.acs_no_substrings(one, two)
        one_three = app.acs_no_substrings(one, three)
        two_three = app.acs_no_substrings(two, three)

        # TODO: replace with check for static string
        strip_a = strip_set(one_two)
        strip_b = strip_set(one_three)
        strip_c = strip_set(two_three)

        in_all = strip_a & strip_b & strip_c
        self.assertGreaterEqual(len(in_all), 1)
