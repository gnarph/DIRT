#!/usr/bin/env python
"""
Main entrance point for DIRT
"""

import argparse
import os
import itertools
import importlib

import preprocessing.preprocessor as preprocessor
import processing.processor as processor

STANDARDIZER_PATH = 'preprocessing.language_standardizer.{}'
COMPARATOR_PATH = 'processing.comparators.{}'


class UnsupportedFunctionException(BaseException):
    pass


def iter_files_in(directory):
    for item_name in os.listdir(directory):
        # Should this use os.walk?
        if not os.path.isdir(item_name):
            yield item_name


def preprocess(args):
    standardizer_path = STANDARDIZER_PATH.format(args.language)
    standardizer = importlib.import_module(standardizer_path)
    for file_name in iter_files_in(args.input_dir):
        pre = preprocessor.Preprocessor(file_name=file_name,
                                        standardizer=standardizer,
                                        input_dir=args.input_dir,
                                        output_dir=args.preprocessed_dir)
        pre.process()


def process(args):
    comparator_path = COMPARATOR_PATH.format(args.comparator)
    comparator = importlib.import_module(comparator_path)

    alpha_iter = iter_files_in(args.preprocessed_dir)
    beta_iter = iter_files_in(args.preprocessed_dir)
    compared = set()
    for a, b in itertools.product(alpha_iter, beta_iter):
        this_set = {a, b}
        if a != b and this_set not in compared:
            compared = set.union(compared, this_set)
            pro = processor.Processor(a, b, args.preprocessed_dir, args.output_dir,
                                      comparator=comparator)
            pro.process()


def postprocess(args):
    for file_name in iter_files_in(args.output_dir):
        print file_name
        # TODO: actually postprocess


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='DIRT.py',
                                     description='Find reused text in a corpus of text')

    # TODO: add parameters to allow only pre/processing/postprocessing
    parser.add_argument('-i', '--input_dir',
                        help='Directory containing input corpus')
    parser.add_argument('-pre', '--preprocessed_dir',
                        default='dirt_preprocessed',
                        help='Directory containing preprocessed corpus')
    parser.add_argument('-o', '--output_dir',
                        default='dirt_output',
                        help='Directory for output files')

    parser.add_argument('-l', '--language',
                        default='eng',
                        help='ISO 639-2 language code')
    parser.add_argument('-c', '--comparator',
                        default='simple',
                        help='comparator for processor')

    parsed_args = parser.parse_args()
    preprocess(parsed_args)
    process(parsed_args)
    postprocess(parsed_args)
