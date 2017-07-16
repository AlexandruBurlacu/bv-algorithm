import unittest
from src import space_tagger

class TestSpaceTagger(unittest.TestCase):

    def test_space_tagger_match(self):
        space_dict = {
            "Terra Obscura": "earth",
            "Vulcan": "other planets",
            "Counter-Earth": "other planets",
            "Phaëton": "other planets",
            "Earth": "earth"
            }
        ts = "Earth and Vulcan are very related planets"
        self.assertEqual([space_tagger(t, space_dict) for t in ts.split()],
                         [("earth", "Earth"), None, ("other planets", "Vulcan"),
                          None, None, None, None])

    def test_space_tagger_no_match(self):
        space_dict = {
            "Terra Obscura": "earth",
            "Vulcan": "other planets",
            "Counter-Earth": "other planets",
            "Phaëton": "other planets",
            "Earth": "earth"
            }
        ts = "Joe and Valerian are such an assholes"
        self.assertEqual([space_tagger(t, space_dict) for t in ts.split()],
                         [None, None, None, None, None, None, None])
