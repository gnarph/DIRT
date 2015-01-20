import os
import unittest

import mock

import DIRT
from models.match_set import MatchSet
from models import match_set_factory
import utilities.path


def iter_match_passages(match_set):
    for match in match_set.matches:
        yield match.alpha_passage.strip()
        yield match.beta_passage.strip()


def contains_contains(l, search_for):
    for item in l:
        if search_for in item:
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

    def test_a(self):
        args = mock.Mock()
        args.input = 'test_data'
        args.preprocessed_dir = self.pre_dir
        args.output_dir = self.out_dir
        args.language = 'eng'
        args.comparator = 'simple'
        args.gap_length = 3
        args.match_length = 10
        DIRT.main(args)
        # TODO: test the outputs

    def test_b(self):
        args = mock.Mock()
        args.input = 'other_test_files/input_list.txt'
        args.preprocessed_dir = self.pre_dir
        args.output_dir = self.out_dir
        args.language = 'eng'
        args.comparator = 'simple'
        args.gap_length = 3
        args.match_length = 10
        DIRT.main(args)

    def test_z(self):
        args = mock.Mock()
        args.input = 'test_data/zhi'
        args.preprocessed_dir = self.pre_dir
        args.output_dir = self.out_dir
        args.language = 'zhi'
        args.comparator = 'simple'
        args.gap_length = 3
        args.match_length = 10
        DIRT.main(args)

    def full_test(self):
        args = mock.Mock()
        args.input = 'test_data/full_test/files_to_process.txt'
        args.preprocessed_dir = 'test_data/full_test/preprocessed'
        args.output_dir = self.out_dir
        args.language = 'eng'
        args.comparator = 'simple'
        args.gap_length = 10
        args.match_length = 10
        DIRT.main(args)

        one_two = match_set_factory.find_in_dir('one', 'two', self.out_dir)
        one_three = match_set_factory.find_in_dir('one', 'three', self.out_dir)
        three_two = match_set_factory.find_in_dir('three', 'two', self.out_dir)

        common_pass = ('This test file consists of multiple '
                       'paragraphs  This paragraph in particular '
                       'occurs in multiple test files  DIRT should '
                       'be able to determine this and create the '
                       'appropriate matches')
        passages_32 = list(iter_match_passages(three_two))
        found = contains_contains(passages_32, common_pass)
        self.assertTrue(found)

        passages_12 = list(iter_match_passages(one_two))
        found = contains_contains(passages_12, common_pass)
        self.assertTrue(found)

        passages_13 = list(iter_match_passages(one_three))
        found = contains_contains(passages_13, common_pass)
        self.assertTrue(found)
