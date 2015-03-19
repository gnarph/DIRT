"""
Module for standardizing Chinese text
"""
from cjklib import characterlookup
import mafan

from preprocessing.language_standardizer import base_standardizer


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
    """
    Iterator over characters in text, replacing them as needed
    Replaces punctuation, symbols, separators with spaces
    Reduces characters to their variant with the lowest code point
    :param text: input text
    :param sub: thing to substitute for unwanted characters
    :return: generator
    """

    # Lookup characters in chinese locale
    lookup = characterlookup.CharacterLookup(locale='C')

    for char in base_standardizer.remove_unwanted_gen(text, sub):
        if char == sub:
            yield char
        else:
            # see https://github.com/cburgmer/cjklib/blob/3faf249e1416ed5dca4d7b9a3341400bf64a9e50/cjklib/characterlookup.py
            # much faster - one db hit
            # includes (specialized)semantic variants, traditional/simplified variants
            # unicode compatibility variants, and Z variants
            # Empty list if character not found
            variants = lookup.getAllCharacterVariants(char)
            variants.append((char, 'M'))
            desired = min(v[0] for v in variants if v[1] in {'P', 'M'})

            yield desired
