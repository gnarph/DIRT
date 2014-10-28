import codecs
from os import path

import cjson

from models.document import Document
import models.document_factory as document_factory
from preprocessing.language_standardizer import eng

PREPROCESS_SUFFIX = '_PRE.json'


class Preprocessor(object):
    """
    Preprocessor
    """
    def __init__(self, file_name, input_dir, output_dir, standardizer=eng):
        """
        :param file_name: name of file to be preprocessed
        :param input_dir: input directory
        :param output_dir: output directory
        :param standardizer: text standardizer
        :return:
        """
        self.standardizer = standardizer
        self.input_dir = input_dir
        self.file_name = file_name
        self.output_dir = output_dir

    def process(self):
        output_name = self.file_name + PREPROCESS_SUFFIX
        in_file = path.join(self.input_dir, self.file_name)
        out_file = path.join(self.output_dir, output_name)

        in_document = document_factory.from_file(in_file)
        processed = self.standardizer.standardize(in_document.body)
        out_document = Document(output_name, processed, in_document.metadata)
        processed_dict = out_document.to_dict()
        processed_json = cjson.encode(processed_dict)
        with codecs.open(out_file, mode='w+', encoding='UTF-8') as o:
            o.write(processed_json)
