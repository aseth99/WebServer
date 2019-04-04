import json
import os

filesArr = ['ACM', 'AllKKM', 'Bakkers', 'Bakkerswereld', 'Ceres','Dossche', 'Soufflet', 'Tijd']

for x in filesArr:
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

    for x in documents:
        dataLine.append(x)

    uniqueLine = { each['articleID'] : each for each in dataLine }.values()
