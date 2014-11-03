import unittest

import mock

import DIRT


class SmokeTest(unittest.TestCase):

    def test_a(self):
        args = mock.Mock()
        args.input_dir = 'test_data'
        args.preprocessed_dir = 'test_preprocessed'
        args.output_dir = 'test_output'
        args.language = 'eng'
        args.comparator = 'simple'
        DIRT.main(args)
        # TODO: test the outputs
