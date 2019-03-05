from flask import Flask, render_template
from functions import scrape_run

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
	scrape_run()
	return render_template('scraper.html')

@app.route("/filter")
def filter():
	return render_template('filter.html')

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)