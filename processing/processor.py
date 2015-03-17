# -*- coding: utf-8 -*-
import os
import time

from models.match import Match
from models.match_set import MatchSet
from processing.comparators import simple
from utilities import path
from utilities import file_ops
from utilities import logger

REPORT_NAME = u'{}__{}__CMP.json'


class Processor(object):
    """
    Processor
    """
    def __init__(self, output_dir, comparator=simple, gap_length=3,
                 match_length=10, percentage_match_length=None):
        """
        Create a new Processor
        :param output_dir: directory of output files
        :param comparator: comparator module
        :param gap_length: length of gap to jump
        :param match_length: min match length
        :param percentage_match_length: min percentage match len
        """
        self.comparator = comparator
        self.output_dir = output_dir
        self.gap_length = gap_length
        self.match_length = match_length
        self.percentage_match_length = percentage_match_length

    @staticmethod
    def _get_match(a, alpha, b, beta):
        """
        Get a single Match from Singlets
        :param a: alpha MatchSinglet
        :param alpha: alpha Document
        :param b: beta MatchSinglet
        :param beta: beta Document
        :return: Match
        """
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
        """
        Change singlet pairs into matches
        :param alpha: document
        :param beta: document
        :param singlet_pairs: list of MatchSinglet pairs
        """
        matches = []
        for a, b in singlet_pairs:
            m = Processor._get_match(a, alpha, b, beta)
            matches.append(m)
        return matches

    @staticmethod
    def _log_duration(alpha_name, beta_name, duration):
        template = u'Processed {}, {} in {} seconds'
        message = template.format(alpha_name,
                                  beta_name,
                                  duration)
        logger.info(message)

    @staticmethod
    def _get_report_name(alpha_document, beta_document):
        """
        Get the name of the report file
        """
        name_a = path.get_name(alpha_document.file_name, extension=False)
        name_b = path.get_name(beta_document.file_name, extension=False)
        out_name = REPORT_NAME.format(name_a,
                                      name_b)
        return out_name

    def _get_matches(self, alpha_document, beta_document):
        """
        Get Matches between two documents
        :param alpha_document: Document
        :param beta_document: Document
        :return: Matches
        """
        comparator = self.comparator.Comparator(a=alpha_document.pre_body,
                                                b=beta_document.pre_body,
                                                name_a=alpha_document.file_name,
                                                name_b=beta_document.file_name,
                                                match_length=self.match_length,
                                                gap_length=self.gap_length)
        singlet_pairs = comparator.compare()
        matches = self.singlet_pairs_to_matches(alpha=alpha_document,
                                                beta=beta_document,
                                                singlet_pairs=singlet_pairs)
        return matches

    def _process(self, alpha_document, beta_document):
        """
        Do processing itself
        :param alpha_document: Document one to compare
        :param beta_document: Document two to compare
        """
        out_name = self._get_report_name(alpha_document, beta_document)
        out_file = os.path.join(self.output_dir, out_name)
        if file_ops.exists(out_file):
            # Already processed
            return
        matches = self._get_matches(alpha_document, beta_document)
        match_set = MatchSet(alpha_doc=alpha_document,
                             beta_doc=beta_document,
                             matches=matches)
        match_set_dict = match_set.to_dict()
        file_ops.write_json_utf8(out_file, match_set_dict)

    def process(self, alpha_document, beta_document):
        """
        Process input files
        """
        start_time = time.time()
        self._process(alpha_document, beta_document)

        duration = time.time() - start_time
        self._log_duration(alpha_name=alpha_document.file_name,
                           beta_name=beta_document.file_name,
                           duration=duration)
