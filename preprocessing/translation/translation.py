#!/usr/bin/env python
#coding: utf-8

import io, json

# Maximum Forward Match
def conv(string,dic):
    i = 0
    while i < len(string):
        for j in range(len(string) - i, 0, -1):
            if string[i:][:j] in dic:
                t = dic[string[i:][:j]]
                string = string[:i] + t + string[i:][j:]
                i += len(t) - 1
                break
        i += 1
    return string
 
# Translating words according to the dictionary
def mdic():    
    table = open('ZhConversion.php','r').readlines()
    dic = dict()
    name = []
    for line in table:
        if line[0] == '$':
            #print line.split()[0][1:]
            name.append(dic)
            dic = dict()
        if line[0] == "'":
            word = line.split("'")
            dic[word[1]] = word[3]
    name[3].update(name[1]) # Simplified to Traditional(zh2Hant) Taiwanese Style(zh2TW)
    #name[4].update(name[1]) # Simplified to Traditional(zh2Hant) HongKong Style (zh2HK)
    #name[5].update(name[2]) # Traditional to Simplified (zh2Hans) Chinese Style(zh2CN)
    return name[3],name[4],name[5]
 
if __name__=="__main__":
    f = open('workfile.txt', 'r')
    temp = f.read()
    [dic_TW,dic_HK,dic_CN] = mdic()
    str_TW = conv(temp,dic_TW)
    #str_HK = conv(c,dic_HK)    Translate into Traditional Language(HongKong), another style of Traditional, not the best.
    #str_CN = conv(b,dic_CN)    Translate into Simplified from Traditional
    print unicode(temp,'utf8').encode('utf8'), ' <-> ', unicode(str_TW,'utf8').encode('utf8') # Print Simplified on left side and Traditional on right side

    
    
