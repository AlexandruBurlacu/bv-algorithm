"""ner_tagger_client module

This is the client part of the `ner_tagger` system.
"""

# Author: Alexandru Varacuta
# Email:  alexandru-varacuta@bookvoyager.org

from xmlrpc import client
from .utilities import get_config

class NERTagger:
    def __init__(self):
        self._config = get_config()
        self._full_url = "http://{address}:{port}".format(**self._config["ner_tagger"])
        self._proxy = client.ServerProxy(self._full_url)

    def get_labels(self, source):
        """Given the iterable `source`, returns a list of entities."""
        return self._proxy.streamming_ner_tagger(source)

