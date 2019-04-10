import os, datetime, re, hashlib
import requests

import csv
from datetime import datetime
from datetime import date
from bs4 import BeautifulSoup
import json
import sys

#writes into todays csv files, appends to all time 
def jsonToCSV1(name):
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    name = name + ".csv"
    directoryName = os.path.join(scrapeDate,name)
    directoryName2 = os.path.join("allTime",name)

    os.makedirs(os.path.dirname(directoryName), exist_ok=True)
    os.makedirs(os.path.dirname(directoryName2), exist_ok=True)


    csv_out = open(directoryName, mode='w') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object


    fields = ['Title', 'URL', 'Text', 'Publication Date', 'Source'] #field names
    writer.writerow(fields) #writes field
    csv_out.close()

    csv_out = open(directoryName2, mode='w') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Title', 'URL', 'Text', 'Publication Date', 'Source'] #field names
    writer.writerow(fields) #writes field
    csv_out.close()

    return

#appends stuff to csv file, line by line
def jsonToCSV(name, line):
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    name = name + ".csv"
    directoryName = os.path.join(scrapeDate,name)

    os.makedirs(os.path.dirname(directoryName), exist_ok=True)

    csv_out = open(directoryName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    urlvar = line.get('url')
    writer.writerow([line.get('title'),urlvar,line.get('text').encode('unicode_escape'),line.get('publication date'),line.get('source')])
    csv_out.close()

    return

def jsonToCSVallTime(name, line):
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    name = name + ".csv"
    directoryName2 = os.path.join("allTime",name)

    os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

    csv_out = open(directoryName2, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    urlvar = line.get('url')
    writer.writerow([line.get('title'),urlvar,line.get('text').encode('unicode_escape'),line.get('publication date'),line.get('source')])
    csv_out.close()

    return


def bns_scrape_run():
    # https://www.acm.nl/nl/nieuws
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')
    previousUrls = []


    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))
    currentUrls = []
    documents = []
    docs, urls = scrape_bns(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsBNS' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)

        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        
        dataLine = []
        jsonFileToBeOpened = directoryName
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine.append(json.loads(line))
        except:
            print("no bns results file yet today")

        for x in documents:
            dataLine.append(x)

        uniqueLine = { each['articleID'] : each for each in dataLine }.values()

        with open(directoryName, 'w') as f:
            for line in uniqueLine:
                f.write(json.dumps(line)+"\n")


        dataLine2 = []
        jsonFileToBeOpened = directoryName2
        
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine2.append(json.loads(line))
        except:
            print("no dr results file yet allTime")

        for x in documents:
            dataLine2.append(x)

        uniqueLine2 = { each['articleID'] : each for each in dataLine2 }.values()
        
        with open(directoryName2, 'w') as f2:
            for line in uniqueLine2:
                f2.write(json.dumps(line)+"\n")

        jsonToCSV1('bns')
        for x in uniqueLine:
            jsonToCSV('bns', x)
        for y in uniqueLine2:
            jsonToCSVallTime('bns', y)

        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_bns(previousUrls):

    def LinkExtractor(content):
        links = []
        newssoup = BeautifulSoup(content, 'html.parser')
        dataBoxChildren = newssoup.find_all('h3', attrs={'class':'Teaser-title'})
        for link in dataBoxChildren:
            links.append('https://www.bakeryandsnacks.com' + link.a.get('href'))

        return(links)

    documents = []
    linksArr = []

    for x in range(1,11):
        print(x)
        r = requests.get('https://www.bakeryandsnacks.com/Article?page={}'.format(str(x)))

        allLinks = LinkExtractor(r.content)

        allLinks = [link for link in allLinks if link not in previousUrls]

        if len(allLinks) != 0:
            for link in allLinks:
                # print(link)
                try:
                    r = requests.get(link)
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("h1", attrs={"class":"Detail-title"})
                    # print(header.text)

                    dateTimeData = articlesoup.find("p", attrs={"class":"Detail-date"})
                    dateTime = dateTimeData.time.get("datetime")
                    # print(dateTime)

                    bodyTexttest = ''
                    if (articlesoup.find("div", attrs={"class":"Detail-intro"})) is not None:
                        for string in articlesoup.find("div", attrs={"class":"Detail-intro"}).stripped_strings:
                            bodyTexttest += string
                        bodyTexttest += '\n'    
                    for string2 in articlesoup.find("div", attrs={"class":"ezxmltext-field RichText"}).stripped_strings:
                        bodyTexttest += string2
                        bodyTexttest += ' '
                    bodyTexttest = bodyTexttest.replace('googletag.cmd.push(function ()', '')
                    bodyTexttest = bodyTexttest.replace('googletag.display(\'text-ad1\');', '')
                    bodyTexttest = bodyTexttest.replace('});', '')
                    bodyTexttest = bodyTexttest.replace('{\n', '')
                    bodyTexttest = ' '.join(bodyTexttest.split())


                    # print(bodyTexttest)

                    dict = {}
                    dict['title'] = header.text
                    dict['url'] = link
                    dict['publication date'] = dateTime
                    dict['source'] = 'Bakery and Snacks'
                    dict['text'] = bodyTexttest
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")    
    return documents, linksArr


def dr_scrape_run():
    # https://www.acm.nl/nl/nieuws
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')
    previousUrls = []


    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))
    currentUrls = []
    documents = []
    docs, urls = scrape_dr(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsDR' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)

        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        
        dataLine = []
        jsonFileToBeOpened = directoryName
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine.append(json.loads(line))
        except:
            print("no dr results file yet today")

        for x in documents:
            dataLine.append(x)

        uniqueLine = { each['articleID'] : each for each in dataLine }.values()

        with open(directoryName, 'w') as f:
            for line in uniqueLine:
                f.write(json.dumps(line)+"\n")


        dataLine2 = []
        jsonFileToBeOpened = directoryName2
        
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine2.append(json.loads(line))
        except:
            print("no dr results file yet allTime")

        for x in documents:
            dataLine2.append(x)

        uniqueLine2 = { each['articleID'] : each for each in dataLine2 }.values()
        
        with open(directoryName2, 'w') as f2:
            for line in uniqueLine2:
                f2.write(json.dumps(line)+"\n")

        jsonToCSV1('dr')
        for x in uniqueLine:
            jsonToCSV('dr', x)
        for y in uniqueLine2:
            jsonToCSVallTime('dr', y)

        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_dr(previousUrls):

    def LinkExtractor(content):
        links = []
        newssoup = BeautifulSoup(content, 'html.parser')
        dataBoxChildren = newssoup.find_all('h3', attrs={'class':'Teaser-title'})
        for link in dataBoxChildren:
            # print('https://www.dairyreporter.com' + link.a.get('href'))
            links.append('https://www.dairyreporter.com' + link.a.get('href'))

        return(links)

    documents = []
    linksArr = []

    for x in range(1,11):
        print(x)
        r = requests.get('https://www.dairyreporter.com/Article?page={}'.format(str(x)))

        allLinks = LinkExtractor(r.content)

        allLinks = [link for link in allLinks if link not in previousUrls]

        if len(allLinks) != 0:
            for link in allLinks:
                # print(link)
                try:
                    r = requests.get(link)
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("h1", attrs={"class":"Detail-title"})
                    # print(header.text)

                    dateTimeData = articlesoup.find("p", attrs={"class":"Detail-date"})
                    dateTime = dateTimeData.time.get("datetime")
                    # print(dateTime)

                    bodyTexttest = ''
                    if (articlesoup.find("div", attrs={"class":"Detail-intro"})) is not None:
                        for string in articlesoup.find("div", attrs={"class":"Detail-intro"}).stripped_strings:
                            bodyTexttest += string
                        bodyTexttest += '\n'    
                    for string2 in articlesoup.find("div", attrs={"class":"ezxmltext-field RichText"}).stripped_strings:
                        bodyTexttest += string2
                        bodyTexttest += ' '
                    bodyTexttest = bodyTexttest.replace('googletag.cmd.push(function ()', '')
                    bodyTexttest = bodyTexttest.replace('googletag.display(\'text-ad1\');', '')
                    bodyTexttest = bodyTexttest.replace('});', '')
                    bodyTexttest = bodyTexttest.replace('{\n', '')
                    bodyTexttest = ' '.join(bodyTexttest.split())


                    # print(bodyTexttest)

                    dict = {}
                    dict['title'] = header.text
                    dict['url'] = link
                    dict['publication date'] = dateTime
                    dict['source'] = 'Dairy Reporter'
                    dict['text'] = bodyTexttest
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")    
    return documents, linksArr



def fn_scrape_run():
    # https://www.acm.nl/nl/nieuws
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')
    previousUrls = []


    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))
    currentUrls = []
    documents = []
    docs, urls = scrape_fn(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsFN' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)

        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        
        dataLine = []
        jsonFileToBeOpened = directoryName
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine.append(json.loads(line))
        except:
            print("no fn results file yet today")

        for x in documents:
            dataLine.append(x)

        uniqueLine = { each['articleID'] : each for each in dataLine }.values()

        with open(directoryName, 'w') as f:
            for line in uniqueLine:
                f.write(json.dumps(line)+"\n")


        dataLine2 = []
        jsonFileToBeOpened = directoryName2
        
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine2.append(json.loads(line))
        except:
            print("no fn results file yet allTime")

        for x in documents:
            dataLine2.append(x)

        uniqueLine2 = { each['articleID'] : each for each in dataLine2 }.values()
        
        with open(directoryName2, 'w') as f2:
            for line in uniqueLine2:
                f2.write(json.dumps(line)+"\n")

        jsonToCSV1('fn')
        for x in uniqueLine:
            jsonToCSV('fn', x)
        for y in uniqueLine2:
            jsonToCSVallTime('fn', y)

        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_fn(previousUrls):

    def LinkExtractor(content):
        links = []
        newssoup = BeautifulSoup(content, 'html.parser')
        dataBoxChildren = newssoup.find_all('h3', attrs={'class':'Teaser-title'})
        for link in dataBoxChildren:
            # print('https://www.dairyreporter.com' + link.a.get('href'))
            links.append('https://www.foodnavigator.com' + link.a.get('href'))

        return(links)

    documents = []
    linksArr = []

    for x in range(1,11):
        print(x)
        r = requests.get('https://www.foodnavigator.com/Article?page={}'.format(str(x)))

        allLinks = LinkExtractor(r.content)

        allLinks = [link for link in allLinks if link not in previousUrls]

        if len(allLinks) != 0:
            for link in allLinks:
                # print(link)
                try:
                    r = requests.get(link)
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("h1", attrs={"class":"Detail-title"})
                    # print(header.text)

                    dateTimeData = articlesoup.find("p", attrs={"class":"Detail-date"})
                    dateTime = dateTimeData.time.get("datetime")
                    # print(dateTime)

                    bodyTexttest = ''
                    if (articlesoup.find("div", attrs={"class":"Detail-intro"})) is not None:
                        for string in articlesoup.find("div", attrs={"class":"Detail-intro"}).stripped_strings:
                            bodyTexttest += string
                        bodyTexttest += '\n'    
                    for string2 in articlesoup.find("div", attrs={"class":"ezxmltext-field RichText"}).stripped_strings:
                        bodyTexttest += string2
                        bodyTexttest += ' '
                    bodyTexttest = bodyTexttest.replace('googletag.cmd.push(function ()', '')
                    bodyTexttest = bodyTexttest.replace('googletag.display(\'text-ad1\');', '')
                    bodyTexttest = bodyTexttest.replace('});', '')
                    bodyTexttest = bodyTexttest.replace('{\n', '')
                    bodyTexttest = ' '.join(bodyTexttest.split())


                    # print(bodyTexttest)

                    dict = {}
                    dict['title'] = header.text
                    dict['url'] = link
                    dict['publication date'] = dateTime
                    dict['source'] = 'Food Navigator'
                    dict['text'] = bodyTexttest
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")    
    return documents, linksArr



def fif_scrape_run():
    # https://www.acm.nl/nl/nieuws
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')
    previousUrls = []


    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))
    currentUrls = []
    documents = []
    docs, urls = scrape_fif(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsFIF' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)

        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        
        dataLine = []
        jsonFileToBeOpened = directoryName
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine.append(json.loads(line))
        except:
            print("no fif results file yet today")

        for x in documents:
            dataLine.append(x)

        uniqueLine = { each['articleID'] : each for each in dataLine }.values()

        with open(directoryName, 'w') as f:
            for line in uniqueLine:
                f.write(json.dumps(line)+"\n")


        dataLine2 = []
        jsonFileToBeOpened = directoryName2
        
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine2.append(json.loads(line))
        except:
            print("no fif results file yet allTime")

        for x in documents:
            dataLine2.append(x)

        uniqueLine2 = { each['articleID'] : each for each in dataLine2 }.values()
        
        with open(directoryName2, 'w') as f2:
            for line in uniqueLine2:
                f2.write(json.dumps(line)+"\n")

        jsonToCSV1('fif')
        for x in uniqueLine:
            jsonToCSV('fif', x)
        for y in uniqueLine2:
            jsonToCSVallTime('fif', y)
        
        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_fif(previousUrls):

    def LinkExtractor(content):
            links = []
            newssoup = BeautifulSoup(content, 'html.parser')
            dataBoxChildren = newssoup.find_all('a', attrs={'class':'readmorelink'})
            for link in dataBoxChildren:
                # print(link.get('href'))
                links.append(link.get('href'))

            return(links)

    documents = []
    linksArr = []

    r = requests.get('https://www.foodingredientsfirst.com/news.html')

    allLinks = LinkExtractor(r.content)

    allLinks = [link for link in allLinks if link not in previousUrls]
    
    if len(allLinks) != 0:
        for link in allLinks:
            # print(link)
            try:
                r = requests.get(link)
                articlesoup = BeautifulSoup(r.content, 'html.parser')
                header = articlesoup.find("h1", attrs={"class":"article_title"})
                # print(header.text)
                bodyText = ''
                bodyTextStrings = articlesoup.find_all("div", attrs={"class":"textsize imgcontent"})
                for texts in bodyTextStrings:
                    bodyText += texts.text
                # print(bodyText)


                dict = {}
                dict['title'] = header.text[45:-20]
                dict['url'] = link
                dict['publication date'] = bodyText[8:19]
                dict['source'] = 'Food Ingredients First'
                dict['text'] = bodyText[22:]
                dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                documents.append(dict)
                linksArr.append(link)
            except:
                print('This link was not scraped:\n', link)
    else:
        print("no new links")    
    return documents, linksArr



def foodBev_scrape_run():
    # https://www.acm.nl/nl/nieuws
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')
    previousUrls = []


    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))
    currentUrls = []
    documents = []
    docs, urls = scrape_foodBev(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsFB' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)

        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        
        dataLine = []
        jsonFileToBeOpened = directoryName
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine.append(json.loads(line))
        except:
            print("no fb results file yet today")

        for x in documents:
            dataLine.append(x)

        uniqueLine = { each['articleID'] : each for each in dataLine }.values()

        with open(directoryName, 'w') as f:
            for line in uniqueLine:
                f.write(json.dumps(line)+"\n")


        dataLine2 = []
        jsonFileToBeOpened = directoryName2
        
        try:
            for line in open(jsonFileToBeOpened, 'r'):
                dataLine2.append(json.loads(line))
        except:
            print("no fb results file yet allTime")

        for x in documents:
            dataLine2.append(x)

        uniqueLine2 = { each['articleID'] : each for each in dataLine2 }.values()
        
        with open(directoryName2, 'w') as f2:
            for line in uniqueLine2:
                f2.write(json.dumps(line)+"\n")

        jsonToCSV1('fb')
        for x in uniqueLine:
            jsonToCSV('fb', x)
        for y in uniqueLine2:
            jsonToCSVallTime('fb', y)

        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_foodBev(previousUrls):

    def LinkExtractor(content):
        links = []
        newssoup = BeautifulSoup(content, 'html.parser')
        dataBoxChildren = newssoup.find_all('h2')#, attrs={'class':'Teaser-title'})
        for link in dataBoxChildren:
            # print(link.a.get('href'))
            links.append(link.a.get('href'))

        return(links)

    documents = []
    linksArr = []

    for x in range(1,11):
        print(x)
        r = requests.get('https://www.foodbev.com/news/page/{}/'.format(str(x)))

        allLinks = LinkExtractor(r.content)

        allLinks = [link for link in allLinks if link not in previousUrls]

        if len(allLinks) != 0:
            for link in allLinks:
                # print(link)
                try:
                    r = requests.get(link)
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("h1", attrs={"class":"post-tile entry-title"})
                    # print(header.text)
                    dateTimeData = articlesoup.find("time")#, attrs={"class":"Detail-date"})
                    dateTime = dateTimeData.get("datetime")
                    # print(dateTime[:10])
                    bodyText = ""
                    bodyTexttest = articlesoup.find("div", attrs={"class":"entry-content"})
                    allTextFields = bodyTexttest.find_all('p')
                    for texts in allTextFields:
                        bodyText += texts.text + " "
                    # print(bodyText)
                    dict = {}
                    dict['title'] = header.text
                    dict['url'] = link
                    dict['publication date'] = dateTime[:10]
                    dict['source'] = "FoodBev Media"
                    dict['text'] = bodyText
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()

                    documents.append(dict)
                    linksArr.append(link)

                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")    
    return documents, linksArr
   


def allCSKFunctionsRan():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    
    data = []
    dataAllTime = []
    try:
        fileScrapeResults = 'ResultsBNS' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)

        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        try:
            with open(directoryName) as f:
                for line in f:
                    data.append(json.loads(line))
        except:
            print("no bns scraped files today")

        try:
            with open(directoryName2) as f2:
                for line in f2:
                    dataAllTime.append(json.loads(line))
        except:
            print("no bns scraped files all time yet")

    except:
        print("no new BNS results")

    try:
        fileScrapeResults = 'ResultsDR' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)
        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        try:
            with open(directoryName) as f:
                for line in f:
                    data.append(json.loads(line))
        except:
            print("no dr scraped files today")

        try:
            with open(directoryName2) as f2:
                for line in f2:
                    dataAllTime.append(json.loads(line))
        except:
            print("no dr scraped files all time yet")
    except:
        print("no new DR results")

    try:
        fileScrapeResults = 'ResultsFN' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)
        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        try:
            with open(directoryName) as f:
                for line in f:
                    data.append(json.loads(line))
        except:
            print("no fn scraped files today")

        try:
            with open(directoryName2) as f2:
                for line in f2:
                    dataAllTime.append(json.loads(line))
        except:
            print("no fn scraped files all time yet")    
    except:
        print("no new FN results")

    try:
        fileScrapeResults = 'ResultsFIF' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)
        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        try:
            with open(directoryName) as f:
                for line in f:
                    data.append(json.loads(line))
        except:
            print("no fif scraped files today")

        try:
            with open(directoryName2) as f2:
                for line in f2:
                    dataAllTime.append(json.loads(line))
        except:
            print("no fif scraped files all time yet")    
    except:
        print("no new FIF results")

    try:
        fileScrapeResults = 'ResultsFB' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)
        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)

        try:
            with open(directoryName) as f:
                for line in f:
                    data.append(json.loads(line))
        except:
            print("no fb scraped files today")

        try:
            with open(directoryName2) as f2:
                for line in f2:
                    dataAllTime.append(json.loads(line))
        except:
            print("no fb scraped files all time yet")
            
    except:
        print("no new FB results")

    
    try:
        fileScrapeResults = 'ResultsAllCSK' + '.json'
        directoryName = os.path.join(scrapeDate,fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName), exist_ok=True)
        directoryName2 = os.path.join("allTime",fileScrapeResults)
        os.makedirs(os.path.dirname(directoryName2), exist_ok=True)
        print("got here")

        jsonToCSV1('AllCSK')
        print("got here2")

        output_file = open(directoryName,'w')
        
        for x in data:
            jsonToCSV('ALLCSK', x)
            json.dump(x, output_file)
            output_file.write("\n")

        output_file2 = open(directoryName2,'w')
        
        for x in dataAllTime:
            jsonToCSVallTime('ALLCSK', x)
            json.dump(x, output_file2)
            output_file2.write("\n")
    
    except:
        print("somethin wrong")

    return

