"""
Module for standarizing Chinese text
"""

from unicodedata import category

import mafan


BLACKLIST = [u' ',
             u'\n']


def standardize(text):
    """
    Standardize a line of Chinese text
    :param text: unicode string of Chinese
    :return: standardize form of input line
    """
    trad = make_traditional(text)
    # Remove punctuation?
    return trad


def make_traditional(text):
    if not mafan.is_traditional(text):
        trad = mafan.tradify(text)
    else:
        trad = text
    return trad


def is_trad(text):
    return mafan.is_traditional(text)


def is_simp(text):
    return mafan.is_simplified(text)


def strip(text):
    """
    Strip punctuation and symbols from text
    Thanks to http://stackoverflow.com/a/11066579/2701544
    :param text: input unicode string
    :return: unicode string without punctuation or symbols
    """
    punctuation_cats = {'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'}
    symbol_cats = {'Sc', 'Sk', 'Sm', 'So'}
    remove_cats = punctuation_cats.union(symbol_cats)
    print remove_cats
    gen = (x for x in text
           if category(x) not in remove_cats)
    return u''.join(gen)

