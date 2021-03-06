import unittest

import mock

import DIRT
from models import match_set_factory
import utilities.path


def iter_match_passages(match_set):
    for match in match_set.matches:
        yield match.alpha_passage
        yield match.beta_passage


def contains_contains(l, search_for):
    for item in l:
        if search_for in item or item in search_for:
            return True
    return False


class SmokeTest(unittest.TestCase):

    pre_dir = 'test_preprocessed'
    out_dir = 'test_output'

    def _reset_dirs(self):
        utilities.path.reset_folder(self.pre_dir)
        utilities.path.reset_folder(self.out_dir)

    def setUp(self):
        self._reset_dirs()

    def tearDown(self):
        self._reset_dirs()

    def _no_matchset_dupes(self, ms):
        found = set()
        for match in ms:
            self.assertNotIn(match, found)
            found.add(match)

    def full_test(self):
        args = mock.Mock()
        args.input = 'test_data/full_test/files_to_process.txt'
        args.preprocessed_dir = 'test_data/full_test/preprocessed'
        args.output_dir = self.out_dir
        # TODO: use zhi
        args.language = 'eng'
        args.comparator = 'simple'
        args.gap_length = 10
        args.match_length = 10
        # Nosetests doesn't seem to like multiprocessing
        args.parallel = False
        DIRT.main(args)

        one_two = match_set_factory.find_in_dir('one', 'two', self.out_dir)
        one_three = match_set_factory.find_in_dir('one', 'three', self.out_dir)
        three_two = match_set_factory.find_in_dir('three', 'two', self.out_dir)

        common_pass = (u'This test file consists of multiple '
                       u'paragraphs  This paragraph in particular '
                       u'occurs in multiple test files  DIRT should '
                       u'be able to determine this and create the '
                       u'appropriate matches')
        passages_32 = list(iter_match_passages(three_two))
        found = contains_contains(passages_32, common_pass)
        self.assertTrue(found)

        passages_12 = list(iter_match_passages(one_two))
        found = contains_contains(passages_12, common_pass)
        self.assertTrue(found)

        passages_13 = list(iter_match_passages(one_three))
        found = contains_contains(passages_13, common_pass)
        self.assertTrue(found)

        self._no_matchset_dupes(one_two)
        self._no_matchset_dupes(one_three)
        self._no_matchset_dupes(three_two)

        # Check matched passages
        self.assertTrue(contains_contains(passages_12,
                                          search_for=u'ONEANDTWO'))
        self.assertTrue(contains_contains(passages_13,
                                          search_for=u'ONEANDTHREE'))
        self.assertTrue(contains_contains(passages_32,
                                          search_for=u'TWOANDTHREE'))
