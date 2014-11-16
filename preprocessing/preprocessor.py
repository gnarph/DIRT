import codecs
import os

import cjson

from models.document import Document
from preprocessing.language_standardizer import eng
from preprocessing.tei.reader import TEIReader
from utilities import path
from utilities import file_ops

PREPROCESS_DIR = 'dirt_preprocess/'
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
        name = path.get_name(self.file_name, extension=False)
        output_name = name + PREPROCESS_SUFFIX
        in_file = self.file_name
        out_file = os.path.join(self.output_dir, output_name)

        if in_file.endswith('.tei') or in_file.endswith('.xml'):
            reader = TEIReader(in_file)
            raw_text, metadata = reader.read()
        else:
            raw_text = file_ops.read_utf8(in_file)
            metadata = {}

        raw_file = os.path.join(self.output_dir,
                                'raw/',
                                name)
        file_ops.write_string(raw_file, raw_text)

        processed_text = self.standardizer.standardize(raw_text)
        pre_file = os.path.join(self.output_dir,
                                'pre/',
                                name)
        file_ops.write_string(pre_file, processed_text)

        out_document = Document(file_name=self.file_name,
                                raw_file_name=raw_file,
                                pre_file_name=pre_file,
                                metadata=metadata)
        processed_dict = out_document.to_dict()
        processed_json = cjson.encode(processed_dict)
        with codecs.open(out_file, mode='w+', encoding='utf8') as o:
            o.write(processed_json)