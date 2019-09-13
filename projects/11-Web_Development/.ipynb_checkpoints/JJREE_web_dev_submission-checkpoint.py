# Dependendies
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify, request, url_for, redirect, render_template

#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

# # Save reference to the table
# Cities = Base.classes.cities

# # Create our session (link) from Python to the DB
# session = Session(engine)
# inspector = inspect(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home page.
# List all routes that are available.
@app.route("/")
def index():
    print("Server received request for 'Home' page...")

    with app.test_request_context():
        (url_for('precipitation'))

    return( f"Welcome to the Climate API page! <br/><br/><br/>"
            "<a href='/api/v1.0/precipitation'>Precipitation</a>" + ": /api/v1.0/precipitation <br/>"
            "<a href='/api/v1.0/stations'>Station</a>" + f": /api/v1.0/stations <br/>"
            "<a href='/api/v1.0/tobs'>TOBS</a>" + f": /api/v1.0/tobs <br/>"
            "<a href='/api/v1.0/2010-01-01'>Start Date</a>" + f": /api/v1.0/&lt;start&gt;  (2010-01-01 ~ 2017-08-23) *Default: 2010-01-01<br/>"
            "<a href='/api/v1.0/2010-01-01/2017-08-23'>Start End Date</a>" + f": /api/v1.0/&lt;start&gt;/&lt;end&gt; (2010-01-01 ~ 2017-08-23) *Default: /2010-01-01/2017-08-23<br/>"
            #f"{render_template("api/v1.0/precipitation.html")"
            # (url_for('precipitation')) 
            
    )

    # return "You are not logged in <br>
    #         <a href = '/login'></b>" + "click here to log in</b></a>"

    
    
# * A [landing page](#landing-page) containing:
#   * An explanation of the project.
#   * Links to each visualizations page.

@app.route("/landing")
def landing():
    return render_template('landing.html')
# * Four [visualization pages](#visualization-pages), each with:
#   * A descriptive title and heading tag.
#   * The plot/visualization itself for the selected comparison.
#   * A paragraph describing the plot and its significance.

@app.route("/visualizations1")
def visualization1():
    return "vis1 page"
@app.route("/visualizations2")
def visualization2():
    return "vis2 page"
@app.route("/visualizations3")
def visualization3():
    return "vis3 page"
@app.route("/visualizations4")
def visualization4():
    return "vis4 page"
# * A ["Comparisons" page](#comparisons-page) that:
#   * Contains all of the visualizations on the same page so we can easily visually compare them.
#   * Uses a bootstrap grid for the visualizations.
#     * The grid must be two visualizations across on screens medium and larger, and 1 across on extra-small and small screens.
@app.route("/comparisons")
def comparisons():
    return "comparisons page"
# * A ["Data" page](#data-page) that:
#   * Displays a responsive table containing the data used in the visualizations.
#     * The table must be a bootstrap table component.
#     * The data must come from exporting the `.csv` file as HTML, or converting it to HTML. Try using a tool you already know, pandas. Pandas has a nifty method approprately called `to_html` that allows you to generate a HTML table from a pandas dataframe. See the documentation [here](https://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.to_html.html)
@app.route("/data")
def data():
    return "data page"

# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)
