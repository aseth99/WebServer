import json
import csv
from datetime import datetime
import os
dt = datetime.now()
scrapeDate = dt.strftime('%y%m%d')
scrapeTime = dt.strftime('%H%M%S')

def webFilterFunction(andVar, todayVar, sourceVar, words):

	if sourceVar == "ACM" or "Bakkers" or "Bakkerswereld" or "Ceres" or "Tijd":
		fname =  "Results" + sourceVar +".json"
		
	# elif sourceVar == "Bakkers":
	# 	#..
	# elif sourceVar == "Bakkerswereld":
	# 	#..
	# elif sourceVar == "Ceres":
	# 	#..
	# elif sourceVar == "Tijd":
	# 	#..
	elif sourceVar == "all":
		#..
		return
	else:
		print("shrug...")
		return
	# print(fname)

	if todayVar == True:
		directoryName = os.path.join(scrapeDate,fname)
	else:
		directoryName = os.path.join("allTime", fname)

	os.makedirs(os.path.dirname(directoryName), exist_ok=True)


	csvName = "filter_Webscraper_" + sourceVar + "_" + scrapeDate #+ '_' + scrapeTime

	# directoryName2 = os.path.join(scrapeDate, csvName)
	# os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

	csvFileName = scrapeDate + "/" + "{}.csv".format(csvName)


	csv_out = open(csvFileName, mode='w') #opens csv file
	writer = csv.writer(csv_out) #create the csv writer object

	# fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'keywords', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names

	fields = ['Title', 'URL', 'Text', 'Publication Date', 'Source', 'Keywords Searched', 'Keyword', 'Found in'] #field names
	writer.writerow(fields) #writes field
	filterArray = words

	texts = []
	# filterArray = ['dossche', 'ceres', 'soufflet', 'meneba', 'overname']

	jsonFileToBeOpened = directoryName
	for lineToBeRead in open(jsonFileToBeOpened, 'r'):
	    texts.append(json.loads(lineToBeRead))

	for line in texts:
	    #writes a row and gets the fields from the (now pyton) dict
	    
	#     # if any(x in (line.get('text')).lower() for x in filterArray):
	    for x in filterArray:
	        if x in (line.get('text')).lower():
	            if any(x in (line.get('title')).lower() for x in filterArray):
	                writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'title & text'])
	            else:
	                writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'text'])     
	        

	        elif x in (line.get('title')).lower():
	            writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'title'])

	csv_out.close()

	csv_out = open(csvFileName, mode='r') #opens csv file
	reader = csv.reader(csv_out)
	rows = []
	iterReader = iter(reader)
	next(iterReader)
	row_count = 0
	for row in iterReader:
		row_count = row_count + 1
		rows.append(row)
	return row_count, csvName, fields, rows