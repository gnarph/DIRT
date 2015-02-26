"""
Module for common standardization functions
"""
from unicodedata import category

# Unicode categories
PUNCTUATION_CATS = {'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'}
SYMBOL_CATS = {'Sc', 'Sk', 'Sm', 'So'}
SEPARATOR_CATS = {'Zi', 'Zp', 'Zs'}


def remove_unwanted_gen(text, sub=' '):
    """
    Iterator over characters in text, replacing them as needed
    Replaces punctuation, symbols, separators with spaces
    :param text: input text
    :param sub: thing to substitute for unwanted characters
    :return: generator
    """
    sub_cats = PUNCTUATION_CATS | SYMBOL_CATS | SEPARATOR_CATS

    for char in text:
        if category(char) in sub_cats:
            yield sub
        else:
            yield char