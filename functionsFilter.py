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

def handleFilter(handle, words):
	
	fname =  "@" + handle +".json"

	directoryName = os.path.join(scrapeDate,fname)

	os.makedirs(os.path.dirname(directoryName), exist_ok=True)


	chooseName = "filterTwitter_@" + handle + "_" + scrapeDate #+ '_' + scrapeTime


	csvFileName = scrapeDate + "/" + "{}.csv".format(chooseName)
	csv_out = open(csvFileName, mode='w') #opens csv file
	writer = csv.writer(csv_out) #create the csv writer object

	fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
	writer.writerow(fields) #writes field
	filterArray = words

	tweets = []

	jsonFileToBeOpened = scrapeDate + '/' + fname
	for line in open(jsonFileToBeOpened, 'r'):
		tweets.append(json.loads(line))

	for line in tweets:
		dateOfTweet = line.get('created_at')
		yearOfTweet = dateOfTweet[-4:]
		monthOfTweet = dateOfTweet[4:7]
		dayofTweet = dateOfTweet[8:10]
		inputDate = dayofTweet + '-' + monthOfTweet + '-' + yearOfTweet

		urlvar = line.get('entities').get('urls')
		if(urlvar):
			urlvar = urlvar[0].get('expanded_url')
		else:
			urlvar = "no external urls in this tweet"

		hashtagsVar = line.get('entities').get('hashtags')
		tempHashList = []
		if not hashtagsVar:
			hashtagsVar = "no hashtags in this tweet"
		else:
			for i in hashtagsVar:
				tempHashList.append(i['text'])
			hashtagsVar = tempHashList


		if any(x in line.get('text') for x in filterArray):

			writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'), 
			line.get('text'), #unicode escape to fix emoji issue
			urlvar,
			hashtagsVar,
			filterArray,
			inputDate,
			line.get('user').get('followers_count'),
			line.get('user').get('friends_count'),
			line.get('retweet_count'),
			line.get('favorite_count')])

			print("got here..")
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
