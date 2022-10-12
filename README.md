# sqlalchemy-challenge

This aim of this project was to complete climate analysis & plot it and then design a Flask API based on the queries developed. 

## Part 1: Climate Analysis and Exploration
In this section, I used Python and SQLAlchemy to perform basic climate analysis and data exploration of the climate database. This was completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

The analysis is in the climate_analysis.ipynb notebook. 

* Used SQLAlchemy’s create_engine to connect to the SQLite database.
* Used SQLAlchemy’s automap_base() to reflect the tables into classes and saved a reference to those classes called Station and Measurement
* Linked Python to the database by creating a SQLAlchemy session.
* Session was closed at the end of the notebook


### Precipitation Analysis
To perform an analysis of precipitation in the area, the below was carried out:


* Found the most recent date in the dataset.
* Used this date to retrieve the previous 12 months of precipitation data by querying the 12 previous months of data.
* Selected only the date and prcp values.
* Loaded the query results into a Pandas DataFrame, and set the index to the date column.
* Sorted the DataFrame values by date.
* Plotted the results by using the DataFrame plot method & used Pandas to print the summary statistics for the precipitation data.


### Station Analysis
To perform an analysis of stations in the area, the following was carried out:

* Designed a query to calculate the total number of stations in the dataset.
* Designed a query to find the most active stations (the stations with the most rows).
* List the stations and observation counts in descending order.
* Determined which station id had the highest number of observations.
* Using the most active station id, calculated the lowest, highest, and average temperatures  (using functions such as func.min, func.max, func.avg, and func.count in the queries).
* Designed a query to retrieve the previous 12 months of temperature observation data (TOBS).
* Filtered by the station with the highest number of observations.
* Queried the previous 12 months of temperature observation data for this station.
* Plotted the results as a histogram with bins=12


## Part 2: Designing the Climate App

* Flask was used to create the routes. 
* /precipitation: 
    Query results were converted to a dictionary using date as the key and prcp as the value.
    Returned the JSON representation of this dictionary.

* /stations:
    Returned a JSON list of stations from the dataset.

* /tobs:
    Queried the dates and temperature observations of the most active station for the previous year of data.
    Returned a JSON list of temperature observations (TOBS) for the previous year.

* /<start> and /api/v1.0/<start>/<end>:
    Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
    
    When given the start only, calculated TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.

    When given the start and the end date, calculated the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).