""" space_tagger module

This module contains function to deal with space settings indentification of the raw text.
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org

from .utilities import remove_punctuation

def space_tagger(data, word_dict, default_dict):
    for location, location_type in word_dict.items():
        if location in data:
            default_dict[location_type] = 1

    return default_dict

def main():
    data = "He lives in China, Shenzen."
    kv_map = {"China": "Asia", "Shenzen": "Asia"}
    space_dict = {"Asia": 0, "Europe": 0, "America": 0}

    print(space_tagger(remove_punctuation(data), kv_map, space_dict))

if __name__ == '__main__':
    main()
