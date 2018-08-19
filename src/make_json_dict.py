# Author: Alexandru Varacuta
# Email:  alexandru-varacuta@bookvoyager.org

import json

TYPES = [("surprise", 1),
         ("fear", -1),
         ("anger", -1),
         ("sadness", -1),
         ("joy", 1),
         ("love", 1)]

with open("../resources/library_test.json", "w") as fp:
    for topic, score in TYPES:
        data = open("../resources/emotions/{}.txt".format(topic)).read().split()
        data_dict = {e: {"category": topic, "sentiment": score} for e in data}

        json.dump(data_dict, fp, indent=4)

# don't forget to get rid of surplus curly braces in the file
