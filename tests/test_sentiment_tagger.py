import unittest
from src import sentiment_tagger

class TestSentimentTaggerModule(unittest.TestCase):
    def test_sentiment_tagger_no_match(self):
        data = "Hello darkness my old friend".split()
        word_dict = {"man": {"category": "anger", "sentiment": -1}}

        self.assertEqual(sentiment_tagger(0, data[0], word_dict), None)
        self.assertEqual(sentiment_tagger(1, data[1], word_dict), None)
        self.assertEqual(sentiment_tagger(2, data[2], word_dict), None)
        self.assertEqual(sentiment_tagger(3, data[3], word_dict), None)
        self.assertEqual(sentiment_tagger(4, data[4], word_dict), None)

    def test_sentiment_tagger_match(self):
        data = "Hello darkness my old friend".split()
        word_dict = {"old": {"category": "age", "sentiment": -1}}

        self.assertEqual(sentiment_tagger(0, data[0], word_dict), None)
        self.assertEqual(sentiment_tagger(1, data[1], word_dict), None)
        self.assertEqual(sentiment_tagger(2, data[2], word_dict), None)
        self.assertEqual(sentiment_tagger(3, data[3], word_dict), (-1, "age", "old", 3))
        self.assertEqual(sentiment_tagger(4, data[4], word_dict), None)


if __name__ == '__main__':
    unittest.main()

