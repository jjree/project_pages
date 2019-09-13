# dependencies
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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
inspector = inspect(engine)

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

# /api/v1.0/precipitation
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query date and prcp data
    prcp_query = session.query(Measurement.date, Measurement.prcp).all()
    
    # Organize data into dict for jsonify
    all_measurements = []
    for date, prcp in prcp_query:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_measurements.append(prcp_dict)
    
    # Output JSON of all date/prcp data
    return jsonify(all_measurements)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    select = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    station_query = session.query(*select).all()
    return jsonify(station_query)

# /api/v1.0/tobs
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # Find last date in data and calculate 1 year prior to this last date
    max_date = session.query(func.max(Measurement.date))
    max_date = pd.to_datetime((max_date[0])).date
    min_date = pd.to_datetime((max_date - pd.DateOffset(365))).date
    min_date = str(min_date[0])
    max_date = str(max_date[0])

    # Query tobs between min and max dates obtained above
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <= max_date).filter(Measurement.date >= min_date).all()
    
    # Create dictionary for jsonify
    all_tobs = []
    for d, t in tobs_query:
        tobs_dict = {}
        tobs_dict["date"] = d
        tobs_dict["tobs"] = t
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start(start):
    # Query min/avg/max tobs for all dates after 'start' date provided by user
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    tobs_query_startDate = session.query(*select).filter(Measurement.date >= start).all()
    
    # Create dict to organize query for JSONify
    all_start = []
    for min, avg, max in tobs_query_startDate:
        start_dict={}
        start_dict["min"] = min
        start_dict["avg"] = avg
        start_dict["max"] = max
        all_start.append(start_dict)

    # Output JSON of tobs after 'start' date
    return jsonify(tobs_query_startDate)

# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Query min/avg/max tobs for all dates between 'start' and 'end' date provided by user
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    tobs_query_startEndDate = session.query(*select).filter(Measurement.date <= end).filter(Measurement.date >= start).all()
    
    # Create dict to organize query for JSONify
    all_startEnd = []
    for min, avg, max in tobs_query_startEndDate:
        startEnd_dict={}
        startEnd_dict["min"] = min
        startEnd_dict["avg"] = avg
        startEnd_dict["max"] = max
        all_startEnd.append(startEnd_dict)

    # Output JSON of tobs between 'start' and 'end' date
    return jsonify(tobs_query_startEndDate)


# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
    

