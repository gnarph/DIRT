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
        expected_result = u'hel lo          what s  yo1231薩達231 ur 盛大啊什頓name   '
        testing = u"hel，lo! &^*&^*(&what：s 《yo1231薩達231。ur 盛大阿什頓name? &"

        remove_result = zhi.strip(testing)
        self.assertEqual(remove_result, expected_result)

    def test_unicode_sub(self):
        """
        Test unicode (specialized) semantic variant substitution
        """
        # TODO: test more characters with variants, semantic and otherwise
        text = u'處部止薩達'
        desired = u'䖏部止薩達'

        actual_gen = zhi.chunk_gen(text)
        actual = u''.join(actual_gen)
        self.assertEqual(actual, desired)

        # Roundtrip should be the same
        actual_roundtrip_gen = zhi.chunk_gen(actual)
        actual_roundtrip = u''.join(actual_roundtrip_gen)
        self.assertEqual(actual_roundtrip, actual)

        # Now try the other way
        also_desired_gen = zhi.chunk_gen(desired)
        also_desired = u''.join(also_desired_gen)
        self.assertEqual(also_desired, desired)
