import unittest
import logging

import utilities.path
from utilities import fuzzer
import utilities.logger


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

    def test_longer_passage(self):
        passage = 'a longer passage'
        body = 'longer'
        start, end = fuzzer.find_in_body(body=body,
                                         passage=passage)
        self.assertEqual(start, 0)
        self.assertEqual(end, len(body))

    def test_double_match(self):
        passage = 'name'
        body = 'name is a name in name'
        start, end = fuzzer.find_in_body(body=body,
                                         passage=passage)

        self.assertEqual(start, 0)
        # fails
        self.assertEqual(end, 4)


class LoggerTest(unittest.TestCase):

    def test_show_info(self):
        utilities.logger.show_info()
        logger = utilities.logger.get_logger()
        log_level = logger.getEffectiveLevel()
        self.assertEqual(log_level, logging.INFO)
