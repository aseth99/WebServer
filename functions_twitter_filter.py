import os, datetime, re, hashlib
import requests

import csv
from datetime import datetime
from bs4 import BeautifulSoup
import json

import sys
dt = datetime.now()
scrapeDate = dt.strftime('%y%m%d')
scrapeTime = dt.strftime('%H%M%S')

def deleteFile(fileName):
	directoryName = os.path.join(scrapeDate,fileName)

	os.makedirs(os.path.dirname(directoryName), exist_ok=True)
	# for root, dirs, files in os.walk("."):  
	# 	print(root)
	# 	print(dirs)
		# for filename in files:
		# 	print(filename)
	os.remove(directoryName + '.csv')

def handleFilter(handle, words, andVar):
	
	fname =  "@" + handle +".json"

	# if todayVar == True:
	# 	directoryName = os.path.join(scrapeDate,fname)
	# else:
	directoryName = os.path.join("allTime", fname)

	os.makedirs(os.path.dirname(directoryName), exist_ok=True)


	chooseName = "filterTwitter_@" + handle + "_" + scrapeDate #+ '_' + scrapeTime


	csvFileName = scrapeDate + "/" + "{}.csv".format(chooseName)
	csv_out = open(csvFileName, mode='w') #opens csv file
	writer = csv.writer(csv_out) #create the csv writer object

	fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'keywords', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
	writer.writerow(fields) #writes field
	filterArray = words

	tweets = []

	jsonFileToBeOpened = scrapeDate + '/' + fname
	for line in open(jsonFileToBeOpened, 'r'):
		tweets.append(json.loads(line))

	for line in tweets:
		dateOfTweet = line.get('created_at')
		# print(dateOfTweet)
		yearOfTweet = dateOfTweet[-4:]
		monthOfTweet = dateOfTweet[4:7]
		dayofTweet = dateOfTweet[8:10]
		inputDate = dayofTweet + '-' + monthOfTweet + '-' + yearOfTweet

		urlvar = line.get('entities').get('urls')
		if(urlvar):
			urlvar = urlvar[0].get('expanded_url')
		else:
			urlvar = "no external urls"

		hashtagsVar = line.get('entities').get('hashtags')
		tempHashList = []
		if not hashtagsVar:
			hashtagsVar = "no hashtags"
		else:
			for i in hashtagsVar:
				tempHashList.append(i['text'])
			hashtagsVar = tempHashList


		if len(line.get('text')) > 50:
			textVar = line.get('text')[0:50] + "..."
		else:
			textVar = line.get('text') + "..."
 
		#And search
		if(andVar):
			if all(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar, #unicode escape to fix emoji issue
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("and....got here..")
		#or search
		else:
			if any(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar,
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("or....got here..")
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
	return row_count, chooseName, fields, rows


def handleFilterWithDate(handle, words, andVar, startDate, endDate):
	
	fname =  "@" + handle +".json"

	# if todayVar == True:
	# 	directoryName = os.path.join(scrapeDate,fname)
	# else:
	directoryName = os.path.join("allTime", fname)

	os.makedirs(os.path.dirname(directoryName), exist_ok=True)


	chooseName = "filterTwitter_@" + handle + "_" + scrapeDate #+ '_' + scrapeTime


	csvFileName = scrapeDate + "/" + "{}.csv".format(chooseName)
	csv_out = open(csvFileName, mode='w') #opens csv file
	writer = csv.writer(csv_out) #create the csv writer object

	fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'keywords', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
	writer.writerow(fields) #writes field
	filterArray = words

	tweets = []

	jsonFileToBeOpened = scrapeDate + '/' + fname
	for line in open(jsonFileToBeOpened, 'r'):
		tweets.append(json.loads(line))

	for line in tweets:
		dateOfTweet = line.get('created_at')
		# print(dateOfTweet)
		yearOfTweet = dateOfTweet[-4:]
		monthOfTweet = dateOfTweet[4:7]
		dayofTweet = dateOfTweet[8:10]
		inputDate = dayofTweet + '-' + monthOfTweet + '-' + yearOfTweet
		
		if monthOfTweet == "Jan":
			numMonth = "01"
		elif monthOfTweet == "Feb":
			numMonth = "02"
		elif monthOfTweet == "Mar":
			numMonth = "03"
		elif monthOfTweet == "Apr":
			numMonth = "04"
		elif monthOfTweet == "May":
			numMonth = "05"
		elif monthOfTweet == "Jun":
			numMonth = "06"
		elif monthOfTweet == "July":
			numMonth = "07"
		elif monthOfTweet == "Aug":
			numMonth = "08"
		elif monthOfTweet == "Sep":
			numMonth = "09"
		elif monthOfTweet == "Oct":
			numMonth = "10"
		elif monthOfTweet == "Nov":
			numMonth = "11"
		elif monthOfTweet == "Dec":
			numMonth = "12"

		filterCompareDate = (yearOfTweet+numMonth+dayofTweet)[2:]
		# print(filterCompareDate)

		if ((int(startDate)>int(filterCompareDate)) or (int(endDate)<int(filterCompareDate))):
			continue

		urlvar = line.get('entities').get('urls')
		if(urlvar):
			urlvar = urlvar[0].get('expanded_url')
		else:
			urlvar = "no external urls"

		hashtagsVar = line.get('entities').get('hashtags')
		tempHashList = []
		if not hashtagsVar:
			hashtagsVar = "no hashtags"
		else:
			for i in hashtagsVar:
				tempHashList.append(i['text'])
			hashtagsVar = tempHashList


		if len(line.get('text')) > 50:
			textVar = line.get('text')[0:50] + "..."
		else:
			textVar = line.get('text') + "..."
 
		#And search
		if(andVar):
			if all(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar, #unicode escape to fix emoji issue
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("and....got here..")
		#or search
		else:
			if any(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar,
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("or....got here..")
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
	return row_count, chooseName, fields, rows


def handleGroupFilter(groupName, words, andVar):
	if groupName == "csk":
		fname =  "CSKallTwitter.json"
	elif groupName == "kkm":
		fname = "KKMallTwitter.json"
	else: 
		print("shrug...")
		return 
	# if todayVar == True:
	# 	directoryName = os.path.join(scrapeDate,fname)
	# else:
	directoryName = os.path.join("allTime", fname)

	os.makedirs(os.path.dirname(directoryName), exist_ok=True)


	chooseName = "filterTwitter_@" + groupName + "_" + scrapeDate #+ '_' + scrapeTime


	csvFileName = scrapeDate + "/" + "{}.csv".format(chooseName)
	csv_out = open(csvFileName, mode='w') #opens csv file
	writer = csv.writer(csv_out) #create the csv writer object

	fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'keywords', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
	writer.writerow(fields) #writes field
	filterArray = words

	tweets = []

	jsonFileToBeOpened = "allTime" + '/' + fname
	for line in open(jsonFileToBeOpened, 'r'):
		tweets.append(json.loads(line))

	for line in tweets:
		dateOfTweet = line.get('created_at')
		# print(dateOfTweet)
		yearOfTweet = dateOfTweet[-4:]
		monthOfTweet = dateOfTweet[4:7]
		dayofTweet = dateOfTweet[8:10]
		inputDate = dayofTweet + '-' + monthOfTweet + '-' + yearOfTweet

		urlvar = line.get('entities').get('urls')
		if(urlvar):
			urlvar = urlvar[0].get('expanded_url')
		else:
			urlvar = "no external urls"

		hashtagsVar = line.get('entities').get('hashtags')
		tempHashList = []
		if not hashtagsVar:
			hashtagsVar = "no hashtags"
		else:
			for i in hashtagsVar:
				tempHashList.append(i['text'])
			hashtagsVar = tempHashList


		if len(line.get('text')) > 50:
			textVar = line.get('text')[0:50] + "..."
		else:
			textVar = line.get('text') + "..."
 
		#And search
		if(andVar):
			if all(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar, #unicode escape to fix emoji issue
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("and....got here..")
		#or search
		else:
			if any(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar,
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("or....got here..")
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
	return row_count, chooseName, fields, rows


def handleGroupFilterWithDate(groupName, words, andVar, startDate, endDate):
	
	if groupName == "csk":
		fname =  "CSKallTwitter.json"
	elif groupName == "kkm":
		fname = "KKMallTwitter.json"
	else: 
		print("shrug...")
		return 
	# if todayVar == True:
	# 	directoryName = os.path.join(scrapeDate,fname)
	# else:
	directoryName = os.path.join("allTime", fname)

	os.makedirs(os.path.dirname(directoryName), exist_ok=True)


	chooseName = "filterTwitter_@" + groupName + "_" + scrapeDate #+ '_' + scrapeTime

	csvFileName = scrapeDate + "/" + "{}.csv".format(chooseName)
	csv_out = open(csvFileName, mode='w') #opens csv file
	writer = csv.writer(csv_out) #create the csv writer object

	fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'keywords', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
	writer.writerow(fields) #writes field
	filterArray = words

	tweets = []

	jsonFileToBeOpened = "allTime" + '/' + fname
	for line in open(jsonFileToBeOpened, 'r'):
		tweets.append(json.loads(line))

	for line in tweets:
		dateOfTweet = line.get('created_at')
		# print(dateOfTweet)
		yearOfTweet = dateOfTweet[-4:]
		monthOfTweet = dateOfTweet[4:7]
		dayofTweet = dateOfTweet[8:10]
		inputDate = dayofTweet + '-' + monthOfTweet + '-' + yearOfTweet
		
		if monthOfTweet == "Jan":
			numMonth = "01"
		elif monthOfTweet == "Feb":
			numMonth = "02"
		elif monthOfTweet == "Mar":
			numMonth = "03"
		elif monthOfTweet == "Apr":
			numMonth = "04"
		elif monthOfTweet == "May":
			numMonth = "05"
		elif monthOfTweet == "Jun":
			numMonth = "06"
		elif monthOfTweet == "July":
			numMonth = "07"
		elif monthOfTweet == "Aug":
			numMonth = "08"
		elif monthOfTweet == "Sep":
			numMonth = "09"
		elif monthOfTweet == "Oct":
			numMonth = "10"
		elif monthOfTweet == "Nov":
			numMonth = "11"
		elif monthOfTweet == "Dec":
			numMonth = "12"

		filterCompareDate = (yearOfTweet+numMonth+dayofTweet)[2:]
		# print(filterCompareDate)

		if ((int(startDate)>int(filterCompareDate)) or (int(endDate)<int(filterCompareDate))):
			continue

		urlvar = line.get('entities').get('urls')
		if(urlvar):
			urlvar = urlvar[0].get('expanded_url')
		else:
			urlvar = "no external urls"

		hashtagsVar = line.get('entities').get('hashtags')
		tempHashList = []
		if not hashtagsVar:
			hashtagsVar = "no hashtags"
		else:
			for i in hashtagsVar:
				tempHashList.append(i['text'])
			hashtagsVar = tempHashList


		if len(line.get('text')) > 50:
			textVar = line.get('text')[0:50] + "..."
		else:
			textVar = line.get('text') + "..."
 
		#And search
		if(andVar):
			if all(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar, #unicode escape to fix emoji issue
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("and....got here..")
		#or search
		else:
			if any(x in line.get('text').lower() for x in filterArray):

				writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
				textVar,
				urlvar,
				hashtagsVar,
				filterArray,
				inputDate,
				line.get('user').get('followers_count'),
				line.get('user').get('friends_count'),
				line.get('retweet_count'),
				line.get('favorite_count')])

				# print("or....got here..")
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
	return row_count, chooseName, fields, rows
