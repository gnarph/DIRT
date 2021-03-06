import os
import unittest

from models.document import Document
from preprocessing.preprocessor import Preprocessor
import utilities.path


class PreprocessorTest(unittest.TestCase):

    file_name = 'test_data/lorem.txt'
    input_dir = 'test_data'
    output_dir = 'test_preprocessed'

    def test_smoke(self):
        """
        Smoke test - check that the preprocessor runs without exploding
        """
        pp = Preprocessor(file_name=self.file_name,
                          input_dir=self.input_dir,
                          output_dir=self.output_dir)
        pp.process()
        out_dir_files = os.listdir(self.output_dir)
        for file_name in out_dir_files:
            name = utilities.path.get_name(self.file_name,
                                           extension=False)
            if name in file_name:
                file_path = os.path.join(self.output_dir, file_name)
                doc = Document.from_json(file_path)
                self.assertNotEqual(doc.pre_file_name, self.file_name)
                self.assertEqual(doc.file_name, 'test_preprocessed/lorem.json')
