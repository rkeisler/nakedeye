nakedeye
========

This is code for visualizing how far we can see with the naked eye.  It uses @jakevdp's awesome [mpld3](https://github.com/jakevdp/mpld3) library to convert a lot of python/matplotlib to d3.  Viewable at [rkeisler.github.io/nakedeye/](http://rkeisler.github.io/nakedeye/).

The star positions (RA, Dec, parallax distance) come from the Hipparcos satellite mission.  I included only stars with parallaxes measured with nominal fractional errors smaller than 20%, which is true for most (85%) of the Vmag<6 stars shown here.  I chose to define "city-viewable" stars as those with Vmag<3 (161 stars), and "country-viewable" stars as Vmag<6 (4129 stars).

I should mention that I had to hack the d3 a bit to get the text size to scale with the zoom level.  Specifically I added `axes_{{ axid }}.selectAll("text").attr("font-size", (20.0*d3.event.scale/1.3) + "pt")` inside of the `zoomed` function.  Also note that I wrote this code in early 2014, when mpld3 was under rapid development, and you will almost surely need to apply a different d3.js hack when using newer versions of mpld3.
