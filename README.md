nakedeye
========

This is code for visualizing the how far we can see with the naked eye.  It uses @jakevdp's awesome [mpld3](https://github.com/jakevdp/mpld3) library to convert a lot of python/matplotlib to d3.  Viewable at [stanford.edu/~rkeisler/nakedeye](http://stanford.edu/~rkeisler/nakedeye).

I should mention that I had to hack the d3 a bit to get the text size to scale with the zoom level.  Specifically I added `axes_{{ axid }}.selectAll("text").attr("font-size", (20.0*d3.event.scale/1.3) + "pt")` inside of the `zoomed` function.

