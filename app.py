from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Creating Flask instance
app = Flask(__name__)

# Establishing Mongo connection with PyMongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_data = mongo.db.mars_data

# Routing to render index.html template using data from Mongo
@app.route("/")
def home():

    # Returning template
    return render_template("index.html")

# Defining route for scrape function
@app.route("/scrape")
def scrape():

    # Running scrape function and saving results
    scraped_data = scrape_mars.scrape()

    # Updating Mongo DB using update and upsert=True
    mars_data.update({}, scraped_data, upsert=True)

    # Redirecting to scraped data page
    return redirect("/data")

# Routing to render data.html template using data from Mongo
@app.route("/data")
def data():

    # Finding one record of data from the Mongo DB
    mars_info = mongo.db.mars_data.find_one()

    # Returning template and data
    return render_template("data.html", info=mars_info)

if __name__ == "__main__":
    app.run(debug=True)