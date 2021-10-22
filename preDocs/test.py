#!/usr/bin/env python3

import json

with open("testJson.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

product = jsonObject['firstName']
overall = jsonObject['address']

print(product)
print(overall) 