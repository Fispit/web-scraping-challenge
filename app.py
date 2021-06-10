from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsDB")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_data = scrape_mars.scrape()
    mongo.db.marsdata.update({}, mars_data, upsert=True)

    # Find one record of data from the mongo database
    mars_info = mongo.db.marsdata.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_info)




if __name__ == "__main__":
    app.run(debug=True)
