import os
import time

from models.document import Document
from preprocessing.language_standardizer import eng
from preprocessing.tei.reader import TEIReader
from utilities import path
from utilities import file_ops
from utilities import logger

PREPROCESS_DIR = 'dirt_preprocess/'
PREPROCESS_SUFFIX = '.json'
PLAIN_SUFFIX = '.txt'


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

    @staticmethod
    def _log_duration(duration, file_name, length):
        template = 'Preprocessed {} of length {} in {} seconds ' \
                   '({} char per second)'
        message = template.format(file_name,
                                  length,
                                  duration,
                                  length/duration)
        logger.info(message)

    def process(self):
        """
        Perform processing
        Creates raw and preprocessed versions of the input file
        as well as a json file representing the models.Document
        """
        start_time = time.time()
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
                                'raw' + os.sep,
                                name + PLAIN_SUFFIX)
        file_ops.write_utf8(raw_file, raw_text)

        processed_text = self.standardizer.standardize(raw_text)
        pre_file = os.path.join(self.output_dir,
                                'pre' + os.sep,
                                name + PLAIN_SUFFIX)
        file_ops.write_utf8(pre_file, processed_text)

        out_document = Document(file_name=self.file_name,
                                raw_file_name=raw_file,
                                pre_file_name=pre_file,
                                metadata=metadata)
        processed_dict = out_document.to_dict()
        file_ops.write_json_utf8(out_file, processed_dict)

        duration = time.time() - start_time
        self._log_duration(duration, self.file_name, len(raw_text))

