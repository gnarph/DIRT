#!/usr/bin/env python
#coding: utf-8


def conv(string, dic):
    """
    Maximum Forward Match
    :param string:
    :param dic:
    :return:
    """
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


def mdic():
    """
    Translate words according to the dictionary
    :return: ?
    """
    with open('preprocessing/translation/ZhConversion.php', 'r') as f:
        table = f.readlines()
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

    # TODO: should have a param to indicate which dict to return
    # Simplified to Traditional(zh2Hant) Taiwanese Style(zh2TW)
    name[3].update(name[1])
    # Simplified to Traditional(zh2Hant) HongKong Style (zh2HK)
    #name[4].update(name[1])
    # Traditional to Simplified (zh2Hans) Chinese Style(zh2CN)
    #name[5].update(name[2])
    return name[3], name[4], name[5]
