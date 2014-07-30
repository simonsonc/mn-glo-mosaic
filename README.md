# Overview

This project is designed to take georeferenced images from the the General Land
Office surveys of Minnesota and stitch them together into one georeferenced map.

The original georeferenced images are provided by the [GLO Historic Plat Map
Retrieval System](http://www.mngeo.state.mn.us/glo/).

This project is run by a build system that prepares the images and turns them
into a mosaic. It goes through the following process:

1. Downloading the township/range images from mngeo
2. Generating a virtual image that contains a cutline for the map area
3. Building tiled images that merge the survey maps together

# Building

The simplest way to try out the build is to pick a county to build. For example,
to build Ramsey county, run:

```
rake Ramsey
```
