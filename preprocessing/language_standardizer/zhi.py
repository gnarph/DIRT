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
            # Only want Z-variants, as they indicate no change in
            # meaning
            variants = lookup.getCharacterVariants(char, 'Z')
            variants.append(char)
            yield min(variants)
