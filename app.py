from flask import Flask, render_template, request, flash
from functions_KKM import *
from functions_twitter import *
from functions_twitter_filter import *
from functions_web_filter import *
import os
import tablib


app = Flask(__name__)
app.secret_key = 'random string'

dataset = tablib.Dataset()


#filter functions

@app.route("/filter", methods=['POST'])
def filterFunction():
	#filter form for webscrapers was filled out
	if request.form['filterbtn'] == 'webFilterBtn':
		websiteFunction = "testing"

		if(request.form.get('andOr')):
			andVar = True
		else:
			andVar = False 

		# if(request.form.get('todayAllTime')):
		# 	#true means theyve turned it to all time
		# 	todayVar = False
		# else:
		# 	todayVar = True 

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
			numLines, csvFileName, header, rows = webFilterFunction(andVar, todayVar, sourceVar, words)

			return render_template('handleFilterResult.html', account=sourceVar, words=words, numLines=numLines, csvFileName = csvFileName, header=header, rows=rows)


	#filter form for twitter filled out
	else:
		if(request.form.get('andOr')):
			andVar = True
		else:
			andVar = False 

		if(request.form.get('dateS')):
			if(request.form.get('dateE')):
				startDate = request.form.get('dateS')
				endDate = request.form.get('dateE')
				filterDate = True
			else:
				filterDate = False
		else:
			filterDate = False

		# if(request.form.get('todayAllTime')):
		# 	todayVar = False
		# else:
		# 	todayVar = True 

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
		
		elif request.form['filterbtn'] == 'KKM':
			error = "hehe wassup"
			return render_template('testing.html', error = error)
		

		elif request.form['filterbtn'] == 'CSK':
			error = "hehe wassup"
			flash("heheheh")
			return render_template('testing.html', error = error)

	return render_template('filter.html')



@app.route("/runfilter/", methods=['POST'])
def move_forward10():
	forward_message = "Running Filter..."
	return render_template('filter.html');



@app.route("/handleFilterResult")
def handleFilterResult():
	return render_template('handleFilterResult.html')

@app.route("/handleFilterResult", methods=['POST'])
def deleteBtnFilter():
	# deleteFunction()
	varTextFileName = request.form['deleteBtn']
	deleteFile(varTextFileName)
	return render_template('handleFilterResult.html', deletedFile=varTextFileName)


#TWITTER
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

#for manually typing a twitter handle
@app.route('/handle_data', methods=['POST'])
def handle_data():
	projectpath = request.form['projectFilepath']

	twitterFunction(str(projectpath))
	return render_template('scraper.html')

@app.route("/ranscraper2/", methods=['POST'])
def twitter79():
	return render_template('scraper.html');



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
	# scrape_run()
	return render_template('scraper.html')

@app.route("/filter")
def filter():
	return render_template('filter.html')

@app.route("/testing")
def testing():
	# scrape_run()
	return render_template('testing.html')

# scraper functions...
@app.route("/ranACMscraper1/", methods=['POST'])
def move_forward1():
	try:
		acm_scrape_run()
	except:
		print("acm scraper is broken")
	return render_template('scraper.html');

@app.route("/ranBAKKERSscraper2/", methods=['POST'])
def move_forward2():
	try:
		bakkers_scrape_run()
	except:
		print("bakkers scraper is broken")
	return render_template('scraper.html');

@app.route("/ranBAKKERSWERELDscraper3/", methods=['POST'])
def move_forward3():
	try:
		bakkerswereld_scrape_run()
	except:
		print("bakkerswereld scraper is broken")
	return render_template('scraper.html');

@app.route("/ranCERESscraper4/", methods=['POST'])
def move_forward4():
	try:
		ceres_scrape_run()
	except:
		print("ceres scraper is broken")
	return render_template('scraper.html');

@app.route("/ranDOSSCHEscraper5/", methods=['POST'])
def move_forward5():
	try:
		dossche_scrape_run()
	except:
		print("dossche scraper is broken")
	return render_template('scraper.html');

@app.route("/ranSOUFFLETscraper6/", methods=['POST'])
def move_forward6():
	try:
		soufflet_scrape_run()
	except:
		print("soufflet scraper is broken")
	return render_template('scraper.html');

@app.route("/ranTIJDscraper7/", methods=['POST'])
def move_forward7():
	try:
		tijd_scrape_run()
	except:
		print("tijd scraper is broken")
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
		allFunctionsRan()
	except:
		print("something is broken")
	
	return render_template('scraper.html');


@app.route("/test")
def test():
	return render_template('indexOld.html')

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)