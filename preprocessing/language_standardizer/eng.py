"""
English language standardizer
"""
from preprocessing.language_standardizer import base_standardizer


def standardize(text):
    """
    Standardize text based on the language
    :param text: english input text
    :return: text without spacing, symbols or punctuation
    """
    wanted = base_standardizer.remove_unwanted_gen(text)
    return u''.join(wanted)
