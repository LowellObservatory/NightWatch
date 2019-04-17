# Requirements

bokeh >= x.x.x
django >= 2.1.2
python >= 3.6

...probably other stuff too.  Will fill this in more once I have it
containerized and defined.

## Setup notes

Isotope (https://isotope.metafizzy.co/) downloaded on 2019 04 04,
or they can be linked directly from the CDN, a la:

```
<script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.js"></script>
<!-- or -->
<script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js"></script>
```

I opted to just grab the minified version and put it into the static files
tree so we don't have to worry about it.

### Dev. Notes

Following along from https://docs.djangoproject.com/en/2.2/intro/tutorial01/

"nightwatch" is the *project*, containing the "dctplots" *app* along with
the GOES-16 reprojection stuff as a separate *whateverthing*.

The layout is starting to irritate me a little bit, due to all the
warnings/caveats about namespaces; e.g. I'm tired of making directories
like nightwatch/dctplots/templates/dctplots.  I get the reason this is
the suggested way; I just find it irksome.

Once you make an app, make sure to put it into the main settings.py file;
otherwise the templates and other stuff won't be automagically added to the
path for that app and you'll get stuff like "TemplateDoesNotExist" errors.

Relevant bit from the docs:

```
Your project’s TEMPLATES setting describes how Django will load and
render templates. The default settings file configures a DjangoTemplates
backend whose APP_DIRS option is set to True. By convention DjangoTemplates
looks for a “templates” subdirectory in each of the INSTALLED_APPS.
```

If testing locally, remember to disable AdBlock/Privacy Badger/whatever...
I was getting broken images that showed up as "Blocked By Client" errors
in the Chrome console when viewing the page (on localhost); either of the
above mentioned Chrome extensions were blocking images linked from
another domain on the intranet.
