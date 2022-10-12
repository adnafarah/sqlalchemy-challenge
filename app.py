from flask import Flask, render_template, redirect, url_for, jsonify

import numpy as np
import datetime as dt
from datetime import date, datetime, timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/stations"
        f"/tobs"
        f"/start"
        f"/start/end"
    )


@app.route('/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp_ = session.query(Measurement.date, Measurement.prcp, ).filter(
    Measurement.date < dt.date(2017,8,23), Measurement.date > dt.date(2016,8,23)).all()

    session.close()

    # Convert list of tuples into dictionary
    prcp_dict = dict(prcp_)

    return jsonify(prcp_dict)


@app.route('/stations')
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query database and return stations
    stations_ = session.query(Measurement.station).distinct().all()

    session.close()

    #convert to normal list
    stations_list = list(np.ravel(stations_))

    return jsonify(stations_list)


@app.route('/tobs')
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the previous year of data.
    tobs_ = session.query(Measurement.date, Measurement.prcp, ).filter(
        Measurement.date < dt.date(2016,8,23), Measurement.date > dt.date(2015,8,23)).filter(Measurement.station== 'USC00519281').all()
    
    session.close()
    
    #convert to normal list 
    tobs_list = list(np.ravel(tobs_))


    return jsonify(tobs_list)



@app.route('/<start>')
def start(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start,'%m%d%Y')

    min_temp_ = session.query(Measurement.station, Measurement.prcp,
             func.min(Measurement.tobs)).filter(Measurement.date >= start).all()

    avg_temp_ = session.query(Measurement.station, Measurement.prcp,
             func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    max_temp_ = session.query(Measurement.station, Measurement.prcp,
             func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()
    
    #add to list
    results_list_ = [min_temp_, max_temp_, avg_temp_]

    results_list = []
    for x in range(len(results_list_)):
        #print(results_list_[x])
        results_list.append(results_list_[x])
    results_list = list(np.ravel(results_list))

    return jsonify(results_list)
        

@app.route('/<starti>/<end>')
def starti(starti, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    starti = dt.datetime.strptime(starti,'%m%d%Y')
    end = dt.datetime.strptime(end,'%m%d%Y')
    
    new_min_temp_ = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= starti, Measurement.date <= end).all()

    new_avg_temp_ = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= starti, Measurement.date <= end).all()

    new_max_temp_ = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= starti, Measurement.date <= end).all()
    session.close()

    start_end_list = [new_min_temp_, new_avg_temp_, new_max_temp_]

    start_end_list = list(np.ravel(start_end_list))
    
    return jsonify(start_end_list)


if __name__ == "__main__":
    app.run(debug=True)

