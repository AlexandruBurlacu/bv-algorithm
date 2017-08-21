# -*- coding: utf-8 -*-

# Author: Alexandru Varacuta
# Email:  alexandru-varacuta@bookvoyager.org

import argparse
import os
import csv
import json
import hashlib
import requests

from src import get_config, sentiment_tagger, NERTagger, CharacterProcessor, space_tagger
from src.utilities import drop_none, remove_punctuation

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

def space_processor(raw_data, keyword_dict):
    space_dict = {
        "insideearth": 0,
        "otherplanets": 0,
        "outerspace": 0,
        "beyondsolarsystem": 0,
    }
    return space_tagger(remove_punctuation(raw_data), keyword_dict, space_dict)

def sentiment_processor(sent_data):
    """Computes the values for 'sentiment' field in the schema."""
    sent_d = list(drop_none(sent_data))
    sent_list = [{"axis": k, "value": abs(v)} for k, v in sent_score(sent_d).items()]
    return {"overall": [sent_list], "timeline": sent_d}

def get_metadata(meta_data):
    """
    "metadata": {
            "author":
            "title":
            "goodreads_score":
            "goodreads_n_rev":
            "cover_url":
            "pagecount":
            "genre":
            "authorgender": [F, M]
            "country":
            "lengthtag": [short, medium, long]
            "pubyear":
            "description":
        }

    Meta file columns order
        Title,Author,GoodrReads Stars,GoodReads # Reviews,Cover URL,Description,Filename
    """
    metadata = {}
    metadata.update({"author": meta_data[1]})
    metadata.update({"title": meta_data[0]})
    metadata.update({"goodreads_score": meta_data[2] or None})
    metadata.update({"goodreads_n_rev": meta_data[3] or None})
    metadata.update({"cover_url": meta_data[4]})
    metadata.update({"description": meta_data[5]})

    return metadata

def schemify(ner_data, sent_data, space_dict, raw_data, meta_data):
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

    fields["sentiment"] = sentiment_processor(sent_data)
    fields["timeSetting"] = {"labels": time_processor(ner_data)}
    fields["id"] = hashlib.sha1(" ".join(raw_data).encode("utf-8")).hexdigest()
    fields["metadata"] = get_metadata(meta_data)
    fields["genre"] = {
        "spaceSetting": {"labels": space_dict},
        "characters": {"labels": CharacterProcessor().run(raw_data)}
    }
    return fields

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")   # a directory
    parser.add_argument("--metadata") # a .csv file
    args = parser.parse_args()

    config = get_config()
    ner_tagger = NERTagger()

    with open(args.metadata) as m_fptr:
        meta = csv.reader(m_fptr)
        next(meta, None)

        agg = []
        for (col, *cols, file_name) in meta: # "resources/raw_text" # for test purpose only
            title = args.source + "/" + file_name
            meta_data = [col, *cols]

            with open(title, encoding="utf-8", errors="replace") as file_ptr, \
                open(config["sentiment_vocab"]) as sent_vocab_ptr, \
                open(config["space_vocab"]) as space_vocab_ptr:
                file_content = file_ptr.read()

                sent_vocab = json.load(sent_vocab_ptr)
                space_vocab = json.load(space_vocab_ptr)

                sentiment_data = (sentiment_tagger(i, word, sent_vocab)
                                  for i, word in enumerate(file_content.split()))

                ner_data = ner_tagger.get_labels(file_content.splitlines())

                space_dict = space_processor(file_content, space_vocab)

                data = schemify(ner_data, sentiment_data, space_dict,
                                file_content.split(), meta_data)

                agg += [data]
                print(json.dumps(data))
                return

    # db_write(config["db_service_addr"], agg)


if __name__ == '__main__':
    _main()
