import unittest
from src.ner_tagger import NERTagger


class TestNerTagging(unittest.TestCase):

    def test_ner_tagger(self):

        ner_tagger = NERTagger()

        data_1 = "London is the capital of Great Britain!"
        self.assertEqual(list(ner_tagger.get_labels([data_1])),
                         [('London', '381', 'GPE'), ('Great Britain', '381', 'GPE')])

        data_2 = "screw Jack, let's find a way out of Coruscant!"
        self.assertEqual(list(ner_tagger.get_labels([data_2])),
                         [('Jack', '377', 'PERSON'), ('Coruscant', '381', 'GPE')])

        data_3 = "Don't mess with him, Benjamin Foe, he's a great warior of New China."
        self.assertEqual(list(ner_tagger.get_labels([data_3])),
                         [('Benjamin Foe', '377', 'PERSON'), ('New China', '380', 'ORG')])


if __name__ == '__main__':
    unittest.main()
