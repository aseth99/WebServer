import json
import pymongo 
import os
from bson.json_util import loads


myclient = pymongo.MongoClient("mongodb+srv://serverUser:XXXX@scrapednews-3zys9.azure.mongodb.net/test?retryWrites=true")
# db = client.test

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["KKMdata"]

mycol = mydb["KKMnews"]

#inserted once.. only run this file once, or comment this section out if u fina run again
fileScrapeResults = 'ResultsAllKKM' + '.json'
directoryName2 = os.path.join("allTime",fileScrapeResults)
os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

tweets = []
# jsonFileToBeOpened = "news.json"
with open(directoryName2) as f2:
    for line in f2:
        mycol.insert(json.loads(line))      
