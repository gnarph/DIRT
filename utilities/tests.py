import unittest

import utilities.path
from utilities import fuzzer


class PathTest(unittest.TestCase):

    def test_remove_dir(self):
        utilities.path.delete_folder('doesnotexistokay')


class FuzzerTest(unittest.TestCase):

    def test_fuzzer_fail(self):
        body = 'hello, world!'
        passage = 'xxx'
        self.assertRaises(fuzzer.FuzzerFailure,
                          fuzzer.find_in_body,
                          body, passage)

    def test_fuzzy_match(self):
        a = '0123456789abc'
        b = '01234g6789abc'
        match = fuzzer.is_fuzzy_match(a, b)
        self.assertTrue(match)
