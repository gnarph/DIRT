"""
English language standardizer
"""
from preprocessing.language_standardizer.zhi import strip


def standardize(text):
    return strip(text)
