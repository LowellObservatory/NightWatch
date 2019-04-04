## Setup notes:

Isotope (https://isotope.metafizzy.co/) downloaded on 2019 04 04,
or they can be linked directly from the CDN, a la:

```
<script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.js"></script>
<!-- or -->
<script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js"></script>
```

Same goes for Packery (https://packery.metafizzy.co/):

```
<script src="https://unpkg.com/packery@2/dist/packery.pkgd.js"></script>
<!-- or -->
<script src="https://unpkg.com/packery@2/dist/packery.pkgd.min.js"></script>
```

### Dev. Notes

Following along from https://docs.djangoproject.com/en/2.2/intro/tutorial01/

"nightwatch" is the *project*, containing the "dctplots" *app* along with
the GOES-16 reprojection stuff as a separate *whateverthing*.

The layout is starting to irritate me a little bit, due to all the
warnings/caveats about namespaces; e.g. I'm tired of making directories
like nightwatch/dctplots/templates/dctplots.
