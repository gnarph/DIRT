import codecs
import os

import cjson

import models.document_factory as document_factory
from processing.comparators import simple

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

    def document_from_input(self, file_name):
        """
        Get Document model from file
        :param file_name: file to read
        :return: document model representation of the file
        """
        real_name = os.path.join(self.input_dir, file_name)
        return document_factory.from_file(real_name)

    def process(self):
        """
        Process input files
        """
        alpha = self.document_from_input(self.alpha_name)
        beta = self.document_from_input(self.beta_name)
        comparator = self.comparator.Comparator(alpha.body,
                                                beta.body)
        out_name = REPORT_NAME.format(self.alpha_name,
                                      self.beta_name)
        matches = comparator.compare()
        match_dicts = [match.to_dict() for match in matches]
        json_match = cjson.encode(match_dicts)
        unicode_json_match = json_match.encode('utf8')
        out_file = os.path.join(self.output_dir, out_name)
        with codecs.open(out_file, 'w+', 'UTF-8') as o:
            o.write(unicode_json_match)
