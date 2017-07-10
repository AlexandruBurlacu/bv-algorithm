"""ner_tagger_server module

This module contains 2 classes,
one responsible for running an XML-RPC Server - `RPCServer`
second one encapsulates required behaviour for the NER tagger - `NlpNER`,
with the method `streamming_ner_tagger`.

On executing the `python ner_tagger_server.py` in terminal
there will be instatiated an RPC server bind to
address and port specified in `config.json` file.
"""

# Author: Alexandru Burlacu
# Email:  alexandru-varacuta@bookvoyager.org

from xmlrpc import server
import spacy

from utilities import get_config

CONFIG = get_config()


class NlpNER:
    """The class that will be available as a proxy object on the client side"""
    def __init__(self):
        self.nlp = spacy.load("en")
        self.ner_tagger = lambda word: (str(word), str(word.label), str(word.label_))

    def streamming_ner_tagger(self, stream, batch_size=CONFIG["ner_tagger"]["batch_size"],
                              n_threads=CONFIG["ner_tagger"]["n_threads"]):
        """The method is executed remotely.

        Due to the fact that a lot of `spacy` classes/objects
        and python generators can't be pickled for futher transmition,
        the method require the whole iterable to be sent for processing."""
        nlp_pipeline = self.nlp.pipe(stream, batch_size=batch_size, n_threads=n_threads)
        return [self.ner_tagger(word) for doc in nlp_pipeline for word in doc.ents]


class RPCServer:
    """The class responible for providing a proxy of a class instance through RPC."""
    def __init__(self, addr, port):
        self.server = server.SimpleXMLRPCServer((addr, port))

    def register(self, obj):
        """Taking a class instance, makes it available on the client side, as a proxy."""
        self.server.register_instance(obj)
        return self

    def run(self):
        """Launches the server and waits for `Ctrl-C` to exit."""
        try:
            print("Shit is about to happen.\nCtrl-C to exit")
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\nExiting gracefully")

def _main():
    _address = CONFIG["ner_tagger"]["address"]
    _port = CONFIG["ner_tagger"]["port"]
    RPCServer(_address, _port).register(NlpNER()).run()

if __name__ == '__main__':
    _main()
