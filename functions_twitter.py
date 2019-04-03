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
    # , open(directoryName2, 'a') as f2
    with open(directoryName, 'w') as f:
        for page in Cursor(client.user_timeline, screen_name=handle, count=200).pages(8):
            for status in page:
                f.write(json.dumps(status._json)+"\n")
                # f2.write(json.dumps(status._json)+"\n")


    handleSuf = "@" + handle + ".csv"
    directoryName3 = os.path.join(scrapeDate,handleSuf)
    os.makedirs(os.path.dirname(directoryName3), exist_ok=True)

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

    tweets2 = []
    #only appending new stuff, thus open new json file
    try:
        jsonFileToBeOpened = directoryName2
        for line in open(jsonFileToBeOpened, 'r'):
            tweets2.append(json.loads(line))
    except:
        print("no all time tweets yet")
    uniqueTweets2 = { each['id'] : each for each in tweets2 }.values()

    newTweets = []
    for line in uniqueTweets:
        checkVar = False
        for line2 in uniqueTweets2:
            if line.get('id') == line2.get('id'):
                checkVar = True
        if checkVar:
            continue
        else:
            newTweets.append(line)

    for line in newTweets:
        
        
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

    with open(directoryName, 'w') as f:
        for line in newTweets:
            f.write(json.dumps(line)+"\n")



    handleSuf = "@" + handle + ".csv"
    directoryName4 = os.path.join("allTime",handleSuf)
    os.makedirs(os.path.dirname(directoryName4), exist_ok=True)

    #all time csv file, append data here
    # chooseName = "AllTime_" + handle
    # csvFileName = "{}.csv".format(chooseName)
    csv_out = open(directoryName4, mode='w') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    # tweets = []
    # #only appending new stuff, thus open new json file
    # jsonFileToBeOpened = directoryName2
    # for line in open(jsonFileToBeOpened, 'r'):
    #     tweets.append(json.loads(line))
    for newLine in newTweets:
        tweets2.append(newLine)

    uniqueTweets2 = { each['id'] : each for each in tweets2 }.values()
    # uniqueTweets = { each['id'] : each for each in tweets }.values()

    with open(directoryName2, 'w') as f2:

        for line in uniqueTweets2:
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
    fname = "@KKMallTwitter" + ".json"
    fname2 = "@KKMallTwitter" + ".json"

    directoryName = os.path.join(scrapeDate,fname)
    directoryName2 = os.path.join("allTime",fname2)

    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

    client = get_twitter_client()

    tweetsAccounts = []

    for user in userArr:
        print("scraping {}".format(user))
        twitterFunction(user)
        fnameNew = "@" + user + ".json"
        directoryNameNew = os.path.join("allTime",fnameNew)
        os.makedirs(os.path.dirname(directoryNameNew), exist_ok=True)

        jsonFileToBeOpened = directoryNameNew
        for line in open(jsonFileToBeOpened, 'r'):
            tweetsAccounts.append(json.loads(line))

    with open(directoryName, 'w') as f:
        for line in tweetsAccounts:
            f.write(json.dumps(line)+"\n")

    tweets = []

    jsonFileToBeOpened = directoryName
    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    uniqueTweets = { each['id'] : each for each in tweets }.values()

    tweets2 = []
    #only appending new stuff, thus open new json file
    try:
        jsonFileToBeOpened = directoryName2
        for line2 in open(jsonFileToBeOpened, 'r'):
            tweets2.append(json.loads(line2))
    except:
        print("no all time tweets yet")
    uniqueTweets2 = { each['id'] : each for each in tweets2 }.values()

    newTweets = []
    for line in uniqueTweets:
        checkVar = False
        for line2 in uniqueTweets2:
            if line.get('id') == line2.get('id'):
                checkVar = True
        if checkVar:
            continue
        else:
            newTweets.append(line)

    handleSuf = "@KKMallTwitter" + ".csv"
    directoryName3 = os.path.join(scrapeDate,handleSuf)
    os.makedirs(os.path.dirname(directoryName3), exist_ok=True)

    csv_out = open(directoryName3, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    for line in newTweets:
        # print(line)
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
    
    with open(directoryName, 'w') as f:
        for line in newTweets:
            f.write(json.dumps(line)+"\n")

    handleSuf = "@KKMallTwitter" + ".csv"
    directoryName4 = os.path.join("allTime",handleSuf)
    os.makedirs(os.path.dirname(directoryName4), exist_ok=True)

    csv_out = open(directoryName4, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    # tweets = []
    # #only appending new stuff, thus open new json file
    # jsonFileToBeOpened = directoryName2
    # for line in open(jsonFileToBeOpened, 'r'):
    #     tweets.append(json.loads(line))

    # uniqueTweets = { each['id'] : each for each in tweets }.values()
    for newLine in newTweets:
        tweets2.append(newLine)

    uniqueTweets2 = { each['id'] : each for each in tweets2 }.values()

    with open(directoryName2, 'w') as f2:

        for line in uniqueTweets2:
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

def twitterFunctionAllCSK():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
   
    userArr = ["FoodIng1st", "FoodNavigator", "DairyReporter", "BakeryAndSnacks", "Boerderij_nl"]
    fname = "@CSKallTwitter" + ".json"
    fname2 = "@CSKallTwitter" + ".json"

    directoryName = os.path.join(scrapeDate,fname)
    directoryName2 = os.path.join("allTime",fname2)

    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

    client = get_twitter_client()

    tweetsAccounts = []

    for user in userArr:
        print("scraping {}".format(user))
        twitterFunction(user)
        fnameNew = "@" + user + ".json"
        directoryNameNew = os.path.join("allTime",fnameNew)
        os.makedirs(os.path.dirname(directoryNameNew), exist_ok=True)

        jsonFileToBeOpened = directoryNameNew
        for line in open(jsonFileToBeOpened, 'r'):
            tweetsAccounts.append(json.loads(line))

    with open(directoryName, 'w') as f:
        for line in tweetsAccounts:
            f.write(json.dumps(line)+"\n")

    tweets = []

    jsonFileToBeOpened = directoryName

    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    uniqueTweets = { each['id'] : each for each in tweets }.values()

    tweets2 = []
    #only appending new stuff, thus open new json file
    try:
        jsonFileToBeOpened = directoryName2
        for line2 in open(jsonFileToBeOpened, 'r'):
            tweets2.append(json.loads(line2))
    except:
        print("no all time tweets yet")

    uniqueTweets2 = { each['id'] : each for each in tweets2 }.values()

    newTweets = []
    for line in uniqueTweets:
        checkVar = False
        for line2 in uniqueTweets2:
            if line.get('id') == line2.get('id'):
                checkVar = True
        if checkVar:
            continue
        else:
            newTweets.append(line)

    handleSuf = "@CSKallTwitter" + ".csv"
    directoryName3 = os.path.join(scrapeDate,handleSuf)
    os.makedirs(os.path.dirname(directoryName3), exist_ok=True)

    csv_out = open(directoryName3, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    for line in newTweets:
        # print(line)
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
    
    with open(directoryName, 'w') as f:
        for line in newTweets:
            f.write(json.dumps(line)+"\n")

    handleSuf = "@CSKallTwitter" + ".csv"
    directoryName4 = os.path.join("allTime",handleSuf)
    os.makedirs(os.path.dirname(directoryName4), exist_ok=True)
    csv_out = open(directoryName4, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    # tweets = []
    # #only appending new stuff, thus open new json file
    # jsonFileToBeOpened = directoryName2
    # for line in open(jsonFileToBeOpened, 'r'):
    #     tweets.append(json.loads(line))

    # uniqueTweets = { each['id'] : each for each in tweets }.values()
    for newLine in newTweets:
        tweets2.append(newLine)

    uniqueTweets2 = { each['id'] : each for each in tweets2 }.values()

    with open(directoryName2, 'w') as f2:

        for line in uniqueTweets2:
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
