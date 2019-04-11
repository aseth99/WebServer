#!/usr/bin/env python3
import json
import os

def fixData(x):
    fileScrapeResults = 'Results' + x + '.json'

    directoryName2 = os.path.join("allTime",fileScrapeResults)
    os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

    dataLine = []
    jsonFileToBeOpened = directoryName2
    try:
        for line in open(jsonFileToBeOpened, 'r'):
            dataLine.append(json.loads(line))
    except:
        print("no results file yet")

    uniqueLine2 = { each['url'] : each for each in dataLine }.values()
    uniqueLine = { each['articleID'] : each for each in uniqueLine2 }.values()

    with open(directoryName2, 'w') as f2:
            for line in uniqueLine:
                f2.write(json.dumps(line)+"\n")
    return