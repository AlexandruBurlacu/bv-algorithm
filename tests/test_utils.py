import unittest
import src.utilities as utils

class TestUtilsModule(unittest.TestCase):

    def test_drop_none_match(self):
        pre_data = "Hello darkness my old friend".split()
        data = map(lambda x: (x, 0, 42, None), pre_data)
        self.assertEqual(list(utils.drop_none(data)),
                         [("Hello", 0, 42, None),
                          ("darkness", 0, 42, None),
                          ("my", 0, 42, None),
                          ("old", 0, 42, None),
                          ("friend", 0, 42, None)])

    def test_drop_none_no_match(self):
        pre_data = "Hello darkness my old friend".split()
        data = map(lambda x: None, pre_data)
        self.assertEqual(list(utils.drop_none(data)), [])


    def test_get_config(self):
        self.assertIsInstance(utils.get_config(), dict)
        self.assertNotEqual(utils.get_config().get("raw_text"), None)
        self.assertNotEqual(utils.get_config().get("sentiment_vocab"), None)
