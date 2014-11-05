#!/usr/bin/env python
#coding: utf-8

import codecs
import json
import unittest
import string  
import re

import punctuation_remove


class PunctuationRemoveTest(unittest.TestCase):

    def test_punctuationremove(self):
        expected_result = u'hello whats yo1231薩達231ur 盛大阿什頓name 怎么阿什頓飛工商局等規劃这么的厉害不再'.encode('utf8')
        testing= u"hello! &^*&^*(&whats yo1231薩達231ur 盛大阿什頓name? &&怎么阿什頓飛工商局等規劃这么的厉害!不再".encode('utf8')

        remove_result = punctuation_remove.remove(testing)
        self.assertEqual(remove_result,expected_result)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
