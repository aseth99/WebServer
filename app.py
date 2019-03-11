from flask import Flask, render_template
from functions import *
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

#run the twitter keys so we can run twitter scrapers
@app.route("/syncTwitterKeys/", methods=['POST'])
def osFunction():
	os.system('./ClickHereTwitter.sh')
	return render_template('scraper.html');


# running scrapers......
@app.route("/ranACMscraper1/", methods=['POST'])
def move_forward1():
    #Moving forward code
    acm_scrape_run()
    forward_message = "Running Scraper 1..."
    return render_template('scraper.html');

@app.route("/ranBAKKERSscraper2/", methods=['POST'])
def move_forward2():
    #Moving forward code
    bakkers_scrape_run()
    forward_message = "Running Scraper 2..."
    return render_template('scraper.html');

@app.route("/ranBAKKERSWERELDscraper3/", methods=['POST'])
def move_forward3():
    #Moving forward code
    bakkerswereld_scrape_run()
    forward_message = "Running Scraper 3..."
    return render_template('scraper.html');

@app.route("/ranCERESscraper4/", methods=['POST'])
def move_forward4():
    #Moving forward code
    ceres_scrape_run()
    forward_message = "Running Scraper 4..."
    return render_template('scraper.html');

@app.route("/ranDOSSCHEscraper5/", methods=['POST'])
def move_forward5():
    #Moving forward code
    dossche_scrape_run()
    forward_message = "Running Scraper 5..."
    return render_template('scraper.html');

@app.route("/ranSOUFFLETscraper6/", methods=['POST'])
def move_forward6():
    #Moving forward code
    soufflet_scrape_run()
    forward_message = "Running Scraper 6..."
    return render_template('scraper.html');

@app.route("/ranTIJDscraper7/", methods=['POST'])
def move_forward7():
    #Moving forward code
    tijd_scrape_run()
    forward_message = "Running Scraper 7..."
    return render_template('scraper.html');


@app.route("/ranALLscrapers/", methods=['POST'])
def move_forward8():
    #Moving forward code
    acm_scrape_run()
    bakkers_scrape_run()
    bakkerswereld_scrape_run()
    ceres_scrape_run()
    dossche_scrape_run()
    soufflet_scrape_run()
    tijd_scrape_run()
    allFunctionsRan()
    forward_message = "Running Scraper 7..."
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



@app.route("/runfilter/", methods=['POST'])
def move_forward10():
    #Moving forward code
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