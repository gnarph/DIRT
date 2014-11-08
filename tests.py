import os
import unittest
import shutil

import mock

import DIRT


class SmokeTest(unittest.TestCase):

    pre_dir = 'test_preprocessed'
    out_dir = 'test_output'

    def setUp(self):
        shutil.rmtree(self.pre_dir)
        shutil.rmtree(self.out_dir)
        os.makedirs(self.pre_dir)
        os.makedirs(self.out_dir)

    def tearDown(self):
        pass


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
