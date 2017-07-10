
# Author: Alexandru Varacuta
# Email:  alexandru-varacuta@bookvoyager.org

import argparse
import os
import json
import requests

from src import get_config, sentiment_tagger, NERTagger
from src.utilities import drop_none

def db_write(db_service_url, sources):
    """Wraps the underling request to the database service."""
    requests.put(db_service_url + "/write",
                 data=json.dumps({"source": sources}),
                 headers={"content-type": "application/json"})

def get_data(source_dir):
    """Given `source_dir` string, returns all the
    `.txt` files in the dirs and subdirs of the source"""
    for path, _, files in os.walk(source_dir):
        for filename in files:
            if filename.endswith(".txt"):
                yield os.path.join(path, filename)

def sent_score(sent_data):
    """Computes the 'sentiment snapshot' of the book."""
    sent_dict = {
        "fear": 0,
        "joy": 0,
        "sadness": 0,
        "anger": 0,
        "love": 0,
        "surprise": 0
    }
    for score, cat, _, _ in sent_data:
        sent_dict[cat] += score

    return sent_dict

def sentiment_processor(sent_data):
    """Computes the values for 'sentiment' field in the schema."""
    sent_d = drop_none(sent_data)
    return {"overall": sent_score(sent_d), "timeline": sent_d}

def get_times(entities):
    """Extracts time related tokens or
    combinations of them for futher interpretation."""
    data = []
    for label in entities:
        if label[2] == "DATE":
            data += [label[0]]

    return data

def time_processor(entities):
    """Computes the values for the 'time' field of the schema.

    I need a dictionary with words/n-grams classified
    as `past`, `present`, `future`, `alternative`.

    Or as an alternative idea, to train a ML model (ex. Perceptron)"""
    result = {
        "present": False,
        "past": False,
        "future": False,
        "alternative": False
    }
    data = get_times(entities)

    return {"labels": data} # not finished!

def schemify(ner_data, sent_data):
    """The schema
    book_name: {
        "id":
        "metadata": {
            "author":
            "pagecount":
            "genre":
            "authorgender": [F, M]
            "country":
            "lengthtag": [short, medium, long]
            "pubyear":
        }
        "sentiment": {
            "timeline": []
            "overall": {
                "fear":
                "joy":
                "sadness":
                "love":
                "surprise":
                "anger":
            }
        }
        "time": {
            "labels": {
                "present":
                "past":
                "future":
                "alternative":
            }
        }
        "genre": {
            "space": {
                "labels": {
                    "insideearth": 0/1
                    "otherplanets": 0/1
                    "outerspace": 0/1
                    "beyondsolarsystem": 0/1
                }
            }
            "characters": {
                "aliens": 0/1
                "mutants": 0/1
                "robots": 0/1
                "humanoiddroids": 0/1
                "dragons": 0/1
                "superintelligence": 0/1
            }
        }
    }
    """
    fields = {
        "id": None,
        "sentiment": None,
        "metadata": None,
        "time": None,
        "genre": None
    }
    fields["sentiment"] = sentiment_processor(sent_data)
    fields["time"] = time_processor(ner_data)
    # fields["id"] =
    # fields["metadata"] = get_metadata(...)
    # fields["genre"] = get_genre(...)
    return get_times(ner_data)

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--destination")
    args = parser.parse_args()

    config = get_config()
    ner_tagger = NERTagger()


    for title in get_data(args.source): # "resources/raw_text" # for test purpose only
        with open(title) as file_ptr, \
             open(config["sentiment_vocab"]) as vocab_ptr:
            file_content = file_ptr.read().split()

            vocab = json.load(vocab_ptr)

            sentiment_data = (sentiment_tagger(i, word, vocab)
                              for i, word in enumerate(file_content))

            _ = file_ptr.seek(0) # [WARNING] the `file_ptr`s data will be now available again
            ner_data = ner_tagger.get_labels(file_ptr.readlines())

            data = schemify(ner_data, sentiment_data)

            print(data)
            # db_write(config["db_service_addr"], data)

    return NotImplemented

if __name__ == '__main__':
    _main()
