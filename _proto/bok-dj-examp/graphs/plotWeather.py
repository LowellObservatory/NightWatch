import requests
import time
import io
import os
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime, time, date
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show, output_file 
from django.contrib.staticfiles.storage import staticfiles_storage

class plotWeather(object):

  def __init__(self):
    pass

  def readTempData():

    # Read the data from the CSV file.
    station = 'KAZFLAGS163' # Mars Hill
    file_path = '/Users/dlytle/python/bok-dj-examp/graphs/static/data/{}_weather.csv'.format(station)
    data_raw = pd.read_csv(file_path)

    # Give the variables some friendlier names and convert types as necessary.
    data_raw['temp'] = data_raw['TemperatureF'].astype(float)
    data_raw['rain'] = data_raw['HourlyPrecipIn'].astype(float)
    data_raw['total_rain'] = data_raw['dailyrainin'].astype(float)
    data_raw['date'] = data_raw['DateUTC'].apply(parser.parse)
    data_raw['humidity'] = data_raw['Humidity'].astype(float)
    data_raw['wind_direction'] = data_raw['WindDirectionDegrees']
    data_raw['wind'] = data_raw['WindSpeedMPH']

    # Extract out only the data we need.
    data = data_raw.loc[:, ['date', 'station', 'temp', 'rain', 'total_rain',
          'humidity', 'wind']]
    data = data[(data['date'] >= datetime(2018,11,4)) & (data['date'] 
    <= datetime(2018,11,6))]

    # There's an issue with some stations that record rainfall ~-2500
    # where data is missing.
    if (data['rain'] < -500).sum() > 10:
      print("There's more than 10 messed up days for {}".format(station))

    # remove the bad samples
    data = data[data['rain'] > -500]

    # Assign the "day" to every date entry
    data['day'] = data['date'].apply(lambda x: x.date())

    # Get the time, day, and hour of each timestamp in the dataset
    data['time_of_day'] = data['date'].apply(lambda x: x.time())
    data['day_of_week'] = data['date'].apply(lambda x: x.weekday())
    data['hour_of_day'] = data['time_of_day'].apply(lambda x: x.hour)
    data['minute'] = data['time_of_day'].apply(lambda x: x.minute)
    # Mark the month for each entry so we can look at monthly patterns
    data['month'] = data['date'].apply(lambda x: x.month)

    # Is each time stamp on a working day (Mon-Fri)
    data['working_day'] = (data['day_of_week'] >= 0) & (data['day_of_week'] <= 4)

    # If there's any rain at all, mark that!
    data['raining'] = data['rain'] > 0.0

    #data[['temp', 'humidity', 'wind']].plot()
    #ax = plt.gca()
    #data.plot(kind='line',x='date',y='temp', ax=ax)
    #data.plot(kind='line',x='date',y='humidity', ax=ax)
    #plt.show()

    source = ColumnDataSource(data)

    p = figure(x_axis_type="datetime", plot_width=800, plot_height=180)
    p.line('date', 'temp', line_width=3,source=source)
    p.add_tools(HoverTool(
       tooltips = [
         ( 'time',   '@hour_of_day:@minute{(00)}'),
         ( 'temp', '@temp{(5.2f}F'),
       ],

       formatters={
         'date'      : 'datetime', # use 'datetime' formatter for 'date' field
       },

       mode='vline', point_policy="follow_mouse"))

    return(p)


  def readHumidity():

    # Read the data from the CSV file.
    station = 'KAZFLAGS163' # Mars Hill
    file_path = '/Users/dlytle/python/bok-dj-examp/graphs/static/data/{}_weather.csv'.format(station)
    data_raw = pd.read_csv(file_path)

    # Give the variables some friendlier names and convert types as necessary.
    data_raw['temp'] = data_raw['TemperatureF'].astype(float)
    data_raw['rain'] = data_raw['HourlyPrecipIn'].astype(float)
    data_raw['total_rain'] = data_raw['dailyrainin'].astype(float)
    data_raw['date'] = data_raw['DateUTC'].apply(parser.parse)
    data_raw['humidity'] = data_raw['Humidity'].astype(float)
    data_raw['wind_direction'] = data_raw['WindDirectionDegrees']
    data_raw['wind'] = data_raw['WindSpeedMPH']

    # Extract out only the data we need.
    data = data_raw.loc[:, ['date', 'station', 'temp', 'rain', 'total_rain',
          'humidity', 'wind']]
    data = data[(data['date'] >= datetime(2018,11,4)) & (data['date'] 
    <= datetime(2018,11,6))]

    # There's an issue with some stations that record rainfall ~-2500
    # where data is missing.
    if (data['rain'] < -500).sum() > 10:
      print("There's more than 10 messed up days for {}".format(station))

    # remove the bad samples
    data = data[data['rain'] > -500]

    # Assign the "day" to every date entry
    data['day'] = data['date'].apply(lambda x: x.date())

    # Get the time, day, and hour of each timestamp in the dataset
    data['time_of_day'] = data['date'].apply(lambda x: x.time())
    data['day_of_week'] = data['date'].apply(lambda x: x.weekday())
    data['hour_of_day'] = data['time_of_day'].apply(lambda x: x.hour)
    data['minute'] = data['time_of_day'].apply(lambda x: x.minute)
    # Mark the month for each entry so we can look at monthly patterns
    data['month'] = data['date'].apply(lambda x: x.month)

    # Is each time stamp on a working day (Mon-Fri)
    data['working_day'] = (data['day_of_week'] >= 0) & (data['day_of_week'] <= 4)

    # If there's any rain at all, mark that!
    data['raining'] = data['rain'] > 0.0

    #data[['temp', 'humidity', 'wind']].plot()
    #ax = plt.gca()
    #data.plot(kind='line',x='date',y='temp', ax=ax)
    #data.plot(kind='line',x='date',y='humidity', ax=ax)
    #plt.show()

    source = ColumnDataSource(data)

    p = figure(x_axis_type="datetime", plot_width=800, plot_height=180)
    p.line('date', 'humidity', line_width=3,source=source)
    p.add_tools(HoverTool(
       tooltips = [
         ( 'time',   '@hour_of_day:@minute{(00)}'),
         ( 'humidity', '@humidity{(5.2f}%'),
       ],

       formatters={
         'date'      : 'datetime', # use 'datetime' formatter for 'date' field
       },

       mode='vline', point_policy="follow_mouse"))

    return(p)
