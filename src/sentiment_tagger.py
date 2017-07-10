""" sentiment_tagger module

This module contains functions to deal with sentiment tagging of the raw text.
"""

# Author: Alexandru Varacuta
# Email:  alexandru-varacuta@bookvoyager.org

def sentiment_tagger(index, word, word_dict):
    """(int, str, dict<str, dict<str, str>>) -> tuple<int, str, str, int>"""
    condition = word_dict.get(word)
    if condition is None:
        return (None, None, word, index)
    return (condition["sentiment"], condition["category"], word, index)

