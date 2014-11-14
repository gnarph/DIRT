import unittest

import preprocessing.tei.reader as reader
import preprocessing.tei.document as tei_document
from utilities import file_ops
from models.document import Document

TEI_ZHI = 'test_data/zhi_tei.xml'
TEI_ENG = 'test_data/eng_tei.xml'

JSON_ZHI = 'test_data/zhi_parsed.json'
JSON_ENG = 'test_data/eng_parsed.json'

RAW_ZHI = 'test_data/raw/zhi_tei.txt'
RAW_ENG = 'test_data/raw/eng_tei.txt'


class TEITest(unittest.TestCase):

    def _get_test_file_name(self, file_name):
        return file_ops.get_full_file_name(file_name, __file__)

    def _read_json_file(self, file_name):
        full_name = self._get_test_file_name(file_name)
        return file_ops.read_json_utf8(full_name)

    def _read_file(self, file_name):
        full_name = self._get_test_file_name(file_name)
        return file_ops.read_utf8(full_name)

    def _test_get_data(self, data_file, parsed_json_file, raw_file):
        """
        Check that an input file is correctly segmented
        :param data_file: utf8 chinese input file
        :param parsed_json_file: uft8 json file of correct segmentation
        """
        real_data_file = self._get_test_file_name(data_file)
        doc = tei_document.TEIDocument(real_data_file)
        output = doc.get_data()
        desired = self._read_json_file(parsed_json_file)
        metadata = desired['metadata']
        self.assertEquals(output['title'], metadata['title'])
        body = self._read_file(raw_file)
        esc = body.decode('string_escape')
        file_ops.write_string('preprocessing/gordgord.txt', output['body'])
        self.assertEqual(output['body'], body)

    def test_get_data(self):
        self._test_get_data(TEI_ZHI, JSON_ZHI, RAW_ZHI)
        self._test_get_data(TEI_ENG, JSON_ENG, RAW_ENG)

    def test_read(self):
        real_data_file = self._get_test_file_name(TEI_ZHI)
        tei_doc = tei_document.TEIDocument(real_data_file)
        tei_data = tei_doc.get_data()
        tei_body = tei_data['body']
        r = reader.TEIReader(real_data_file)
        read_doc = r.read()
        self.assertEqual(tei_body, read_doc[0])
        global_doc = Document.from_json(real_data_file)
        self.assertEqual(read_doc, global_doc)
