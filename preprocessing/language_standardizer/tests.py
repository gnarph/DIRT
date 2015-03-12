# -*- coding: utf-8 -*-
from itertools import izip
import unittest

from preprocessing.language_standardizer import zhi


class ZhiTest(unittest.TestCase):

    def test_translate(self):
        """
        Test simplified to tradiational translation
        """
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
        """
        Test replacement of unwanted characters
        """
        expected_result = u'hel lo          what s  yo1231薩達231 ur 盛大阿什頓name   '
        testing = u"hel，lo! &^*&^*(&what：s 《yo1231薩達231。ur 盛大阿什頓name? &"

        remove_result = zhi.strip(testing)
        self.assertEqual(remove_result, expected_result)

    @unittest.skip
    def test_unicode_sub(self):
        """
        Test unicode (specialized) semantic variant substitution
        """
        # TODO: test more characters with variants
        # these are z variants, not semantic variants
        text = u'處部止'
        desired = u'処卩只'

        actual = zhi.chunk_gen(text)
        for actual_char, desired_char in izip(actual, desired):
            self.assertEqual(actual_char, desired_char)

        # Now try the other way
        also_desired = zhi.chunk_gen(desired)
        for ad_char, desired_char in izip(also_desired, desired):
            self.assertEqual(ad_char, desired_char)