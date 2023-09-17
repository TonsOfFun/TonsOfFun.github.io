---
layout: post
published: false
title: Cainthus Drone Mapping and Analytics
date: 2016-03-01
datetime: March 1, 2016
category:
    career
tags:
    agtech
    startups
    python
    celery
    flask
    django
    mongodb
    redis
    leaflet
    gdal2tiles
    gdal
    gis
---

I am excited to share my experience as CTO/Lead Software Engineer at Cainthus. It was an amazing time where I learned a lot and grew professionally.

While placing 3rd in the UC Davis AppsForAg hackathon I met Ross Hunt, cofounder of Cainthus and Francois Allain their first data science and engineering hire. This was the second in a series of 3 hackathons back in 2015, leading to the foudning of GreenThumb IO.

I joined Cainthus in 2016 when the company was just a few months old. The team was small but very talented, and we were all passionate about using technology to improve agriculture.

My first task was to lead the development of a product for drone flight mapping and analysis with heat map overlays for agronomists. This was a challenging project, but it was also very rewarding. We were able to develop a product that was used by agronomists all over the world. The goal was to provide agronomists ith a map interface where they could inspect instances of a field from weekly drone flight and analysis similarities and progressions of crop development or decay.

We used the Geospatial Data Abstraction Library GDAL's [GDAL2Tiles](https://gdal.org/programs/gdal2tiles.html) to preprocess giant GeoTIFFs that were gigabytes in size into a more consumable format of tiles for a Tiles Map Service (TMS). Tiles were 256x256 pixel representations of a map grid. At the outer most zoom level, 0, the entire world can be rendered in a single map tile. Each zoom level doubles in both dimensions, so a single tile is replaced by 4 tiles when zooming in. This means that about 22 zoom levels are sufficient for most practical purposes. These custom TMS layers were rendered using Leaflet.js along with the UI allowing for users to draw polygons to target regions of interest and query the system to highlight matching regions of interest.

This allowed for out computer vision data analysis to be distributed across multiple [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) worker processess using Redis as a jobs broker to managed processes across multiple EC2 instances. Individual celery jobs would process the 256x256 images. The rendered outputs could be accessed as images served through a python Flask server, with a URL like http://.../query_id/Z/X/Y.png, where Z is the zoom level, and X and Y identify the tile. The rendered outputs were processed on-demand the first time and cachced in S3 for subsequent views. Only tiles that were rendered in the viewport of a user were rendered with the heatmap analysis. This provided the most responsive user experience while also optimizing resources consumption.

During this time I lead the growth of the team bringing on a number of web application developers for the react map interface, backend engineers for the data processing pipeline, data scietists for improving our machine learning algorithms, and a product manager to help me keep the product focused on the business needs while ensuring our engineering efforts were as efficient as possible for this stage of the company.

Ultimately, even though we were able to achieve industry leading performance with results rendered in under a second (compared to the industry average of 24 hours), the agriculture industry had been burded by AgTech promises of drone flight analytics. So with a lack of adoption from the market the startup had to pivot away from the drone product. This lead the company into their series B fund raising mode as they found product market fit in dairy barns from Fresno, California, USA to Kanata, Ottowa, Canada.