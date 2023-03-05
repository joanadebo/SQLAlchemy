app.py

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Welcome to Hawaii."""
    return (
        f"Available links for Station Weather and Preciptation:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    date_year = sessions.query(func.max(Measurement.date)).first()
    for max_year in date_year:
        date_last_year = max_year
        
    """Return a list of precipitation for the last year"""
    # Query all passengers
    precips = session.query(Measurement.date, func.sum(Measurement.prcp)).filter((Measurement.date >= date_last_year) & \
                                                         (Measurement.prcp != "None") & \
                                                         (Measurement.prcp != "0.0")).\
                      group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    all_precip_dates = []
    for date, prcp in precips:
        precip_dict = {}
        precip_dict[date] = prcp
        all_precip_dates.append(precip_dict)


    return jsonify(all_precip_dates)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of stations"""
    station_results = session.query(Station.station, Station.name).order_by(Station.station).all()

    session.close()

    all_stations = []
    for station_id, station_name in station_results:
        station_dict = {}
        station_dict["id"] = station_id
        station_dict["name"] = station_name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return the most active station Temps"""
    sel = [Measurement.date,
      func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]
    top_observe_stats = session.query(*sel).filter(Measurement.station == 'USC00519281').all()

    session.close()
    
    top_list = []
    for top_station, top_min, top_max, top_avg in top_observe_stats:
        top = {}
        top["Station"] = top_station
        top["Min Temp"] = top_min
        top["Max Temp"] = top_max
        top["Avg Temp"] = top_avg
        top_list.append(top)
    
    jsonify(top)

@app.route("api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return the most active station Temps"""
    sel = [Measurement.date,
      func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]
    top_observe_stats = session.query(*sel).filter(Measurement.station == 'USC00519281').all()

    session.close()
    
    top_list = []
    for top_station, top_min, top_max, top_avg in top_observe_stats:
        top = {}
        top["Station"] = top_station
        top["Min Temp"] = top_min
        top["Max Temp"] = top_max
        top["Avg Temp"] = top_avg
        top_list.append(top)
    
    jsonify(top)


@app.route("api/v1.0/<start>/<end>")
def date_measures(start, end):
    session = Session(engine)

    if start and end:
   
        """Return the most active station Temps"""
        sel = [Measurement.date,
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
        top_observe_stats = session.query(*sel).filter(Measurement.station == 'USC00519281').\
            filter((Measurement.date > start) & (Measurement.date <= end)).all()

    elif start:

        """Return the most active station Temps"""
        sel = [Measurement.date,
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
        top_observe_stats = session.query(*sel).filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date > start).all()

    else:

                """Return the most active station Temps"""
        sel = [Measurement.date,
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
        top_observe_stats = session.query(*sel).filter(Measurement.station == 'USC00519281').all()



    session.close()
    
    top_list = []
    for top_station, top_min, top_max, top_avg in top_observe_stats:
        top = {}
        top["Station"] = top_station
        top["Min Temp"] = top_min
        top["Max Temp"] = top_max
        top["Avg Temp"] = top_avg
        top_list.append(top)
    
    jsonify(top)

if __name__ == '__main__':
    app.run(debug=True)