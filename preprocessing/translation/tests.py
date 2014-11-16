#!/usr/bin/env python
#coding: utf-8

import unittest

import preprocessing.translation.translation as translation


class TranslationTests(unittest.TestCase):

    def test_translation(self):
        simplified = u'来自Bandai Namco Games TW/HK 官方FACEBOOK情报' \
                     u'，PS3/PSV平台动漫改编作品《刀剑神域：失落之歌》繁' \
                     u'体中文版正式公开!预定于2015年发售，并一同公开了繁' \
                     u'体中文版宣传片，下面来欣赏了解一下。'
        traditional = u'來自Bandai Namco Games TW/HK 官方FACEBOOK情報，' \
                      u'PS3/PSV平台動漫改編作品《刀劍神域：失落之歌》繁' \
                      u'體中文版正式公開!預定於2015年發售，並一同公開了繁' \
                      u'體中文版宣傳片，下面來欣賞了解一下。'

        trans_simple = translation.simplify(traditional)
        self.assertEqual(trans_simple, simplified)

        trans_traditional = translation.tradify(simplified)
        print trans_traditional
        print traditional
        self.assertEqual(trans_traditional, traditional)
