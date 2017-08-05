
# Author: Alexandru Varacuta
# Email:  alexandru-varacuta@bookvoyager.org

import argparse
import os
import json
import hashlib
import requests

from src import get_config, sentiment_tagger, NERTagger, CharacterProcessor
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

def time_processor(data):
    return "ALTERNATIVE_TIMELINE"

def sentiment_processor(sent_data):
    """Computes the values for 'sentiment' field in the schema."""
    sent_d = list(drop_none(sent_data))
    sent_list = [{"axis": k, "value": v} for k, v in sent_score(sent_d).items()]
    return {"overall": [sent_list], "timeline": sent_d}

def schemify(ner_data, sent_data, raw_data):
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
        "timeSetting": {
            "labels": {
                "present":
                "past":
                "future":
                "alternative":
            }
        }
        "genre": {
            "spaceSetting": {
                "labels": {
                    "insideearth": 0/1
                    "otherplanets": 0/1
                    "outerspace": 0/1
                    "beyondsolarsystem": 0/1
                }
            }
            "characters":
                "labels": {
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
        "timeSetting": None,
        "genre": None
    }

    space_default = {
        "insideearth": 0,
        "otherplanets": 0,
        "outerspace": 0,
        "beyondsolarsystem": 0,
    }

    fields["sentiment"] = sentiment_processor(sent_data)
    fields["timeSetting"] = {"labels": time_processor(ner_data)}
    fields["id"] = hashlib.sha1(" ".join(raw_data).encode("utf-8")).hexdigest()
    # fields["metadata"] = get_metadata(...)
    fields["metadata"] = {
        "author": "Robert A. Heinlein".lower(),
        "title": "some_title"
    }
    fields["genre"] = {
        "spaceSetting": {"labels": space_default}, # space_processor()
        "characters": {"labels": CharacterProcessor().run(raw_data)}
    }
    return fields

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--destination")
    args = parser.parse_args()

    config = get_config()
    ner_tagger = NERTagger()

    agg = []
    for title in get_data(args.source): # "resources/raw_text" # for test purpose only
        with open(title) as file_ptr, \
             open(config["sentiment_vocab"]) as vocab_ptr:
            file_content = file_ptr.read()

            vocab = json.load(vocab_ptr)

            sentiment_data = (sentiment_tagger(i, word, vocab)
                              for i, word in enumerate(file_content.split()))

            ner_data = ner_tagger.get_labels(file_content.splitlines())

            data = schemify(ner_data, sentiment_data, file_content.split())

            agg += [data]

    db_write(config["db_service_addr"], agg)


if __name__ == '__main__':
    _main()
