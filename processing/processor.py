import codecs
import os

from models.document import Document
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
        return Document.from_file(real_name)

    def process(self):
        """
        Process input files
        """
        alpha = self.document_from_input(self.alpha_name)
        beta = self.document_from_input(self.beta_name)
        comparator = self.comparator.Comparator(alpha=alpha.body,
                                                beta=beta.body)
        out_name = REPORT_NAME.format(self.alpha_name,
                                      self.beta_name)
        compared = comparator.compare()
        str_compared = str(compared)
        uni_compared = str_compared.encode('utf8')
        out_file = os.path.join(self.output_dir, out_name)
        with codecs.open(out_file, 'w+', 'UTF-8') as o:
            o.write(uni_compared)
