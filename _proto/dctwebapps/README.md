### This is a skeleton Django/Bokeh web application for NightWatch.

The subdirectory, "dctwebapps" contains the Django setup for this collection of web applications.  There
is only one webapp defined for now, "NightWatch".

The "Bokeh" directory contains two subdirectories, each of which makes and active plot when run with
the bokeh server.

The subdirectory, "NightWatch", contains the main NightWatch prototype code.

Currently, Nightwatch displays an embedded weather map, two non-active plots, and two active plots.

To run the system

1. Download everything in this directory.

2. In the bokeh directory, run the bokeh server:\
   bokeh serve newact/ ohlc/ --allow-websocket-origin=localhost:800\
   This runs the server with two applications, "newact" and "ohlc" and allows Django running
   at localhost:8000 to create web sockets.
  
3. In the main directory, the one with "manage.py", run the Django server:\
   python3 manage.py runserver 0.0.0.0:8000\
   This will run the web server and make it visible on your machine as localhost:8000
   and it will be available inside the local area network as "yourmachinename.lowell.edu:8000"
   from other computers.
   
 4. In a web browser, go to http://localhost:8000 to see the web page.
