import os, datetime, re, hashlib
import requests

import csv
from datetime import datetime
from bs4 import BeautifulSoup
import json

import sys
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor

def get_twitter_auth():
    #setup twitter authentication
    #return: tweepy.OAuthHandler object

    try:
        
    except KeyError:
        sys.stderr.write("TWITTER_* env vars not set\n")
        sys.exit(1)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def get_twitter_client():
    #setup twitter API client
    #return tweepy.API object
    auth = get_twitter_auth()
    client = API(auth)
    return client

def jsonToCSV1(name):
    chooseName = name
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Title', 'URL', 'Text', 'Publication Date', 'Source'] #field names
    writer.writerow(fields) #writes field
    csv_out.close()
    return

def jsonToCSV(name, line):
    chooseName = name
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    urlvar = line.get('url')
    writer.writerow([line.get('title'),urlvar,line.get('text').encode('unicode_escape'),line.get('publication date'),line.get('source')])
    csv_out.close()
    return

def acm_scrape_run():
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
    docs, urls = scrape_acm(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsACM' + scrapeDate + '.json'
        output_file = open(fileScrapeResults,'a')
        jsonToCSV1('acm' + scrapeDate)
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            jsonToCSV('acm' + scrapeDate, x)

        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_acm(previousUrls):
    
    def LinkExtractor(content):
        newssoup = BeautifulSoup(content, 'html.parser')
        links = []
        dataBoxChildren = newssoup.find_all("a", attrs={"class":"underlined"})
        for link in dataBoxChildren:
            links.append('https://www.acm.nl'+link.get('href'))
            
        return links
    
    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    documents = []
    linksArr = []

    #Scrape contents of newspage and extract all URLs of complete articles
    for x in range(2):
        print(x)
        if (x == 0):
            r = requests.get('https://www.acm.nl/nl/publicaties/zoeken-in-publicaties?datasource=entity%3Anode&publication_type=1&text=&date%5B0%5D=&date%5B1%5D=&field_subjects=All&field_keywords_single=&sort_by=combined_date&page=0')
        else:
            r = requests.get('https://www.acm.nl/nl/publicaties/zoeken-in-publicaties?datasource=entity%3Anode&publication_type=1&text=&date%5B0%5D=&date%5B1%5D=&field_subjects=All&field_keywords_single=&sort_by=combined_date&page=0{}'.format(str(x)))

        allLinks = LinkExtractor(r.content)

        allLinks = [link for link in allLinks if link not in previousUrls]
        #For each URL, scrape the full artcle, store in dict and append to list of dicts
        if len(allLinks) != 0:
            for link in allLinks:
                print(link)
                try:
                    r = requests.get(link)
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("h1")#, attrs={"itemprop":"headline"})
                    dateTime = articlesoup.find("span", attrs={"class":"date date-fix"})
                    bodyText = articlesoup.find("div", attrs={"class":"text--paragraph editable--colors no-padding"})


                    dict = {}
                    dict['title'] = header.text
                    dict['url'] = link
                    dict['publication date'] = dateTime.text
                    dict['source'] = 'ACM'
                    dict['text'] = bodyText.text
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")
                    
    return documents, linksArr

def bakkers_scrape_run():# https://www.bakkersinbedrijf.nl/nieuws?bib_nieuwspagina-page=1
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')
    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))
    currentUrls = []
    documents = []
    docs, urls = scrape_bakkersinbedrijf(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsBakkers' + scrapeDate + '.json'
        output_file = open(fileScrapeResults,'a')
        jsonToCSV1('bakkers' + scrapeDate)
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            jsonToCSV('bakkers' + scrapeDate, x)

        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_bakkersinbedrijf(previousUrls): 
    
    def LinkExtractor(content):
        newssoup = BeautifulSoup(content, 'html.parser')
        linksContent = []
        titles = newssoup.find_all("h2")
        for link in titles:
            # print(link)
            linksContent.append('https://www.bakkersinbedrijf.nl'+ link.a.get('href'))
        return linksContent
    
    documents = []
    linksArr = []
    
    for x in range(1,5):
        print(x)
        r = requests.get('https://www.bakkersinbedrijf.nl/nieuws?bib_nieuwspagina-page={}'.format(str(x)))
        allLinks = LinkExtractor(r.content)
        allLinks = [link for link in allLinks if link not in previousUrls]
        if len(allLinks) != 0:
            for link in allLinks:
                print(link)
                try:
                    r = requests.get(link)

                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("h1", attrs={"class":"title-half-line"})

                    title = header.text
                    # print(title)
                    data = articlesoup.find("span", attrs={"class":"data"})
                    dateTime = data.text
                    # print(dateTime[25:40])

                    textData = articlesoup.find_all("p")
                    
                    articleText = ''

                    for texts in textData:
                        articleText = articleText + texts.text

                    dict = {}
                    dict['title'] = title
                    dict['url'] = link
                    dict['publication date'] = dateTime
                    dict['source'] = 'bakkersinbedrijf'
                    dict['text'] = articleText
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")                
    return documents, linksArr

def bakkerswereld_scrape_run():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')

    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    currentUrls = []
    documents = []


    docs, urls = scrape_bakkerswereld(previousUrls)
    documents += docs
    currentUrls += urls


    if len(currentUrls) !=0:
        
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsBakkerswereld' + scrapeDate + '.json'
        output_file = open(fileScrapeResults,'a')
        jsonToCSV1('bakkerswereld' + scrapeDate)
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            jsonToCSV('bakkerswereld' + scrapeDate, x)
                
        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_bakkerswereld(previousUrls):
    def LinkExtractor(content):
        newssoup = BeautifulSoup(content, 'html.parser')
        links = []
        dataBoxChildren = newssoup.find_all("h3", attrs={"class":"h5"})

        for link in dataBoxChildren:
            # print(link)
            try:
                link.a.get('href')
                links.append("https://www.bakkerswereld.nl"+link.a.get("href"))
            except:
                # print(link)
                print("\ndoesnt have a link")
            # print(links)
        return links

    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    documents = []
    linksArr = []
    for x in range(5):
        print(x)
        if (x == 0):
            r = requests.get('https://www.bakkerswereld.nl/nieuws')
        else:
            r = requests.get('https://www.bakkerswereld.nl/paginated?category=2&content_type=news_article&excludes=11247%2C11246%2C11248%2C11245%2C11244%2C11110%2C11243%2C11242%2C11241%2C11240%2C11239%2C11238%2C11236%2C11235%2C11234%2C11232%2C11231%2C11230%2C11229%2C11228&paginated_page={}'.format(str(x)))
        
        allLinks = LinkExtractor(r.content)
        allLinks = [link for link in allLinks if link not in previousUrls]
        
        if len(allLinks) != 0:
            for link in allLinks:
                try:
                    r = requests.get(link)
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("div", attrs={"class":"title"})
                    title = header.h1.text
                    textField = articlesoup.find("div", attrs={"class": "article contain"})
                    timeField = articlesoup.find("div", attrs={"id": "content"})
                    dateTime = timeField.time.get('datetime')   
                    
                    dict = {}
                    dict['title'] = title
                    dict['url'] = link
                    dict['publication date'] = dateTime[:10]
                    dict['source'] = 'bakkerswereld'
                    dict['text'] = textField.text
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")
                
    return documents, linksArr

def ceres_scrape_run():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')


    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    currentUrls = []
    documents = []


    docs, urls = scrape_ceres(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsCeres' + scrapeDate + '.json'
        output_file = open(fileScrapeResults,'a')
        jsonToCSV1('ceres' + scrapeDate)
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            jsonToCSV('ceres' + scrapeDate, x)
                
        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')

def scrape_ceres(previousUrls):

    def LinkExtractor(content):

        newssoup = BeautifulSoup(content, 'html.parser')
        linksContent = []
        dataBoxChildren = newssoup.find_all("a", attrs={"class":"newsitem"})

        for link in dataBoxChildren:
            linkWithDate = []

            date = (link.find('span', attrs={'class':'datum'})).text
            linkWithDate.append(date)
            linkWithDate.append('https://www.ceres.be'+link.get('href'))
            linksContent.append(linkWithDate)
        return linksContent
    # math.help
    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    documents = []
    linksArr = []
    tempLinkDict = []
    tempLinks = []
    tempLinkDate = []
            

    r  = requests.get('https://www.ceres.be/nl/nieuws')

    allLinks = LinkExtractor(r.content)
    
    for link in allLinks:
        if link[1] not in previousUrls:
            tempLinkDict.append(link)

    allLinks = tempLinkDict

    # print(allLinks)
    #For each URL, scrape the full artcle, store in dict and append to list of dicts
    if len(allLinks) != 0:

        for link in allLinks:
            print(link[1])
            try:
                r = requests.get(link[1])
                articlesoup = BeautifulSoup(r.content, 'html.parser')
                header = articlesoup.find("div", attrs={"class":"newsarticle"})
                title = header.find('h1')
                bodyText = articlesoup.find("div", attrs={"class":"article-beschr"})


                dict = {}
                dict['title'] = title.text
                dict['url'] = link[1]
                dict['publication date'] = link[0]
                dict['source'] = 'Ceres'
                dict['text'] = bodyText.text
                dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                documents.append(dict)
                linksArr.append(link[1])
    #             print(dict)
            except:
                print('This link was not scraped:\n', link)
    else:
        print("no new links")
                
    return documents, linksArr

def dossche_scrape_run():

    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')


    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    currentUrls = []
    documents = []


    docs, urls = scrape_dossche(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsDossche' + scrapeDate +'.json'
        output_file = open(fileScrapeResults,'a')
        jsonToCSV1('dossche' + scrapeDate)
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            jsonToCSV('dossche' + scrapeDate, x)
                
        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_dossche(previousUrls):
    def LinkExtractor(content):
        newssoup = BeautifulSoup(content, 'html.parser')
        linksContent = []
        dataBoxChildren = newssoup.find_all("div", attrs={"class":"subpage has-image"})

        for link in dataBoxChildren:
            linkWithDate = []
            date = (link.find("span", attrs={"class":"date"})).text
            linkWithDate.append(date)
            titleData = link.find("h3")
            linkWithDate.append("https://www.dosschemills.com" + titleData.a.get('href'))
            linksContent.append(linkWithDate)
        return linksContent

    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    documents = []
    linksArr = []

    #Scrape contents of newspage and extract all URLs of complete articles
    for x in range(5):
        tempLinkDict = []
        tempLinks = []
        tempLinkDate = []
        print(x)
        r = requests.get('https://www.dosschemills.com/nl/over-maalderij-dossche-mills/dossche-news?page={}'.format(str(x)))
        allLinks = LinkExtractor(r.content)
        #Remove URLs that are in the list previousUrls (whch have been scraped before)
        for link in allLinks:
            if link[1] not in previousUrls:
                tempLinkDict.append(link)
                tempLinks.append(link[1])
                tempLinkDate.append(link[0])

        allLinks = tempLinkDict
        titles = []
        if len(allLinks) != 0:
            for link in allLinks:
                try:
                    r = requests.get(link[1])
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("span", attrs={"property":"dc:title"})
                    title = header.get('content')

                    textField = articlesoup.find("div", attrs={"class": "field-item even"})

                    dict = {}
                    dict['title'] = title
                    dict['url'] = link[1]
                    dict['publication date'] = link[0]
                    dict['source'] = 'dosschemills'
                    dict['text'] = textField.text
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link[1])
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")
                
    return documents, linksArr

def soufflet_scrape_run():

    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')

    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    currentUrls = []
    documents = []


    docs, urls = scrape_soufflet(previousUrls)
    documents += docs
    currentUrls += urls


    if len(currentUrls) !=0:
        
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsSoufflet' + scrapeDate + '.json'
        output_file = open(fileScrapeResults,'a')
        jsonToCSV1('soufflet' + scrapeDate)
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            jsonToCSV('soufflet' + scrapeDate, x)
                
        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True

def scrape_soufflet(previousUrls):
    def LinkExtractor(content):

        newssoup = BeautifulSoup(content, 'html.parser')
        links= []
        dataBoxChildren = newssoup.find_all("h5")#, attrs={"class":"newsitem"})

        for link in dataBoxChildren:
            links.append('https://www.soufflet.com' + link.a.get('href'))
        return links

    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    documents = []
    linksArr = []
            

    #Scrape contents of newspage and extract all URLs of complete articles
    for x in range(3):
        print(x)
        r  = requests.get('https://www.soufflet.com/fr/recherche?s=&f%5B0%5D=content_type%3Anews&page={}'.format(str(x)))
        allLinks = LinkExtractor(r.content)

        allLinks = [link for link in allLinks if link not in previousUrls]
        #For each URL, scrape the full artcle, store in dict and append to list of dicts
        if len(allLinks) != 0:

            for link in allLinks:
                print(link)
                try:
                    r = requests.get(link)
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
                    header = articlesoup.find("div", attrs={"class":"content-actu col-12 col-lg-9"})
                    titleData = header.find('h1')#.get('h1').text)
                    dateTimeData = header.find("div", attrs={"class":"date"})
                    dateTimeData2 = " ".join(dateTimeData.text.split())
                    dateTimeData3 = dateTimeData2[:-6] + dateTimeData2[-4:]

                    bodyText = articlesoup.find("div", attrs={"class":"content mt-5"})

                    dict = {}
                    dict['title'] = titleData.text
                    dict['url'] = link
                    dict['publication date'] = dateTimeData3
                    dict['source'] = 'Soufflet'
                    dict['text'] = bodyText.text
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")
                
    return documents, linksArr

def tijd_scrape_run():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')


    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    currentUrls = []
    documents = []


    docs, urls = scrape_tijd(previousUrls)
    documents += docs
    currentUrls += urls

    if len(currentUrls) !=0:
        
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'ResultsTijd' + scrapeDate + '.json'
        output_file = open(fileScrapeResults,'a')
        jsonToCSV1('tijd' + scrapeDate)
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            jsonToCSV('tijd' + scrapeDate, x)
                
        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLog.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')

def scrape_tijd(previousUrls):
        
    def LinkExtractor(content):
        newssoup = BeautifulSoup(content, 'html.parser')
        links = []
        dataBoxChildren = newssoup.find_all("a", attrs={"class":"c-articleteaser__link"})
        for link in dataBoxChildren:
            links.append("https://www.tijd.be"+link.get('href'))
        return links
    previousUrls = []
    with open('ScrapeLog.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))

    documents = []
    linksArr = []

    r = requests.get('https://www.tijd.be/meest-recent.html')

    allLinks = LinkExtractor(r.content)
    allLinks = [link for link in allLinks if link not in previousUrls]
    #For each URL, scrape the full artcle, store in dict and append to list of dicts
    if len(allLinks) != 0:
        for link in allLinks:
            try:
                r = requests.get(link)
                articlesoup = BeautifulSoup(r.content, 'html.parser')
                header = articlesoup.find("h1", attrs={"itemprop":"headline"})
                dateTime = articlesoup.find("time", attrs={"itemprop":"datePublished"})
                dateTime = dateTime.get("datetime")
                bodyText = articlesoup.find("div", attrs={"itemprop":"articleBody"})

                dict = {}
                dict['title'] = header.text
                dict['url'] = link
                dict['publication date'] = dateTime[:10]
                dict['source'] = 'tijd'
                dict['text'] = bodyText.text
                dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                documents.append(dict)
                linksArr.append(link)
            except:
                print('This link was not scraped:\n', link)
    else:
        print("no new links")
            
    return documents, linksArr

def allFunctionsRan():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    
    data = []
    try:
        fileScrapeResults = 'ResultsACM' + scrapeDate + '.json'
        with open(fileScrapeResults) as f:
            for line in f:
                data.append(json.loads(line))
    except:
        print("no new ACM results")

    try:
        fileScrapeResults = 'ResultsBakkers' + scrapeDate + '.json'
        with open(fileScrapeResults) as f:
            for line in f:
                data.append(json.loads(line))
    except:
        print("no new Bakkers results")

    try:
        fileScrapeResults = 'ResultsBakkerswereld' + scrapeDate + '.json'
        with open(fileScrapeResults) as f:
            for line in f:
                data.append(json.loads(line))
    except:
        print("no new Bakkerswereld results")

    try:
        fileScrapeResults = 'ResultsCeres' + scrapeDate + '.json'
        with open(fileScrapeResults) as f:
            for line in f:
                data.append(json.loads(line))
    except:
        print("no new Ceres results")

    try:
        fileScrapeResults = 'ResultsDossche' + scrapeDate + '.json'
        with open(fileScrapeResults) as f:
            for line in f:
                data.append(json.loads(line))
    except:
        print("no new Dossche results")

    try:
        fileScrapeResults = 'ResultsSoufflet' + scrapeDate + '.json'
        with open(fileScrapeResults) as f:
            for line in f:
                data.append(json.loads(line))
    except:
        print("no new Soufflet results")

    try:
        fileScrapeResults = 'ResultsTijd' + scrapeDate + '.json'
        with open(fileScrapeResults) as f:
            for line in f:
                data.append(json.loads(line))
    except:
        print("no new Tijd results")
    

    jsonToCSV1('All' + scrapeDate)
    for x in data:
        jsonToCSV('ALL' + scrapeDate, x)

def twitterFunction(handle):
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    # userArr = ["bakkerswereldnl", "BakkersinB", "BakkerijCentrum", "BakeryNext", "dossche_mills", "GroupeSoufflet"]
    fname = handle + scrapeDate + ".json"
    client = get_twitter_client()

    print("scraping {}".format(handle))
    with open(fname, 'a') as f:
        for page in Cursor(client.user_timeline, screen_name=handle, count=200).pages(2):
            for status in page:
                f.write(json.dumps(status._json)+"\n")

    chooseName = handle + scrapeDate
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = fname
    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    for line in tweets:
        
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
    fname = "AllTwitter" + scrapeDate + ".json"
    client = get_twitter_client()

    for user in userArr:
        print("scraping {}".format(user))
        with open(fname, 'a') as f:
            for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(2):
                for status in page:
                    f.write(json.dumps(status._json)+"\n")

    chooseName = "AllTwitter" + scrapeDate
    csvFileName = "{}.csv".format(chooseName)
    csv_out = open(csvFileName, mode='a') #opens csv file
    writer = csv.writer(csv_out) #create the csv writer object

    fields = ['Twitter Handle & User Name', 'Tweet', ' external URL', 'Hashtags', 'Date of Tweet', 'Followers', 'Following', 'RT', 'FAV'] #field names
    writer.writerow(fields) #writes field

    tweets = []

    jsonFileToBeOpened = fname
    for line in open(jsonFileToBeOpened, 'r'):
        tweets.append(json.loads(line))

    for line in tweets:
        
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
