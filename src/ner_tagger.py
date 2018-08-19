"""ner_tagger_client module

This is the client part of the `ner_tagger` system.
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org

import spacy
from .utilities import get_config

class NlpNER:
    """The class that will be available as a proxy object on the client side"""
    def __init__(self):
        self.nlp = spacy.load("en")
        self.ner_tagger = lambda word: (str(word), str(word.label), str(word.label_))

    def streamming_ner_tagger(self, stream, batch_size, n_threads):
        """The method is executed remotely.

        Due to the fact that a lot of `spacy` classes/objects
        and python generators can't be pickled for futher transmition,
        the method require the whole iterable to be sent for processing."""
        nlp_pipeline = self.nlp.pipe(stream, batch_size=batch_size, n_threads=n_threads)
        return (self.ner_tagger(word) for doc in nlp_pipeline for word in doc.ents)

class NERTagger:
    def __init__(self):
        self._config = get_config()
        self.nlp = NlpNER()

    def get_labels(self, source):
        """Given the iterable `source`, returns a list of entities."""
        return self.nlp.streamming_ner_tagger(source, self._config["ner_tagger"]["batch_size"],
                                              self._config["ner_tagger"]["n_threads"])

