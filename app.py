from flask import Flask, render_template, request
from functions_KKM import *
from functions_twitter import *
import os

app = Flask(__name__)

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

# #run the twitter keys so we can run twitter scrapers
# @app.route("/syncTwitterKeys/", methods=['POST'])
# def osFunction():
# 	os.system('./ClickHereTwitter.sh')
# 	return render_template('scraper.html');


# running scrapers......
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
		bakkers_scrape_run()
		bakkerswereld_scrape_run()
		ceres_scrape_run()
		dossche_scrape_run()
		soufflet_scrape_run()
		tijd_scrape_run()
		allFunctionsRan()
	except:
		print("one of the scrapers is broken")
	return render_template('scraper.html');

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
	twitterFunctionAll()
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

@app.route("/runfilter/", methods=['POST'])
def move_forward10():
	forward_message = "Running Filter..."
	return render_template('filter.html');

@app.route("/filter")
def filter():
	return render_template('filter.html')

@app.route("/test")
def test():
	return render_template('indexOld.html')

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)