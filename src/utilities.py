"""utils module

This module provides utility functions.
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org

import json
import os
import re, string

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
    return regex.sub("", data)