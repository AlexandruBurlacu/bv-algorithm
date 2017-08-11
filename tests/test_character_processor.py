import unittest
from src import CharacterProcessor

class TestCharacterIndentification(unittest.TestCase):

    def test_singular_word_occurance(self):
        self.assertEqual(CharacterProcessor() \
                            .run("Hey, did you know that Logan is a mutant?".split()),
                         {'aliens': 0, 'dragons': 0, 'humanoiddroids': 0,
                         'mutants': 1, 'robots': 0, 'superintelligence': 0})

    def test_plural_word_occurance(self):
        self.assertEqual(CharacterProcessor().run("Hey, did you know that Logan \
                                               is a mutant and Daenerys has 3 dragons?".split()),
                        {'aliens': 0, 'dragons': 1, 'humanoiddroids': 0,
                         'mutants': 1, 'robots': 0, 'superintelligence': 0})
