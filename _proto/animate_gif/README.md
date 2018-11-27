A simple example of downloading images, constructing animated GIFs of recent data on a regular time interval,
and displaying and updating these animaged GIFs in a web page.

"test-get.py" downloads images from a web cam in Bishop, California every ten seconds and puts them in the local directory.
The files are named bishop00001.jpg and etc.

"update-gif.py" constructs an animated GIF from the most recent 30 images and puts it in "updateMovie.gif" every 60 seconds.

"showImage.html" is a very small web page that displays the above mentioned "updateMovie.gif" and updates itself every 60
seconds to grab the new movie.  There is some code in there to fool the web browsers so they don't just reload the cached
image.
