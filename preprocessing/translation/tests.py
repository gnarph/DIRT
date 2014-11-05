#!/usr/bin/env python
#coding: utf-8

import codecs
import json
import unittest

import translation


class TranslationTests(unittest.TestCase):
    
    def test_translation(self):
        simplified = u'来自Bandai Namco Games TW/HK 官方FACEBOOK情报，PS3/PSV平台动漫改编作品《刀剑神域：失落之歌》繁体中文版正式公开!预定于2015年发售，并一同公开了繁体中文版宣传片，下面来欣赏了解一下。'.encode('utf8')
        traditional = u'來自Bandai Namco Games TW/HK 官方FACEBOOK情報，PS3/PSV平台動漫改編作品《刀劍神域：失落之歌》繁體中文版正式公開!預定於2015年發售，並一同公開了繁體中文版宣傳片，下面來欣賞了解一下。'.encode('utf8')

        #translation_dicts = translation.mdic()
        [dic_TW,dic_HK,dic_CN] = translation.mdic()
        translated = translation.conv(simplified, dic_TW)
        self.assertEqual(translated, traditional)   
        


def main():
    unittest.main()

if __name__ == '__main__':
    main()
