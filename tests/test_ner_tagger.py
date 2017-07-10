import unittest
from src.ner_tagger_client import NERTagger


class TestNerTagging(unittest.TestCase):

    def test_ner_tagger(self):
        """[WARNING] Keep in mind that in order for this test to pass,
        the `ner_tagger_server` should run."""

        msg = "Maybe you should launch the `ner_tagger_server` first"

        ner_tagger = NERTagger()

        data_1 = "London is the capital of Great Britain!"
        self.assertEqual(ner_tagger.get_labels([data_1]),
                         [['London', '381', 'GPE'], ['Great Britain', '381', 'GPE']], msg=msg)

        data_2 = "screw Jack, let's find a way out of Coruscant!"
        self.assertEqual(ner_tagger.get_labels([data_2]),
                         [['Jack', '377', 'PERSON'], ['Coruscant', '381', 'GPE']])

        data_3 = "Don't mess with him, Benjamin Foe, he's a great warior of New China."
        self.assertEqual(ner_tagger.get_labels([data_3]),
                         [['Benjamin Foe', '377', 'PERSON'], ['New China', '380', 'ORG']])


if __name__ == '__main__':
    unittest.main()
