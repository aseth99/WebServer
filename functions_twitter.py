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
    fname =  scrapeDate + "@" + handle +".json"
    fname2 =  "allTime_" + "@" + handle +".json"

    client = get_twitter_client()

    print("scraping {}".format(handle))
    with open(fname, 'w') as f:
        for page in Cursor(client.user_timeline, screen_name=handle, count=200).pages(2):
            for status in page:
                f.write(json.dumps(status._json)+"\n")

    with open(fname2, 'a') as f2:
        for page in Cursor(client.user_timeline, screen_name=handle, count=200).pages(2):
            for status in page:
                f2.write(json.dumps(status._json)+"\n")


    #current dates csv file
    chooseName = scrapeDate + handle
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='w') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = fname
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
    #all time csv file, append data here
    chooseName = "AllTime_" + handle
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = fname
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
    return True

def twitterFunctionAll():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
   
    userArr = ["bakkerswereldnl", "BakkersinB", "BakkerijCentrum", "BakeryNext", "dossche_mills", "GroupeSoufflet"]
    fname = scrapeDate + "_allTwitter" + ".json"
    fname2 = "allTime" + "_allTwitter" + ".json"

    client = get_twitter_client()

    for user in userArr:
        print("scraping {}".format(user))
        with open(fname, 'a') as f:
            for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(2):
                for status in page:
                    f.write(json.dumps(status._json)+"\n")
        with open(fname2, 'a') as f2:
            for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(2):
                for status in page:
                    f2.write(json.dumps(status._json)+"\n")

    #todays stuff
    chooseName = scrapeDate + "allTwitter"
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = fname
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

    #all time stuff
    chooseName = "allTime_" + "allTwitter"
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = fname
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
    return True
