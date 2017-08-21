""" space_tagger module

This module contains function to deal with space settings indentification of the raw text.
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org

import logging

from collections import Counter
from .utilities import remove_punctuation

def space_tagger(data, word_dict, default_dict):
    for location, location_type in word_dict.items():
        if " {} ".format(location) in data:
            default_dict[location_type.replace(" ", "")] += [location]

    summed_loc_occur = {k: dict(Counter(val)) for k, val in default_dict.items()}

    logging.error(summed_loc_occur)

    for k in summed_loc_occur.keys():
        cond = list(filter(lambda x: x > 1, summed_loc_occur[k].values()))
        if cond:
            default_dict[k] = 1
        else:
            default_dict[k] = 0

    return default_dict

def main():
    data = "He lives in China, Shenzen."
    kv_map = {"China": "Asia", "Shenzen": "Asia"}
    space_dict = {"Asia": [], "Europe": [], "America": []}

    print(space_tagger(remove_punctuation(data), kv_map, space_dict))

if __name__ == '__main__':
    main()
