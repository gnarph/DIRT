#!/usr/bin/env python
"""
Main entrance point for DIRT
"""

import argparse
import os
import itertools
import importlib

from models.document import Document
import preprocessing.preprocessor as preprocessor
import processing.processor as processor
from utilities import path

STANDARDIZER_PATH = 'preprocessing.language_standardizer.{}'
COMPARATOR_PATH = 'processing.comparators.{}'


class UnsupportedFunctionException(BaseException):
    pass


def iter_files_in_file(filename):
    with open(filename) as f:
        contents = f.read()
        lines = contents.split('\n')
    for line in lines:
        if line and path.should_use_file(line):
            yield line


def preprocess(args):
    standardizer_path = STANDARDIZER_PATH.format(args.language)
    standardizer = importlib.import_module(standardizer_path)
    if os.path.isdir(args.input):
        it = path.iter_files_in(args.input)
    else:
        it = iter_files_in_file(args.input)
    for file_name in it:
        pre = preprocessor.Preprocessor(file_name=file_name,
                                        standardizer=standardizer,
                                        input_dir=args.input,
                                        output_dir=args.preprocessed_dir)
        pre.process()


def process(args):
    comparator_path = COMPARATOR_PATH.format(args.comparator)
    comparator = importlib.import_module(comparator_path)

    alpha_iter = path.iter_files_in(args.preprocessed_dir)
    beta_iter = path.iter_files_in(args.preprocessed_dir)
    pro = processor.Processor(output_dir=args.output_dir,
                              comparator=comparator,
                              gap_length=args.gap_length,
                              match_length=args.match_length,
                              percentage_match_length=args.percentage_match_length)
    compared = []
    for a, b in itertools.product(alpha_iter, beta_iter):
        this_set = sorted([a, b])
        if a != b and this_set not in compared:
            compared.append(this_set)
            alpha = Document.from_json(a)
            beta = Document.from_json(b)
            pro.process(alpha_document=alpha, beta_document=beta)


def postprocess(args):
    for file_name in path.iter_files_in(args.output_dir):
        print file_name
        # TODO: actually postprocess


def main(parsed_args):
    preprocess(parsed_args)
    process(parsed_args)
    postprocess(parsed_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='DIRT.py',
                                     description='Find reused text in a corpus of text')

    # TODO: add parameters to allow only pre/processing/postprocessing
    parser.add_argument('-i', '--input',
                        help='Directory containing input corpus',
                        # required=True,
                        type=str)
    parser.add_argument('-pre', '--preprocessed_dir',
                        default='dirt_preprocessed',
                        help='Directory containing preprocessed corpus',
                        type=str)
    parser.add_argument('-o', '--output_dir',
                        default='dirt_output',
                        help='Directory for output files',
                        type=str)

    parser.add_argument('-l', '--language',
                        default='eng',
                        help='ISO 639-2 language code',
                        type=str)
    parser.add_argument('-c', '--comparator',
                        default='simple',
                        help='comparator for processor',
                        type=str)

    parser.add_argument('-gl', '--gap_length',
                        default=3,
                        help='Size of gaps between matches to be jumped',
                        type=int)
    parser.add_argument('-ml', '--match_length',
                        default=10,
                        help='Minimum length of a match',
                        type=int)
    parser.add_argument('-pml', '--percentage_match_length',
                        default=0,
                        help='Minimum length of match as a percentage of total'
                             'document length',
                        type=int)

    parser.add_argument('-v', '--verbose',
                        help='Verbose',
                        action='count')
    parser.add_argument('-gui',
                        help='Run Gui',
                        action='store_const',
                        const=True)

    parsed = parser.parse_args()
    if parsed.verbose:
        from utilities import logger
        logger.show_info()

    if parsed.input:
        main(parsed)
    if parsed.gui:
        from dirtgui import main_window
        main_window.main()
        # TODO: open just-processed matchset
