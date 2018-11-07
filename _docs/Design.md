## Proposed Design Elements for *NightWatch*

1. Propose that *NightWatch* be presented as a website.
2. Propose we use Django for the website, not because we need much interactivity
   for this project but because I think familiarity with Django will serve us well on
   other projects such as the DOL replacement, which may also be a website.
3. Also, there is the possibility that some of the other software developed in the
   future (besides the DOL) will be developed as interactive websites (LOUI replacement, perhaps?).
4. Propose that we DO build some interactivity into *NightWatch*, in spite of the requirements.
   
   -  From some of the initial prototypes, it seems evident that it will be necessary
      to adjust plot limits in-situ rather than deal with hard coded values
      or zooming in/out until it's ok enough.

5. Interactive plots in Django possible using Bokeh with the Bokeh Server.

   [examples of Bokeh Server plots](https://bokeh.pydata.org/en/latest/docs/gallery.html)

6. Propose that the resulting product has a 'darker' theme (black/dark background) to
   not cause additional bright-light-like shine while observing.
