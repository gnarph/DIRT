import unittest
import logging

import utilities.path
from utilities import fuzzer
import utilities.logger


class PathTest(unittest.TestCase):

    def test_remove_dir(self):
        utilities.path.delete_folder('doesnotexistokay')


class FuzzerTest(unittest.TestCase):

    def test_fuzzy_match(self):
        a = '0123456789abc'
        b = '01234g6789abc'
        match = fuzzer.is_fuzzy_match(a, b)
        self.assertTrue(match)

    def test_fuzzy_not_match(self):
        a = '01235465'
        b = '012teststring'
        match = fuzzer.is_fuzzy_match(a, b)
        self.assertFalse(match)


class LoggerTest(unittest.TestCase):

    def test_show_info(self):
        utilities.logger.show_info()
        logger = utilities.logger.get_logger()
        log_level = logger.getEffectiveLevel()
        self.assertEqual(log_level, logging.INFO)
