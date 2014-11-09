import os
import unittest
import shutil

import mock

import DIRT


class SmokeTest(unittest.TestCase):

    pre_dir = 'test_preprocessed'
    out_dir = 'test_output'

    def _reset_dirs(self):
        try:
            shutil.rmtree(self.pre_dir)
        except OSError:
            pass
        try:
            shutil.rmtree(self.out_dir)
        except OSError:
            pass
        os.makedirs(self.pre_dir)
        os.makedirs(self.out_dir)

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
        DIRT.main(args)
        # TODO: test the outputs

    def test_b(self):
        args = mock.Mock()
        args.input = 'other_test_files/input_list.txt'
        args.preprocessed_dir = self.pre_dir
        args.output_dir = self.out_dir
        args.language = 'eng'
        args.comparator = 'simple'
        DIRT.main(args)
