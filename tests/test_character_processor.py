import unittest
from src import CharacterProcessor

class TestCharacterIndentification(unittest.TestCase):

    def test_singular_word_occurance(self):
        self.assertEqual(CharacterProcessor() \
                            .run("Hey, did you know that Logan is a mutant?".split()),
                         {'mutants': 1})

    def test_plural_word_occurance(self):
        self.assertEqual(CharacterProcessor().run("Hey, did you know that Logan \
                                               is a mutant and Daenerys has 3 dragons?".split()),
                         {'dragons': 1, 'mutants': 1})
