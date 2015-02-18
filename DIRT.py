#!/usr/bin/env python
"""
Main entrance point for DIRT
"""

import argparse
import os
import itertools
import importlib
from multiprocessing import Pool
import time

from models.document import Document
import preprocessing.preprocessor as preprocessor
import processing.processor as processor
from utilities import path
from utilities import logger

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
    """
    Run processing step
    """
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


def process_parallel_worker(a, output_dir, gap_length, match_length,
                            percentage_match_length, b, comparator):
    """
    Worker for processing two files at a time in parallel
    """
    comparator_path = COMPARATOR_PATH.format(comparator)
    comparator = importlib.import_module(comparator_path)
    pro = processor.Processor(output_dir=output_dir,
                              comparator=comparator,
                              gap_length=gap_length,
                              match_length=match_length,
                              percentage_match_length=percentage_match_length)
    alpha = Document.from_json(a)
    beta = Document.from_json(b)
    pro.process(alpha_document=alpha, beta_document=beta)


def process_parallel(args, alpha_files, beta_files):
    """
    Process on multiple threads/processes
    """
    p = Pool()
    compared = []
    for a, b in itertools.product(alpha_files, beta_files):
        this_set = sorted([a, b])
        if a != b and this_set not in compared:
            p.apply_async(process_parallel_worker, (a,
                                                    args.output_dir,
                                                    args.gap_length,
                                                    args.match_length,
                                                    args.percentage_match_length,
                                                    b,
                                                    args.comparator))
            compared.append(this_set)
    p.close()
    p.join()
    return len(compared)


def process_serial(args, alpha_files, beta_files):
    """
    Process on a single thread
    """
    comparator_path = COMPARATOR_PATH.format(args.comparator)
    comparator = importlib.import_module(comparator_path)
    pro = processor.Processor(output_dir=args.output_dir,
                              comparator=comparator,
                              gap_length=args.gap_length,
                              match_length=args.match_length,
                              percentage_match_length=args.percentage_match_length)
    compared = []
    for a, b in itertools.product(alpha_files, beta_files):
        this_set = sorted([a, b])
        if a != b and this_set not in compared:
            alpha = Document.from_json(a)
            beta = Document.from_json(b)
            pro.process(alpha_document=alpha, beta_document=beta)
    return len(compared)


def process(args):
    """
    Run processing step
    """
    start = time.time()
    alpha_files = path.iter_files_in(args.preprocessed_dir)
    beta_files = path.iter_files_in(args.preprocessed_dir)
    if args.parallel:
        cnt = process_parallel(args, alpha_files, beta_files)
    else:
        cnt = process_serial(args, alpha_files, beta_files)

    duration = time.time() - start
    comparisons_per_sec = cnt/duration
    logger.info('Processed {} files per second'.format(comparisons_per_sec))


def main(parsed_args):
    preprocess(parsed_args)
    process(parsed_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='DIRT.py',
                                     description='Find reused text in a corpus of text')

    # TODO: add parameters to allow only pre/processing
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
    parser.add_argument('-p', '--parallel',
                        help='Run on multiple threads/processes',
                        action='store_const',
                        const=True)

    parsed = parser.parse_args()
    if parsed.verbose:
        logger.show_info()

    if parsed.input:
        main(parsed)
    if parsed.gui:
        from dirtgui import main_window
        if parsed.input:
            main_window.main(parsed.output_dir)
        else:
            main_window.main(None)
