import codecs
import os
import unittest

import cjson

import models.document as global_document
import preprocessing.tei.reader as reader
import preprocessing.tei.document as tei_document

TEI_ZHI = 'test_data/zhi_tei.xml'
TEI_ENG = 'test_data/eng_tei.xml'

JSON_ZHI = 'test_data/zhi_parsed.json'
JSON_ENG = 'test_data/eng_parsed.json'


class TEITest(unittest.TestCase):

    # TODO: move three methods to superclass
    #       they are copied from language prep test
    def _get_test_file_name(self, file_name):
        raw_loc = os.path.realpath(__file__)
        my_dir = os.path.dirname(raw_loc)
        real_file_name = os.path.join(my_dir, file_name)
        return real_file_name

    def _read_file(self, file_name):
        real_file_name = self._get_test_file_name(file_name)
        with codecs.open(real_file_name, encoding='utf-8') as f:
            raw_passage = f.read()
        return raw_passage

    def _read_json_file(self, file_name):
        raw = self._read_file(file_name)
        return cjson.decode(raw, all_unicode=True)

    def _test_get_data(self, data_file, parsed_json_file):
        """
        Check that an input file is correctly segmented
        :param data_file: utf8 chinese input file
        :param parsed_json_file: uft8 json file of correct segmentation
        """
        real_data_file = self._get_test_file_name(data_file)
        doc = tei_document.TEIDocument(real_data_file)
        output = doc.get_data()
        desired = self._read_json_file(parsed_json_file)
        self.assertEquals(output, desired)

    def test_get_data(self):
        self._test_get_data(TEI_ZHI, JSON_ZHI)
        self._test_get_data(TEI_ENG, JSON_ENG)

    def test_read(self):
        real_data_file = self._get_test_file_name(TEI_ZHI)
        tei_doc = tei_document.TEIDocument(real_data_file)
        tei_data = tei_doc.get_data()
        tei_body = tei_data['body']
        r = reader.TEIReader(real_data_file)
        read_doc = r.read()
        self.assertEqual(tei_body, read_doc.body)
        global_doc = global_document.Document.from_file(real_data_file)
        self.assertEqual(read_doc, global_doc)
