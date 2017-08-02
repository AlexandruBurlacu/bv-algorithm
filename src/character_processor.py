"""character_processor module

Module contains methods to indentify 5 main types of Sci-fi characters:
- Aliens
- Mutants
- Androids
- Robots
- Dragons
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org

from collections import defaultdict
from .utilities import drop_none


class CharacterProcessor:
    """given a stream of raw text,
    checks if specific type of characters are present in in"""

    def __init__(self):
        self.default_dict = {
            "aliens": 0,
            "mutants": 0,
            "robots": 0,
            "humanoiddroids": 0,
            "dragons": 0,
            "superintelligence": 0
        }

    def _check_typeof_character(self, tok):
        if "alien" in tok:
            return {"aliens": 1}
        if "robot" in tok:
            return {"robots": 1}
        if "droid" in tok:
            return {"humanoiddroids": 1}
        if "dragon" in tok:
            return {"dragons": 1}
        if "mutant" in tok:
            return {"mutants": 1}
        if "superintelligence" in tok:
            return {"superintelligence": 1}
        else:
            return None

    def _func(self, key_vals):
        """Merges and sums an iterable of dictionaries"""
        ret = defaultdict(int)
        for key_val in key_vals:
            for key, val in key_val.items():
                # ret[key] += val
                ret[key] = 1
        return dict(ret)

    def run(self, text_stream):
        """Runs the search for character types"""
        self.default_dict.update(self._func(drop_none(self._check_typeof_character(tok)
                                                      for tok in text_stream)))
        return self.default_dict # fuckin' in-place methods
