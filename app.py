from flask import Flask, render_template
from functions import *

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

@app.route("/ranscraper1/", methods=['POST'])
def move_forward1():
    #Moving forward code
    scrape_run()
    forward_message = "Running Scraper 1..."
    return render_template('scraper.html');

@app.route("/ranscraper2/", methods=['POST'])
def move_forward2():
    #Moving forward code
    forward_message = "Running Scraper 2..."
    return render_template('scraper.html');
@app.route("/ranscraper3/", methods=['POST'])
def move_forward3():
    #Moving forward code
    forward_message = "Running Scraper 3..."
    return render_template('scraper.html');

@app.route("/ranscraper4/", methods=['POST'])
def move_forward4():
    #Moving forward code
    forward_message = "Running Scraper 4..."
    return render_template('scraper.html');



@app.route("/runfilter/", methods=['POST'])
def move_forward5():
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