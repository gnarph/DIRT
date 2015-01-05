# -*- coding: utf-8 -*-
import os
import time

from models.document import Document
from models.match import Match
from models.match_set import MatchSet
from processing.comparators import simple
from utilities import path
from utilities import file_ops
from utilities import fuzzer
from utilities import logger

REPORT_NAME = '{}__{}__CMP.json'


class Processor(object):
    """
    Processor
    """
    def __init__(self, alpha_name, beta_name, input_dir,
                 output_dir, comparator=simple, gap_length=3,
                 match_length=10, percentage_match_length=None):
        """
        Create a new Processor
        :param alpha_name: name of first file to be compared
        :param beta_name: name of second file to be compared
        :param input_dir: directory of input files
        :param output_dir: directory of output files
        :param comparator: comparator module
        :param gap_length: length of gap to jump
        :param match_length: min match length
        :param percentage_match_length: min percentage match len
        """
        self.comparator = comparator
        self.alpha_name = alpha_name
        self.beta_name = beta_name
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.gap_length = gap_length
        self.match_length = match_length
        self.percentage_match_length = percentage_match_length

    @staticmethod
    def _get_match(a, alpha, b, beta):
        alpha_indices = a.get_match_bounds(alpha.pre_body)
        alpha_passage = a.passage
        beta_indices = b.get_match_bounds(beta.pre_body)
        beta_passage = b.passage
        m = Match(alpha_passage=alpha_passage,
                  alpha_indices=alpha_indices,
                  beta_passage=beta_passage,
                  beta_indices=beta_indices)
        return m

    @staticmethod
    def singlet_pairs_to_matches(alpha, beta, singlet_pairs):
        # TODO: should use pre_body
        matches = []
        for a, b in singlet_pairs:
            try:
                m = Processor._get_match(a, alpha, b, beta)
                matches.append(m)
            except fuzzer.FuzzerFailure:
                print 'err'
        return matches

    def _log_duration(self, duration):
        template = 'Processed {}, {} in {} seconds'
        message = template.format(self.alpha_name,
                                  self.beta_name,
                                  duration)
        logger.info(message)

    def process(self):
        """
        Process input files
        """
        start_time = time.time()
        alpha = Document.from_json(self.alpha_name)
        beta = Document.from_json(self.beta_name)
        comparator = self.comparator.Comparator(a=alpha.pre_body,
                                                b=beta.pre_body,
                                                name_a=self.alpha_name,
                                                name_b=self.beta_name,
                                                match_length=self.match_length,
                                                gap_length=self.gap_length)
        name_a = path.get_name(self.alpha_name, extension=False)
        name_b = path.get_name(self.beta_name, extension=False)
        out_name = REPORT_NAME.format(name_a,
                                      name_b)
        singlet_pairs = comparator.compare()
        matches = self.singlet_pairs_to_matches(alpha, beta, singlet_pairs)
        match_set = MatchSet(alpha_doc=alpha,
                             beta_doc=beta,
                             matches=matches)
        match_set_dict = match_set.to_dict()
        out_file = os.path.join(self.output_dir, out_name)
        file_ops.write_json_utf8(out_file, match_set_dict)

        duration = time.time() - start_time
        self._log_duration(duration)
