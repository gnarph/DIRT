import os

from models.document import Document
from models.match import Match
from models.match_set import MatchSet
from processing.comparators import simple
from utilities import path
from utilities import file_ops

REPORT_NAME = '{}__{}__CMP.json'


class Processor(object):
    """
    Processor
    """
    def __init__(self, alpha_name, beta_name, input_dir, output_dir, comparator=simple):
        """
        Create a new Processor
        :param alpha_name: name of first file to be compared
        :param beta_name: name of second file to be compared
        :param input_dir: directory of input files
        :param output_dir: directory of output files
        :param comparator: comparator module
        """
        self.comparator = comparator
        self.alpha_name = alpha_name
        self.beta_name = beta_name
        self.input_dir = input_dir
        self.output_dir = output_dir

    @staticmethod
    def singlet_pairs_to_matches(alpha, beta, singlet_pairs):
        # TODO: should use pre_body
        matches = []
        for a, b in singlet_pairs:
            alpha_indices = a.get_match_bounds(alpha.raw_body)
            alpha_passage = a.passage
            beta_indices = b.get_match_bounds(beta.raw_body)
            beta_passage = b.passage
            m = Match(alpha_passage=alpha_passage,
                      alpha_indices=alpha_indices,
                      beta_passage=beta_passage,
                      beta_indices=beta_indices)
            matches.append(m)
        return matches

    def process(self):
        """
        Process input files
        """
        alpha = Document.from_json(self.alpha_name)
        beta = Document.from_json(self.beta_name)
        comparator = self.comparator.Comparator(a=alpha.pre_body,
                                                b=beta.pre_body,
                                                name_a=self.alpha_name,
                                                name_b=self.beta_name)
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
