import sys
import os, datetime, re, hashlib
import requests

import csv
from datetime import datetime
from bs4 import BeautifulSoup
import json

from twitter_scraper_client import get_twitter_client
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor


def twitterFunction(handle):
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')

    fname =  "@" + handle +".json"
    fname2 =  "@" + handle +".json"

    directoryName = os.path.join(scrapeDate,fname)
    directoryName2 = os.path.join("allTime",fname2)

    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

    client = get_twitter_client()

    print("scraping {}".format(handle))
    with open(directoryName, 'w') as f, open(directoryName2, 'a') as f2:
        for page in Cursor(client.user_timeline, screen_name=handle, count=200).pages(8):
            for status in page:
                f.write(json.dumps(status._json)+"\n")
                f2.write(json.dumps(status._json)+"\n")


    handleSuf = "@" + handle + ".csv"
    directoryName3 = os.path.join(scrapeDate,handleSuf)
    #current dates csv file
    csv_out = open(directoryName3, mode='w') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = directoryName
    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    uniqueTweets = { each['id'] : each for each in tweets }.values()

    for line in uniqueTweets:
        
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

        writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'),
            line.get('text').encode('unicode_escape'), #unicode escape to fix emoji issue
            urlvar,
            hashtagsVar,
            line.get('created_at'),
            line.get('user').get('followers_count'),
            line.get('user').get('friends_count'),
            line.get('retweet_count'),
            line.get('favorite_count')])
         
    csv_out.close()

    handleSuf = "@" + handle + ".csv"
    directoryName4 = os.path.join("allTime",handleSuf)
   
    #all time csv file, append data here
    # chooseName = "AllTime_" + handle
    # csvFileName = "{}.csv".format(chooseName)
    csv_out = open(directoryName4, mode='w') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []
    #only appending new stuff, thus open new json file
    jsonFileToBeOpened = directoryName2
    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    uniqueTweets = { each['id'] : each for each in tweets }.values()
    with open(directoryName2, 'w') as f2:

        for line in uniqueTweets:
            f2.write(json.dumps(line)+"\n")
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

            writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'),
                line.get('text').encode('unicode_escape'), #unicode escape to fix emoji issue
                urlvar,
                hashtagsVar,
                line.get('created_at'),
                line.get('user').get('followers_count'),
                line.get('user').get('friends_count'),
                line.get('retweet_count'),
                line.get('favorite_count')])
             
    csv_out.close()
    return True

def twitterFunctionAllKKM():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
   
    userArr = ["bakkerswereldnl", "BakkersinB", "BakkerijCentrum", "BakeryNext", "dossche_mills", "GroupeSoufflet"]
    fname = "KKMallTwitter" + ".json"
    fname2 = "KKMallTwitter" + ".json"

    directoryName = os.path.join(scrapeDate,fname)
    directoryName2 = os.path.join("allTime",fname2)

    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

    client = get_twitter_client()

    for user in userArr:
        print("scraping {}".format(user))
        with open(directoryName, 'w') as f, open(directoryName2, 'a') as f2:
            for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(8):
                for status in page:
                    f.write(json.dumps(status._json)+"\n")
                    f2.write(json.dumps(status._json)+"\n")


    handleSuf = "@KKMallTwitter" + ".csv"
    directoryName3 = os.path.join(scrapeDate,handleSuf)
    
    #todays stuff
    # chooseName = scrapeDate + "allTwitter"
    # csvFileName = "{}.csv".format(chooseName)
    csv_out = open(directoryName3, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = directoryName
    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    uniqueTweets = { each['id'] : each for each in tweets }.values()


    for line in uniqueTweets:
        
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

        writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'),
            line.get('text').encode('unicode_escape'), #unicode escape to fix emoji issue
            urlvar,
            hashtagsVar,
            line.get('created_at'),
            line.get('user').get('followers_count'),
            line.get('user').get('friends_count'),
            line.get('retweet_count'),
            line.get('favorite_count')])
         
    csv_out.close()

    handleSuf = "@KKMallTwitter" + ".csv"
    directoryName4 = os.path.join("allTime",handleSuf)
    
    #all time stuff
    # chooseName = "allTime_" + "allTwitter"
    # csvFileName = "{}.csv".format(chooseName)
    csv_out = open(directoryName4, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []
    #only appending new stuff, thus open new json file
    jsonFileToBeOpened = directoryName2
    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    uniqueTweets = { each['id'] : each for each in tweets }.values()
    
    with open(directoryName2, 'w') as f2:

        for line in uniqueTweets:
            f2.write(json.dumps(line)+"\n")
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

            writer.writerow([line.get('user').get('screen_name')+" , "+line.get('user').get('name'),
                line.get('text').encode('unicode_escape'), #unicode escape to fix emoji issue
                urlvar,
                hashtagsVar,
                line.get('created_at'),
                line.get('user').get('followers_count'),
                line.get('user').get('friends_count'),
                line.get('retweet_count'),
                line.get('favorite_count')])
             
    csv_out.close()
    return True
