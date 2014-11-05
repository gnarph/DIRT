#!/usr/bin/env python
#coding: utf-8

import string  
import re  

def remove(text):
    exclude = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in exclude)
    return text



if __name__=="__main__":
    asking= u"hello! &^*&^*(&what's yo1231薩達231ur 盛大阿什頓name? &&怎么阿什頓飛工商局等規劃这么的厉害!不再".encode('utf8')
    expect = remove(asking)
    print unicode(expect,'utf8').encode('utf8')

