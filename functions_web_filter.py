import json
import csv
from datetime import datetime
import os
dt = datetime.now()
scrapeDate = dt.strftime('%y%m%d')
scrapeTime = dt.strftime('%H%M%S')

def webFilterFunction(andVar, sourceVar, words):

	if sourceVar == "ACM" or "Bakkers" or "Bakkerswereld" or "Ceres" or "Tijd":
		fname =  "Results" + sourceVar +".json"
		
	
	elif sourceVar == "all":
		#..
		return
	else:
		print("shrug...")
		return
	
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
		# publicationDate = line.get('publication date')
		# if sourceVar == "ACM":
		# 	yearVar = publicationDate[8:]
		# 	monthVar = publicationDate[3:5]
		# 	dateVar = publicationDate[0:2]
		# 	compareDate = yearVar+monthVar+dateVar
		# 	print(compareDate)
	    #writes a row and gets the fields from the (now pyton) dict
	    
	#     # if any(x in (line.get('text')).lower() for x in filterArray):
	# if(andVar):

	# 	if all(x in line.get('title').lower() for x in filterArray):
			
	# 	for x in filterArray:
	# 		if x in (line.get('text')).lower():
	# 			if any(x in (line.get('title')).lower() for x in filterArray):
	# 				writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'title & text'])
	# 			else:
	# 				writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'text'])     

	# 		elif x in (line.get('title')).lower():
	# 			writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'title'])
	# else:
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


def webFilterFunctionWithDate(andVar, sourceVar, words, startDate, endDate):

	if sourceVar == "ACM" or "Bakkers" or "Bakkerswereld" or "Ceres" or "Tijd" or "Dossche" or "Soufflet":
		fname =  "Results" + sourceVar +".json"
		

	elif sourceVar == "all":
		#..
		return
	else:
		print("shrug...")
		return


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
		publicationDate = line.get('publication date')
		if sourceVar == "ACM":
			yearVar = publicationDate[8:]
			monthVar = publicationDate[3:5]
			dateVar = publicationDate[0:2]
			compareDate = yearVar+monthVar+dateVar
			print(compareDate)
			if ((int(startDate)>int(compareDate)) or (int(endDate)<int(compareDate))):
				continue

		elif sourceVar == "Bakkers":
			print("cant filter by date, only month & year")
			startDateLoopVar = "20" + startDate[0:2]
			endDateLoopVar = "20" + endDate[0:2]
			endDateLoopVar = int(endDateLoopVar) + 1
			continueVar = False
			for x in range(int(startDateLoopVar), int(endDateLoopVar)):
				# print(x)
				if (str(x) in publicationDate):
					print("did it work?")
					continueVar = True

			if(continueVar == False):
				continue

			yearVar = publicationDate[-2:]
			if "januari" in publicationDate.lower():
				monthVar = "01"
			elif "februari" in publicationDate.lower():
				monthVar = "02"
			elif "maart" in publicationDate.lower():
				monthVar = "03"
			elif "apr" in publicationDate.lower():
				monthVar = "04"
			elif "mei" in publicationDate.lower():
				monthVar = "05"
			elif "may" in publicationDate.lower():
				monthVar = "05"
			elif "juni" in publicationDate.lower():
				monthVar = "06"
			elif "juli" in publicationDate.lower():
				monthVar = "07"
			elif "aug" in publicationDate.lower():
				monthVar = "08"
			elif "sep" in publicationDate.lower():
				monthVar = "09"
			elif "okt" in publicationDate.lower():
				monthVar = "10"
			elif "november" in publicationDate.lower():
				monthVar = "11"
			elif "december" in publicationDate.lower():
				monthVar = "12"
			else: monthVar = "00"
			dateVar = "00"
			compareDate = yearVar+monthVar+dateVar
			if ((int(startDate)>int(compareDate)) or (int(endDate)<int(compareDate))):
				continue

		elif sourceVar == "Bakkerswereld":
			yearVar = publicationDate[2:4]
			monthVar = publicationDate[5:7]
			dateVar = publicationDate[8:]
			compareDate = yearVar+monthVar+dateVar
			# print(compareDate)
			if ((int(startDate)>int(compareDate)) or (int(endDate)<int(compareDate))):
				continue

		elif sourceVar == "Ceres":
			yearVar = publicationDate[-2:]
			if "jan" in publicationDate:
				monthVar = "01"
			elif "feb" in publicationDate:
				monthVar = "02"
			elif "maart" in publicationDate:
				monthVar = "03"
			elif "apr" in publicationDate:
				monthVar = "04"
			elif "mei" in publicationDate:
				monthVar = "05"
			elif "jun" in publicationDate:
				monthVar = "06"
			elif "jul" in publicationDate:
				monthVar = "07"
			elif "aug" in publicationDate:
				monthVar = "08"
			elif "sep" in publicationDate:
				monthVar = "09"
			elif "okt" in publicationDate:
				monthVar = "10"
			elif "nov" in publicationDate:
				monthVar = "11"
			elif "dec" in publicationDate:
				monthVar = "12"
			else: monthVar = "00"
			dateVar = "00"
			compareDate = yearVar+monthVar+dateVar
			if ((int(startDate)>int(compareDate)) or (int(endDate)<int(compareDate))):
				continue

		elif sourceVar == "Dossche":
			print("no date filter possible for Dossche")

		elif sourceVar == "Soufflet":
			yearVar = publicationDate[-2:]
			if "jan" in publicationDate:
				monthVar = "01"
			elif "f" in publicationDate:
				monthVar = "02"
			elif "mars" in publicationDate:
				monthVar = "03"
			elif "apr" in publicationDate:
				monthVar = "04"
			elif "mei" in publicationDate:
				monthVar = "05"
			elif "juin" in publicationDate:
				monthVar = "06"
			elif "juil" in publicationDate:
				monthVar = "07"
			elif "aug" in publicationDate:
				monthVar = "08"
			elif "sep" in publicationDate:
				monthVar = "09"
			elif "oct" in publicationDate:
				monthVar = "10"
			elif "nov" in publicationDate:
				monthVar = "11"
			elif "d" in publicationDate:
				monthVar = "12"
			else: 
				print("no month found")
				monthVar = "00"
			dateVar = publicationDate[0:2]
			compareDate = yearVar+monthVar+dateVar
			# print(compareDate)
			if ((int(startDate)>int(compareDate)) or (int(endDate)<int(compareDate))):
				continue
		
		elif sourceVar == "Tijd":
			print(publicationDate)
			yearVar = publicationDate[2:4]
			monthVar = publicationDate[5:7]
			dateVar = publicationDate[8:]
			compareDate = yearVar+monthVar+dateVar
			print(compareDate)
			if ((int(startDate)>int(compareDate)) or (int(endDate)<int(compareDate))):
				continue



	    #writes a row and gets the fields from the (now pyton) dict
	    
	#     # if any(x in (line.get('text')).lower() for x in filterArray):
	# if(andVar):

	# 	if all(x in line.get('title').lower() for x in filterArray):
			
	# 	for x in filterArray:
	# 		if x in (line.get('text')).lower():
	# 			if any(x in (line.get('title')).lower() for x in filterArray):
	# 				writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'title & text'])
	# 			else:
	# 				writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'text'])     

	# 		elif x in (line.get('title')).lower():
	# 			writer.writerow([line.get('title'), line.get('url'), line.get('text'), line.get('publication date'), line.get('source'), filterArray, x, 'title'])
	# else:
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