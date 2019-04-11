#!/bin/bash
cd Desktop/test/WebServer
mongoimport --host ScrapedNews-shard-0/scrapednews-shard-00-00-3zys9.azure.mongodb.net:27017,scrapednews-shard-00-01-3zys9.azure.mongodb.net:27017,scrapednews-shard-00-02-3zys9.azure.mongodb.net:27017 --ssl --username serverUser --password News@hammer4 --authenticationDatabase admin --db CSKdata --collection FIFnews --type json --file allTime/ResultsFIF.json
mongoexport --host ScrapedNews-shard-0/scrapednews-shard-00-00-3zys9.azure.mongodb.net:27017,scrapednews-shard-00-01-3zys9.azure.mongodb.net:27017,scrapednews-shard-00-02-3zys9.azure.mongodb.net:27017 --ssl --username serverUser --password News@hammer4 --authenticationDatabase admin --db CSKdata --collection FIFnews --type json --out allTime/ResultsFIF.json
python3 -c 'from databaseManage import fixData; fixData("FIF")'
