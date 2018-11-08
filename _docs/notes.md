[Plotting NEXRAD data using Amazon Web Services Big Data Project](https://www.nsstc.uah.edu/users/brian.freitag/AWS_Radar_with_Python.html)

[GitHub repository for example of displaying Bokeh Server plots on a Django website](https://github.com/konoanalytics/BokehDjango)

### Embedding an active update plot into a Django web page.
#### commandline: bokeh  serve ohlc/ --allow-websocket-origin=127.0.0.1:8000
This runs the Bokeh server on a python routine (in the ohlc directory) that makes dynamic plots.
the --allow-blah-blah part tells Bokeh that a web socket can connect from the URL listed
which is the URL of the Django server in this case.

#### In django/webapp/view.py do: script3 = server_document("http://localhost:5006/ohlc")
This returns a script that can be imbedded into the html document.
The URL listed is the URL defined for where the Bokeh server is running.
