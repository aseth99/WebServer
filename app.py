#!/usr/bin/env python3
from flask import Flask, render_template, request, flash
from functions_KKM import *
from functions_CSK import *
from functions_twitter import *
from functions_twitter_filter import *
from functions_web_filter import *
import os
import tablib


app = Flask(__name__)
app.secret_key = 'random string'

dataset = tablib.Dataset()


#filter function: checks if its web or twitter filter, extracts keywords, source, date, and and/or 
#and feeds correct inputs to correct filter functions
@app.route("/filter", methods=['POST'])
def filterFunction():
	#filter form for webscrapers was filled out
	if request.form['filterbtn'] == 'webFilterBtn':
		websiteFunction = "testing"

		if(request.form.get('andOr')):
			andVar = True
		else:
			andVar = False 

		if(request.form.get('dateS')):

			if(request.form.get('dateE')):
				startDate = request.form.get('dateS')
				startDate = startDate[2:4]+startDate[5:7]+startDate[8:]
				endDate = request.form.get('dateE')
				endDate = endDate[2:4]+endDate[5:7]+endDate[8:]
				filterDate = True
			else:
				filterDate = False
		else:
			filterDate = False


		words = []	
		word1 = request.form['keyword5']
		if word1 != '':
			words.append(word1)

		word2 = request.form['keyword6']
		if word2 != '':
			words.append(word2)
		word3 = request.form['keyword7']
		if word3 != '':
			words.append(word3)
		word4 = request.form['keyword8']
		if word4 != '':
			words.append(word4)

		if not words:
			
			flash("no words specified (webscraper)!! no filter ran", "error")
			return render_template('filter.html', websiteFunction=websiteFunction)

		if request.form['source'] == 'none':
			flash("no source specified (webscraper)!! no filter ran", "error")
			return render_template('filter.html', websiteFunction=websiteFunction)

		else:
			sourceVar = request.form['source']

			if(filterDate):
				numLines, csvFileName, header, rows = webFilterFunctionWithDate(andVar, sourceVar, words, startDate, endDate)
			else:
				numLines, csvFileName, header, rows = webFilterFunction(andVar, sourceVar, words)

			return render_template('handleFilterResult.html', account=sourceVar, words=words, numLines=numLines, csvFileName = csvFileName, header=header, rows=rows)

	#filter form for twitter filled out
	else:
		if(request.form.get('andOr')):
			andVar = True
		else:
			andVar = False 

		if(request.form.get('dateS')):
			# print(request.form.get('dateS'))
			if(request.form.get('dateE')):
				startDate = request.form.get('dateS')
				startDate = startDate[2:4]+startDate[5:7]+startDate[8:]
				endDate = request.form.get('dateE')
				endDate = endDate[2:4]+endDate[5:7]+endDate[8:]
				filterDate = True
			else:
				filterDate = False
		else:
			filterDate = False

		words = []	
		word1 = request.form['keyword1']
		if word1 != '':
			words.append(word1)
		word2 = request.form['keyword2']
		if word2 != '':
			words.append(word2)
		word3 = request.form['keyword3']
		if word3 != '':
			words.append(word3)
		word4 = request.form['keyword4']
		if word4 != '':
			words.append(word4)

		if not words:
			
			flash("no words specified (twitter)!! no filter ran", "error")
			return render_template('filter.html')
		
		if request.form['filterbtn'] == 'input':
			account = request.form['projectFilepath']
			
			if account == '':
				flash("please input a twitter handle that you've previously scraped", "error")
				return render_template('filter.html')

			if(filterDate):
				numLines, csvFileName, header, rows = handleFilterWithDate(account, words, andVar, startDate, endDate)
			else:
				numLines, csvFileName, header, rows = handleFilter(account, words, andVar)

			return render_template('handleFilterResult.html', account=account, words=words, numLines=numLines, csvFileName = csvFileName, header=header, rows=rows)
		
		elif request.form['filterbtn'] == 'KKMorCSK':
			
			accountGroup = request.form['source']
			if(filterDate):
				numLines, csvFileName, header, rows = handleGroupFilterWithDate(accountGroup, words, andVar, startDate, endDate)
			else:
				numLines, csvFileName, header, rows = handleGroupFilter(accountGroup, words, andVar)

			return render_template('handleFilterResult.html', account=accountGroup, words=words, numLines=numLines, csvFileName = csvFileName, header=header, rows=rows)		

		# elif request.form['filterbtn'] == 'CSK':
		# 	error = "hehe wassup"
		# 	flash("heheheh")
		# 	return render_template('testing.html', error = error)
	flash("huh...")
	return render_template('filter.html')


#main page for handling filter, used input variables from filter functions to convey account name,rows,etc.
@app.route("/handleFilterResult")
def handleFilterResult():
	return render_template('handleFilterResult.html')

#if redirected here, provides delete button functionality
@app.route("/handleFilterResult", methods=['POST'])
def deleteBtnFilter():
	# deleteFunction()
	varTextFileName = request.form['deleteBtn']
	deleteFile(varTextFileName)
	return render_template('handleFilterResult.html', deletedFile=varTextFileName)


#TWITTER functions from buttons
@app.route("/ranTwitter1/", methods=['POST'])
def twitter1():
	twitterFunction("bakkerswereldnl")
	return render_template('scraper.html');

@app.route("/ranTwitter2/", methods=['POST'])
def twitter2():
	twitterFunction("bakkersinb")
	return render_template('scraper.html');
@app.route("/ranTwitter3/", methods=['POST'])
def twitter3():
	twitterFunction("bakkerijcentrum")
	return render_template('scraper.html');
@app.route("/ranTwitter4/", methods=['POST'])
def twitter4():
	twitterFunction("bakerynext")
	return render_template('scraper.html');
@app.route("/ranTwitter5/", methods=['POST'])
def twitter5():
	twitterFunction("dossche_mills")
	return render_template('scraper.html');
@app.route("/ranTwitter6/", methods=['POST'])
def twitter6():
	twitterFunction("groupesoufflet")
	return render_template('scraper.html');
@app.route("/ranTwitter7/", methods=['POST'])
def twitter7():
	twitterFunctionAllKKM()
	return render_template('scraper.html');

@app.route("/ranTwitter8/", methods=['POST'])
def twitter8():
	twitterFunction("FoodIng1st")
	return render_template('scraper.html');

@app.route("/ranTwitter9/", methods=['POST'])
def twitter9():
	twitterFunction("FoodNavigator")
	return render_template('scraper.html');
@app.route("/ranTwitter10/", methods=['POST'])
def twitter10():
	twitterFunction("DairyReporter")
	return render_template('scraper.html');
@app.route("/ranTwitter11/", methods=['POST'])
def twitter11():
	twitterFunction("BakeryAndSnacks")
	return render_template('scraper.html');
@app.route("/ranTwitter12/", methods=['POST'])
def twitter12():
	twitterFunction("Boerderij_nl")
	return render_template('scraper.html');
@app.route("/ranTwitter13/", methods=['POST'])
def twitter13():
	twitterFunctionAllCSK()
	return render_template('scraper.html');

#for manually typing a twitter handle
@app.route('/handle_data', methods=['POST'])
def handle_data():
	projectpath = request.form['projectFilepath']
	twitterFunction(str(projectpath))
	return render_template('scraper.html')


#main page functions
@app.route("/")
def main():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/explain")
def explain():
	return render_template('explain.html')

@app.route("/scraper")
def scraper():
	return render_template('scraper.html')

@app.route("/filter")
def filter():
	return render_template('filter.html')

@app.route("/testing")
def testing():
	# scrape_run()
	return render_template('testing.html')

# scraper functions... each scraper function also funs the all functions ran to append correct info into allKKM/allCSK files
@app.route("/ranACMscraper1/", methods=['POST'])
def move_forward1():
	try:
		acm_scrape_run()
	except:
		print("acm scraper is broken")
	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranBAKKERSscraper2/", methods=['POST'])
def move_forward2():
	try:
		bakkers_scrape_run()
	except:
		print("bakkers scraper is broken")
	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranBAKKERSWERELDscraper3/", methods=['POST'])
def move_forward3():
	try:
		bakkerswereld_scrape_run()
	except:
		print("bakkerswereld scraper is broken")
	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranCERESscraper4/", methods=['POST'])
def move_forward4():
	try:
		ceres_scrape_run()
	except:
		print("ceres scraper is broken")
	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranDOSSCHEscraper5/", methods=['POST'])
def move_forward5():
	try:
		dossche_scrape_run()
	except:
		print("dossche scraper is broken")
	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranSOUFFLETscraper6/", methods=['POST'])
def move_forward6():
	try:
		soufflet_scrape_run()
	except:
		print("soufflet scraper is broken")
	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranTIJDscraper7/", methods=['POST'])
def move_forward7():
	try:
		tijd_scrape_run()
	except:
		print("tijd scraper is broken")
	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');


@app.route("/ranALLscrapers/", methods=['POST'])
def move_forward8():
	try:
		acm_scrape_run()
	except:	
		print("acm scraper is broken")

	try:
		bakkers_scrape_run()
	except:	
		print("bakkers scraper is broken")

	try:
		bakkerswereld_scrape_run()
	except:
		print("bakkerswereld scraper is broken")
	try:
		ceres_scrape_run()
	except:	
		print("ceres scraper is broken")
	try:
		dossche_scrape_run()
	except:	
		print("dossche scraper is broken")
	try:
		soufflet_scrape_run()
	except:	
		print("soufflet scraper is broken")
	try:
		tijd_scrape_run()
	except:	
		print("tijd scraper is broken")

	try:
		allKKMFunctionsRan()
	except:
		print("something is broken")
	
	return render_template('scraper.html');


@app.route("/ranBNSscraper9/", methods=['POST'])
def move_forward9():
	try:
		bns_scrape_run()
	except:
		print("bns scraper is broken")
	try:
		allCSKFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranDRscraper10/", methods=['POST'])
def move_forward10():
	try:
		dr_scrape_run()
	except:
		print("dr scraper is broken")
	try:
		allCSKFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranFNscraper11/", methods=['POST'])
def move_forward11():
	try:
		fn_scrape_run()
	except:
		print("fn scraper is broken")
	try:
		allCSKFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranFIFscraper12/", methods=['POST'])
def move_forward12():
	try:
		fif_scrape_run()
	except:
		print("fif scraper is broken")
	try:
		allCSKFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');

@app.route("/ranFBscraper13/", methods=['POST'])
def move_forward13():
	try:
		foodBev_scrape_run()
	except:
		print("fb scraper is broken")
	try:
		allCSKFunctionsRan()
	except:
		print("something is broken")
	return render_template('scraper.html');


@app.route("/ranALLCSKscrapers/", methods=['POST'])
def move_forward14():
	try:
		bns_scrape_run()
	except:
		print("bns scraper is broken")

	try:
		dr_scrape_run()
	except:
		print("dr scraper is broken")

	try:
		fn_scrape_run()
	except:
		print("fn scraper is broken")

	try:
		fif_scrape_run()
	except:
		print("fif scraper is broken")

	try:
		foodBev_scrape_run()
	except:
		print("fb scraper is broken")

	try:
		allCSKFunctionsRan()
	except:
		print("something is broken")
	
	return render_template('scraper.html');

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)