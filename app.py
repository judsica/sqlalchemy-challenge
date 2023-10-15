# Import the dependencies.
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from flask import Flask, jsonify
import datetime as dt
import pandas as pd

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
app = Flask(__name__)

#################################################
# Flask Setup
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start<br/>"
        "/api/v1.0/start/end"
    )
session = Session(engine)


#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")    
def precipitation():
    precipitation_data = session.query(Measurement.date, Measurement.prcp).all()
    
    
    precipitation_type = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_type)
@app.route("/api/v1.0/<stations>")
def stations():
    station_list = session.query(Station.station, Station.name).all()
    
   
    stations = [{"station": station, "name": name} for station, name in station_list]
    
    return jsonify(stations)
@app.route("/api/v1.0/<tobs>")
def tobs():
    active = 'USC00519281'
    last_date = session.query(func.max(Measurement.date)).filter(Measurement.station == active).scalar()
    one_year = (pd.to_datetime(last_date) - pd.DateOffset(days=365)).date()
    tobs_1 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == active, Measurement.date >= one_year).all()
    
    return jsonify(tobs_1) 
@app.route("/api/v1.0/<start>")
def start_date(start_date):
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    return jsonify(temperature_stats)
@app.route("/api/v1.0/<end_date>")
def end_date(start_date, end_date):
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    return jsonify(temperature_stats)
if __name__ == '__main__':
    app.run(debug=True)