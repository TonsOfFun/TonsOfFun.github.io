---
layout: post
published: false
title: Cainthus Drone Mapping and Analytics
date: 2016-03-01
datetime: March 1, 2016
categories:
  - career
tags:
  - Python
  - startups
  - agtech
  - celery
  - django
  - flask
  - gdal
  - gdal2tiles
  - gis
  - leaflet
  - mongodb
  - reactjs
  - redis
---

## Early days of AgTech
While placing 3rd in the UC Davis AppsForAg hackathon I met Ross Hunt, cofounder of Cainthus and Francois Allain their first data science and engineering hire. This was the second in a series of 3 hackathons back in 2015, leading to the founding of GreenThumb IO, and introducing me to the world of AgTech. Starting as a consultant leading development I was eventually hired as the Director of Engineer growing the team, promoting within, and becoming CTO at Cainthus. It was an amazing time where I learned a lot and grew professionally.

![Alt text](https://res.cloudinary.com/tonsoffun/image/upload/v1696214618/snpyalfool1er2uabqjw.png)

### Joining Cainthus
I joined Cainthus in 2016 when the company was just starting out the team was small but very talented, and we were all passionate about using technology to improve agriculture. My first task was to lead the development of a product for drone flight mapping and analysis with heat map overlays for agronomists. This was a challenging project, but it was also very rewarding. We were able to develop a product that was used by agronomists all over the world. 

## Cainthus drone mapping and analytics
The goal was to provide agronomists ith a map interface where they could inspect instances of a field from weekly drone flight and analysis similarities and progressions of crop development, decay, harvestability, or irigation issues.

### Stitching GeoJPEGs into an orthomosaic GeoTIFF
We took GeoJPEGs captured by the drone and stitch them into a single orthomosaic GeoTIFF. 

```python
import os
from osgeo import gdal

# Set the input directory and output file name
input_dir = "/path/to/geojpegs"
output_file = "/path/to/output.tif"

# Get a list of all the GeoJPEG files in the input directory
input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".jpg")]

# Open the first GeoJPEG file to get the image size and projection information
first_file = gdal.Open(input_files[0])
image_size = (first_file.RasterXSize, first_file.RasterYSize)
projection = first_file.GetProjection()

# Create a new GeoTIFF file with the same size and projection as the input images
driver = gdal.GetDriverByName("GTiff")
output = driver.Create(output_file, image_size[0], image_size[1], 3, gdal.GDT_Byte)
output.SetProjection(projection)

# Loop through the input files and copy each band to the output file
for i, input_file in enumerate(input_files):
    input = gdal.Open(input_file)
    for band in range(1, 4):
        output.GetRasterBand(band).WriteArray(input.GetRasterBand(band).ReadAsArray())

# Close the input and output files
input = None
output = None
```

We then used the Geospatial Data Abstraction Library GDAL's [GDAL2Tiles](https://gdal.org/programs/gdal2tiles.html) to preprocess giant GeoTIFFs that were gigabytes in size into a more consumable format of tiles for a [Tiles Map Service](https://en.wikipedia.org/wiki/Tile_Map_Service) (TMS). 

### Tiling GeoTIFFs into tile map service format

This script is a GDAL port of the [popular MapTiler application](https://www.maptiler.com/). It generates a directory with small tiles and metadata, following the OSGeo Tile Map Service Specification. The size of tiles is 256x256 pixels by default, but it can be changed with the options. The tiles are generated in the [Web Mercator projection](https://en.wikipedia.org/wiki/Web_Mercator_projection) (EPSG:3857) used by most online maps such as [OpenStreetMap](https://www.openstreetmap.org/), [Google Maps](https://www.google.com/maps), [Bing Maps](https://www.bing.com/maps), [MapQuest](https://www.mapquest.com/), [MapBox](https://www.mapbox.com/), [HERE](https://www.here.com/), [Wikimedia Maps](https://maps.wikimedia.org/), [Yandex Maps](https://yandex.com/maps), [etc](https://en.wikipedia.org/wiki/List_of_web_map_services). The -s argument specifies the spatial reference system to use, in this case EPSG:4326 which is a common geographic coordinate system. The `-s EPSG:4326` is used for taking data in [WGS84](https://en.wikipedia.org/wiki/World_Geodetic_System) projection (EPSG:4326) and converting them into the Web Mercator projection (EPSG:3857).

```bash
gdal2tiles.py -z 0-22 -w none -p raster -s EPSG:4326 -r near -a 0,0,0 -e -k -v -f "JPEG" -t "Cainthus" -o "tiles" "ortho.tif"
```

### Tiled web maps
We used custom [tile web service](https://en.wikipedia.org/wiki/Tile_Map_Service) where tiles are 256x256 pixel representations of a map grid. At the outer most zoom level, 0, the entire world can be rendered in a single map tile. Each zoom level doubles in both dimensions, so a single tile is replaced by 4 tiles when zooming in. This means that about 22 zoom levels are sufficient for most practical purposes. 

![Cainthus: Drones Animation](https://res.cloudinary.com/tonsoffun/image/upload/v1697297324/cainthus-drones_psvggk.gif)

These custom TMS layers were rendered using Leaflet.js along with the UI allowing for users to draw polygons to target regions of interest and query the system to highlight matching regions of interest.

<script src="https://gist.github.com/TonsOfFun/e6a0a8bae0d251e4e96f533b2db6b0ef.js"></script>

### Distributed computer vision
This allowed for out computer vision data analysis to be distributed across multiple [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) worker processess using Redis as a message broker using jobs queues to manage processing tiles across multiple EC2 instances. Individual celery jobs would process the 256x256 images. 

```python
@celery.task
def process_tile(tile):
    # process tile
    return tile
```
### User experience
The rendered outputs could be accessed as images served through a python Flask server, with a URL like http://.../query_id/Z/X/Y.png, where Z is the zoom level, and X and Y identify the tile. 

![Alt text](https://res.cloudinary.com/tonsoffun/image/upload/v1696215572/cainthus-drones_bdypbn.jpg)

The rendered outputs were processed on-demand the first time and cachced in S3 for subsequent views. Only tiles that were rendered in the viewport of a user were rendered with the heatmap analysis. This provided the most responsive user experience while also optimizing resources consumption. Thumbor was a great tool for 

### Product market misft

During this time I lead the growth of the team bringing on a number of web application developers for the react map interface, backend engineers for the data processing pipeline, data scietists for improving our machine learning algorithms, and a product manager to help me keep the product focused on the business needs while ensuring our engineering efforts were as efficient as possible for this stage of the company.

## The pivot to dairy barn monitoring
Ultimately, even though we were able to achieve industry leading performance with results rendered in under a second (compared to the industry average of 24 hours), the agriculture industry had been burded by AgTech promises of drone flight analytics. So with a lack of adoption from the market the startup had to pivot away from the drone product. This lead the company into their series B fund raising mode as they found <%= link_to('product market fit in dairy barns', '_posts/career/cainthus-cows.md') %> in Fresno, California, USA to Kanata, Ottowa, Canada.