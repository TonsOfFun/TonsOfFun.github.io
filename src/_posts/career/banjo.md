---
layout: post
published: false
title: Banjo Daze
date: 2012-06-01
datetime: June 1, 2012
category:
    career
tags:
    startups
    ruby
    rails
    sidekiq
    mongodb
    redis
    postgres
    postgis
---
I was a Lead Senior Ruby Software Engineer at Banjo from early 2012 to the end of 2013. 

During my time there, I built out the platform, algorithms, and geo indexes that form the foundation of the banjo events platform. This enhanced the backend system responsible for consuming and processing millions of location based social posts daily, allowing it to discover events around the world.

I designed and built a number of low latency high throughput services to analyze the geo location information to determine events based on [OpenStreetMap](https://www.openstreetmap.org/) OSM using [osmosis](https://github.com/openstreetmap/osmosis) to extract polygon info for buildings and regions. I employed spatial indexing supported by the PostGIS extension of Postgres in order to provide an efficient index to perform geoqueries like [geo tntersection queries](http://postgis.net/workshops/postgis-intro/spatial_relationships.html#st-intersects-st-disjoint-st-crosses-and-st-overlaps). The query used [ST_intersect](https://postgis.net/docs/en/ST_Intersects.html) to determine the spatial relationships with [ST_AsGeoJSON](https://postgis.net/docs/en/ST_AsGeoJSON.html) used to render [GeoJSON](https://geojson.org/) from the geometry fields and [ST_GeomFromGeoJSON](https://postgis.net/docs/en/ST_GeomFromGeoJSON.html) to query geometry fields from GeoJSON.

I exposed the data to Web and Mobile clients through a JSON API. This API provided a reverse geocoding service that could be queries in batches of 50 to provide names of places based on the coordinates in order to render place names to users. The could have been done through Google Maps API, but at millions of requests per day this would have cost the company too much money for the UX we were providing. 

With my solution we could handle millions of requests daily at the operating cost of a small application server, a Postgres server, and a Redis server to cache nearby coordinates results. The caching was the key providing a cost effective and efficient geocoding service. I realized that the [precision of coordinates](https://wiki.openstreetmap.org/wiki/Precision_of_coordinates) would allow for a basic key value cache to have a high hit rate if you rounded to the nearest 5 decimal places while still retaining enough precision for building intersections.

Now that there was a large geoindexed set of polygons we could build a system to detect when certain venues had a large number of intersecting social media posts in a given time period. This provided the basis for detecting events without needing scheudles from all of the venues around the world by using [NLP (Natural Languange Processing)](https://en.wikipedia.org/wiki/Natural_language_processing) to gleem the context from the geo feed of the venue. This also became a very powerful tool that was eventually used by news and state governments to provide context for disasters, protests, and other unexepected event.

I worked closely with both Data Science and Client teams to achieve incredible things. I got very familiar with the spatial features from MongoDB and PostgreSQL's [PostGIST](http://postgis.net/workshops/postgis-intro/indexing.html) extension. I am proud of the work I did at Banjo and the impact it had on the company. I am also grateful for the opportunity to have worked with such a talented team of engineers. 
