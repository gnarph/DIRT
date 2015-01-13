import os
import unittest

import mock

import DIRT
from models.match_set import MatchSet
import utilities.path


def iter_match_passages(match_set):
    for match in match_set.matches:
        yield match.alpha_passage.strip()
        yield match.beta_passage.strip()


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

    def _get_match_set(self, name):
        file_name = os.path.join(self.out_dir,
                                 name)
        return MatchSet.from_json(file_name)

    def full_test(self):
        args = mock.Mock()
        args.input = 'test_data/full_test/files_to_process.txt'
        args.preprocessed_dir = 'test_data/full_test/preprocessed'
        args.output_dir = self.out_dir
        args.language = 'eng'
        args.comparator = 'simple'
        args.gap_length = 3
        args.match_length = 10
        DIRT.main(args)

        one_two = self._get_match_set('one__two__CMP.json')
        one_three = self._get_match_set('one__three__CMP.json')
        three_two = self._get_match_set('three__two__CMP.json')

        common_pass = ('This test file consists of mutiple '
                       'paragraphs. This paragraph in particular '
                       'occurs in multiple test files. DIRT should '
                       'be able to determine this and create the '
                       'appropriate matches.')
        passages_32 = list(iter_match_passages(three_two))
        assert(common_pass in passages_32)

        try:
            passages_12 = list(iter_match_passages(one_two))
            assert(common_pass in passages_12)
        except AssertionError:
            print passages_12
            raise

