"""
Module for standardizing Chinese text
"""

from unicodedata import category

import mafan


def standardize(text):
    """
    Standardize a line of Chinese text
    :param text: unicode string of Chinese
    :return: standardize form of input line
    """
    stripped = strip(text)
    trad = make_traditional(stripped)
    return trad


def make_traditional(text):
    """
    Makes Chinese text Traditional Chinese
    :param text: unicode string of Chinese
    :return: unicode string of Traditional Chinese
    """
    if not mafan.is_traditional(text):
        trad = mafan.tradify(text)
    else:
        trad = text
    return trad


def is_traditional(text):
    """
    Checks if a unicode string is Traditional Chinese
    :param text: unicode string
    :return: boolean
    """
    return mafan.is_traditional(text)


def is_simplified(text):
    return mafan.is_simplified(text)


def strip(text):
    """
    Strip punctuation and symbols from text
    Thanks to http://stackoverflow.com/a/11066579/2701544
    :param text: input unicode string
    :return: unicode string without punctuation or symbols
    """
    gen = chunk_gen(text)
    return u''.join(gen)


def chunk_gen(text, sub=' '):
    punctuation_cats = {'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'}
    symbol_cats = {'Sc', 'Sk', 'Sm', 'So'}
    separator_cats = {'Zi', 'Zp', 'Zs'}
    sub_cats = punctuation_cats | symbol_cats | separator_cats

    for char in text:
        if category(char) in sub_cats:
            yield char
        else:
            yield sub
