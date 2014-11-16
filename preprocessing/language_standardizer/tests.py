import unittest

import preprocessing.language_standardizer.zhi as zhi
import utilities.file_ops as file_reading


NEWS_DATA_FILE = 'test_data/zhi_news.txt'
NEWS_2_DATA_FILE = 'test_data/zhi_news_2.txt'
NEWS_TRAD_DATA_FILE = 'test_data/zhi_news_trad.txt'

NEWS_SEG_FILE = 'test_data/zhi_news_segmented.json'
NEWS_2_SEG_FILE = 'test_data/zhi_news_2_segmented.json'
NEWS_TRAD_SEG_FILE = 'test_data/zhi_news_trad_segmented.json'

NEWS_STD_FILE = 'test_data/zhi_news_std.json'
NEWS_2_STD_FILE = 'test_data/zhi_news_2_std.json'
NEWS_TRAD_STD_FILE = 'test_data/zhi_news_trad_std.json'


class ZhiTest(unittest.TestCase):

    def _read_file(self, file_name):
        full_name = file_reading.get_full_file_name(file_name, __file__)
        return file_reading.read_utf8(full_name)

    def _read_json_file(self, file_name):
        full_name = file_reading.get_full_file_name(file_name, __file__)
        return file_reading.read_json_utf8(full_name)

    def _check_data_vs_segmented(self, data_file, seg_file):
        """
        Check that an input file is correctly segmented
        :param data_file: utf8 chinese input file
        :param seg_file: uft8 json file of correct segmentation
        """
        news_passage = self._read_file(data_file)
        output_generator = zhi.segment_words(news_passage)
        news_output = list(output_generator)
        news_desired = self._read_json_file(seg_file)
        self.assertEquals(news_output, news_desired)

    def test_word_segmentation(self):
        """
        Test that a chinese passage is correctly segmented into words

        NOTE: This is based on what jieba.cut does as of 2014-10-21
        """
        self._check_data_vs_segmented(NEWS_DATA_FILE, NEWS_SEG_FILE)
        self._check_data_vs_segmented(NEWS_2_DATA_FILE, NEWS_2_SEG_FILE)
        self._check_data_vs_segmented(NEWS_TRAD_DATA_FILE, NEWS_TRAD_SEG_FILE)

    def _check_data_vs_std(self, data_file, std_file):
        """
        Check that an input file is correctly standardized
        :param data_file: utf8 chinese input file
        :param std_file: uft8 json file of correct standardization
        """
        news_passage = self._read_file(data_file)
        news_output = zhi.standardize(news_passage)
        news_desired = self._read_json_file(std_file)

        self.assertEquals(news_output, news_desired)

    def test_standardization(self):
        """
        Test standardization
        NOTE: Currently just segments, does nothing else
        """
        self._check_data_vs_std(NEWS_DATA_FILE, NEWS_STD_FILE)
        self._check_data_vs_std(NEWS_2_DATA_FILE, NEWS_2_STD_FILE)
        self._check_data_vs_std(NEWS_TRAD_DATA_FILE, NEWS_TRAD_STD_FILE)
