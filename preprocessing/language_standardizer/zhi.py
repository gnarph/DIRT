"""
Module for standarizing Chinese text
"""

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
