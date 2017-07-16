""" space_tagger module

This module contains function to deal with space settings indentification of the raw text.
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org


def space_tagger(tok, word_dict):
    """(str, dict<str, str>) -> tuple<str, str>"""
    condition = word_dict.get(tok)
    if not condition is None:
        return (condition, tok)

