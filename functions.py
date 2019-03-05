import os, datetime, re, hashlib
import requests

import csv
from datetime import datetime
from bs4 import BeautifulSoup
import json
# https://www.acm.nl/nl/nieuws

def scrape_run():
    dt = datetime.now()
    scrapeDate = dt.strftime('%y%m%d')
    scrapeTime = dt.strftime('%H%M%S')
    previousUrls = []
    with open('ScrapeLogACM.txt','r', encoding='utf-8') as log:
        for line in log:
            previousUrls.append(line.rstrip('\n'))
    currentUrls = []
    documents = []
    docs, urls = scrape_acm(previousUrls)
    documents += docs
    currentUrls += urls
    # print(documents)
    # print(currentUrls)
    if len(currentUrls) !=0:
        # Write scrape results to file in JSON format as backup for database
        fileScrapeResults = 'acmResults.json'
        output_file = open(fileScrapeResults,'a')
        for x in documents:
            json.dump(x, output_file)
            output_file.write("\n")
            # jsonToCSV('acm', x)
        # Write all urls to log file te check next time which articles have already been scraped
        with open('ScrapeLogACM.txt','a', encoding='utf-8') as log:
            log.write('Scrape Date = ' + scrapeDate + '\n')
            log.write('Scrape Time = ' + scrapeTime + '\n')
            for url in currentUrls:
                log.write(url + '\n')
    return True


def scrape_acm(previousUrls):
    
    def LinkExtractor(content):
        newssoup = BeautifulSoup(content, 'html.parser')
        # print(newssoup)
        links = []
        dataBoxChildren = newssoup.find_all("a", attrs={"class":"underlined"})
        # print(dataBoxChildren)
        for link in dataBoxChildren:
            # print(link)
            # print(link.get('href'))
            print('https://www.acm.nl' + link.get('href'))
            links.append('https://www.acm.nl'+link.get('href'))
            # print(("https://www.tijd.be/"+link.get('href')))
        
        return links
    # <a href="https://www.hln.be/regio/deinze/lionel-beuvens-en-motu-geven-concert-bij-arscene~aa889f93/" class="teaser-link region-lead-teaser__intro-link"> <p data-gtm="artikel-lijst-large/art-2/text" class="teaser-intro region-lead-teaser__intro">  <time class="teaser-publication-time region-lead-teaser__publication-time" datetime="2019-01-31T07:47:36.987Z[UTC]"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">31/01</font></font></time><font style="vertical-align: inherit;"><font style="vertical-align: inherit;"> The vzw Arscene invites Lionel Beuvens and his group MOTU for a concert in Hansbeke on Saturday 2 February. </font></font></p> </a>
    previousUrls = []
    with open('ScrapeLogACM.txt','r', encoding='utf-8') as log:
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
        # print(allLinks)
        # print("those were all the links we think we need to scrape this time")

        # print(previousUrls)
        # print("those are links already scraped all time")

        allLinks = [link for link in allLinks if link not in previousUrls]
        # print(allLinks)
        # print("these should be all the links we actually need to scrape this time")

        #For each URL, scrape the full artcle, store in dict and append to list of dicts
        if len(allLinks) != 0:
            for link in allLinks:
                print(link)
                try:
                    # print("got to here..")
                    r = requests.get(link)
        #                 # print("got to here2..")
                    articlesoup = BeautifulSoup(r.content, 'html.parser')
        #                 # print("got to here3..")
                    header = articlesoup.find("h1")#, attrs={"itemprop":"headline"})
                    # print(header.text)
                    dateTime = articlesoup.find("span", attrs={"class":"date date-fix"})
                    # print(dateTime.text)
                    # dateTime = dateTime.get("datetime")
    # <div class="text--paragraph editable--colors no-padding">
                    bodyText = articlesoup.find("div", attrs={"class":"text--paragraph editable--colors no-padding"})
                    # print(bodyText.text)


                    dict = {}
                    dict['title'] = header.text
                    dict['url'] = link
                    dict['publication date'] = dateTime.text
                    dict['source'] = 'ACM'
                    dict['text'] = bodyText.text
                    dict['articleID'] = hashlib.sha1(dict['title'].encode()).hexdigest()
                    documents.append(dict)
                    linksArr.append(link)
        #             print(dict)
                except:
                    print('This link was not scraped:\n', link)
        else:
            print("no new links")
                    
    return documents, linksArr
