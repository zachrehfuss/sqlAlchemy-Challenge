# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement

Station = Base.classes.station


# Create a session
session = Session(engine)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

#create route for precipitation query
@app.route("/api/v1.0/precipitation")
def precipitation_query():
    # Create Session from python to the Database
    session = Session(engine)

    #query last 12 months of data for precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23')

    #close session
    session.close()

    #create dictionary from data and append to list of precipitation
    yearly_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        yearly_precipitation.append(precipitation_dict)

    return jsonify(yearly_precipitation)


#create route for station query (query isn't working!!!!!!!!!!!!!)
@app.route("/api/v1.0/stations")
def stations():
    # Create Session from python to the Database
    session = Session(engine)

    #Return list of all stations
    results = session.query(Station.station, Station.id).all()
    
    #close session
    session.close

    #create list of stations
    station_list = []
    for s in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['id'] = id
        station_list.append(station_dict)


    #Jsonify stations
    return jsonify(station_list)



@app.route("/api/v1.0/tobs") #unsure why this isn't working
def tobs():
    # Create Session from python to the Database
    session = Session(engine)

    #Return averages of last year from most active station
    temperature = session.query(Measurement.date, Measurement.tobs).\
    filter((Measurement.date >= '2016-08-23') & (Measurement.station == 'USC00519281')).all()

    #close session
    session.close

    #create list and run for loop
    temp_list = []
    for temp in temperature:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['temp'] = tobs
        temp_list.append(temp_dict) 

    #jsonify temperatures
    return jsonify(temp_list)



# @app.route("/api/v1.0/<start>")
# def start():
#     # Create Session from python to the Database
#     session = Session(engine)




# @app.route("/api/v1.0/<start>/<end>")
# def start_end():
#     # Create Session from python to the Database
#     session = Session(engine)







if __name__ == '__main__':
    app.run(debug=True)
