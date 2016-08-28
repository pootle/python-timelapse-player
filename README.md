# python-timelapse-player
A simple proof of concept python webserver for viewing timelapse sequences in a web page.

A python3 webserver that requires no additional libraries to run, built on http.server.HTTPServer and around 100 lines of code.

This was written to explore how simple and fast a webserver could be on small machines such as Raspberry PI.

It works in conjunction with a simple web page that implements all its functionality in javascript.

The simple webserver builds an index to all the jpeg files in the given folder, and serves a web page which then allows various javascript functions to move around within the images and play them back at various speeds by controlling framerate and stride.

Firefox and chrome on linux, android and windows all appear to work, edge does not work. ie sort of works. On phones and tablets the frame rate has to be kept low to avoid stalling.
