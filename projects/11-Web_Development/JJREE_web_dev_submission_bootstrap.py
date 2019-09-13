# Dependendies
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
import os
import csv
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify, request, url_for, redirect, render_template

#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///resources/hawaii.sqlite")

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

    
# * A [landing page](#landing-page) containing:
#   * An explanation of the project.
#   * Links to each visualizations page.

@app.route("/")
def landing():
#    return "TESTING"
    return render_template('/landing_bs1.html')
# * Four [visualization pages](#visualization-pages), each with:
#   * A descriptive title and heading tag.
#   * The plot/visualization itself for the selected comparison.
#   * A paragraph describing the plot and its significance.

@app.route("/windspeed")
def windspeed():
    return render_template('/windspeed.html')
@app.route("/cloudiness")
def cloudiness():
    return render_template('/cloudiness.html')
@app.route("/humidity")
def humidity():
    return render_template('/humidity.html')
@app.route("/maxtemp")
def maxtemp():
    return render_template('/maxtemp.html')
# * A ["Comparisons" page](#comparisons-page) that:
#   * Contains all of the visualizations on the same page so we can easily visually compare them.
#   * Uses a bootstrap grid for the visualizations.
#     * The grid must be two visualizations across on screens medium and larger, and 1 across on extra-small and small screens.
@app.route("/comparison")
def comparison():
    return render_template('/comparison.html')

@app.route("/comparison1")
def comparison1():
    return render_template('/comparison1.html')
# * A ["Data" page](#data-page) that:
#   * Displays a responsive table containing the data used in the visualizations.
#     * The table must be a bootstrap table component.
#     * The data must come from exporting the `.csv` file as HTML, or converting it to HTML. Try using a tool you already know, pandas. Pandas has a nifty method approprately called `to_html` that allows you to generate a HTML table from a pandas dataframe. See the documentation [here](https://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.to_html.html)
@app.route("/data")
def data():
    file = "/Users/jasonree/Documents/GitHub/Project_Submissions/Projects/11-Web_Develepment/static/resources/cities.csv"
    data_df = pd.read_csv(file)
    data_html = data_df.to_html()

    return render_template('/data.html', column_names=data_df.columns.values, row_data=list(data_df.values.tolist()), zip=zip, data_html = data_html)

# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)
