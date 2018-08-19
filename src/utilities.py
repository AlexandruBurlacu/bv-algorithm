"""utils module

This module provides utility functions.
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org

import json
import os
import re
import string

PATH = os.path.abspath(os.path.dirname(__file__))

def drop_none(word_iter):
    """Drops `None` values from an iterable"""
    return filter(lambda x: x != None, word_iter)

def get_config(config_file_path=os.path.join(PATH, "../config.json")):
    """Loads configuration file into the local module"""
    with open(config_file_path) as config_ptr:
        return json.load(config_ptr)

def remove_punctuation(data):
    regex = re.compile("[{}]".format(re.escape(string.punctuation)))
    return regex.sub(" ", data)

def merge_dicts(dict_a, dict_b):
    for k in dict_a.keys():
        if dict_a[k] == 1:
            dict_b[k] = 1

    return dict_b
