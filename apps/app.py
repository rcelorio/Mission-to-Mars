

#import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#setup flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   #return "Scraping Successful!"
   return index()

@app.route("/hemi")
def hemi():
   mars = mongo.db.mars.find_one()
   return render_template("hemi.html", mars=mars)

# run the app from the command line
if __name__ == "__main__":
   app.run()