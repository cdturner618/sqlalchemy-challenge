import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurements = Base.classes.measurement
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
    """List all available api routes."""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

# Query All stations
    all_stations = session.query(Measurements.station).group_by(
        Measurements.station).all()

    session.close()

    station_list = list(np.ravel(all_stations))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temps():
    # Create our session (link) from Python to the DB
    session2 = Session(engine)


# Query All temp
    import datetime as dt
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    sel1 = [
        Measurements.date,
        Measurements.tobs]
    all_temps = session2.query(*sel1).filter((Measurements.date) >=
                                             query_date).filter(Measurements.station == 'USC00519281').all()

    session2.close()

    Temp_list = list(np.ravel(all_temps))

    return jsonify(Temp_list)


@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session3 = Session(engine)


# Query All Prcp

    sel2 = [
        Measurements.date,
        Measurements.prcp]
    all_prcp = session3.query(
        *sel2).filter(Measurements.date).filter(Measurements.prcp).all()

    session3.close()

    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = []
    for date, prcp, in all_prcp:
        date_dict = {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        all_dates.append(date_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/<date>")
def temp_range(date):
    # Create our session (link) from Python to the DB
    session4 = Session(engine)
# Query All start dates
    sel3 = [Measurements.date,
            func.min(Measurements.tobs),
            func.avg(Measurements.tobs),
            func.max(Measurements.tobs)]
    start_date = session4.query(
        *sel3).filter(Measurements.date).group_by(Measurements.date).all()
    session4.close()
    for day in start_date:
        if day[0] == date:
            return jsonify(
                {
                    "date": day[0],
                    "min": day[1],
                    "avg": day[2],
                    "max": day[3]
                }
            )
    return jsonify(f"{date} not found"), 404


@app.route("/api/v1.0/<startdate>/<enddate>")
def temp_ranges(dates):
    # Create our session (link) from Python to the DB
    session5 = Session(engine)
# Query All start dates
    sel4 = [Measurements.date,
            func.min(Measurements.tobs),
            func.avg(Measurements.tobs),
            func.max(Measurements.tobs)]
    start_dates = session5.query(
        *sel4).filter(Measurements.date).group_by(Measurements.date).all()
    session5.close()
    for days in start_dates:
        if days[0] == dates:
            return jsonify(
                {
                    "date": days[0],
                    "min": days[1],
                    "avg": days[2],
                    "max": days[3]
                }
            )
    return jsonify(f"{dates} not found"), 404


if __name__ == '__main__':
    app.run(debug=True)
