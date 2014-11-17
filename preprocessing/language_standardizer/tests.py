# -*- coding: utf-8 -*-
import unittest

from preprocessing.language_standardizer import zhi
from utilities import file_ops


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
        full_name = file_ops.get_full_file_name(file_name, __file__)
        return file_ops.read_utf8(full_name)

    def _read_json_file(self, file_name):
        full_name = file_ops.get_full_file_name(file_name, __file__)
        return file_ops.read_json_utf8(full_name)

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

    def test_translate(self):
        simplified = u'来自Bandai Namco Games TW/HK 官方FACEBOOK情报' \
                     u'，PS3/PSV平台动漫改编作品《刀剑神域：失落之歌》繁' \
                     u'体中文版正式公开!预定于2015年发售，并一同公开了繁' \
                     u'体中文版宣传片，下面来欣赏了解一下。'
        traditional = u'來自Bandai Namco Games TW/HK 官方FACEBOOK情報' \
                      u'，PS3/PSV平臺動漫改編作品《刀劍神域：失落之歌》繁' \
                      u'體中文版正式公開!預定於2015年發售，並一同公開了繁' \
                      u'體中文版宣傳片，下面來欣賞了解一下。'

        simp_is_simp = zhi.is_simplified(simplified)
        self.assertTrue(simp_is_simp)
        trad_is_trad = zhi.is_traditional(traditional)
        self.assertTrue(trad_is_trad)

        trans_traditional = zhi.make_traditional(simplified)
        self.assertEqual(trans_traditional, traditional)

    def test_strip(self):
        expected_result = u'hellowhatsyo1231薩達231ur盛大阿什頓name'
        testing = u"hel，lo! &^*&^*(&what：s 《yo1231薩達231。ur 盛大阿什頓name? &"

        remove_result = zhi.strip(testing)
        self.assertEqual(remove_result, expected_result)
