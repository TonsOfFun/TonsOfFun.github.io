---
layout: post
published: false
title: Banjo Daze
date: 2012-06-01
datetime: June 1, 2012
categories:
    - career
tags:
    - startups
    - ruby
    - sinatra
    - rails
    - sidekiq
    - mongodb
    - redis
    - PostgreSQL
    - PostGIS
---

I was a Lead Senior Ruby Software Engineer at Banjo from early 2012 to the end of 2013. During my time there, I built out the platform, algorithms, and geo indexes that form the foundation of the banjo events platform. This enhanced the backend system responsible for consuming and processing millions of location based social posts daily, allowing it to discover events around the world.

## The research and development
At banjo we used [MongoDB](https://www.mongodb.com/) extensively and exclusively until I started looking into more advanced GIS features for a new product we were developing. I discovered that [GEOS](https://libgeos.org/) had features we'd need to achieve our goals. [PostGIS](https://postgis.net/) leverages libgeos to support these GIS concepts in [PostgreSQL](https://www.postgresql.org/). Out of the box MongoDB had many geospatial features, but at the time the implementation was still limited to `Polygon` types and did not support more complex `MultiPolygon` types.


I designed and built a number of low latency high throughput services to analyze the geo location information to determine events based on [OpenStreetMap (OSM)](https://www.openstreetmap.org/), this dataset was the foundation for the popular map and navigation app Waze. Using [osmosis](https://github.com/openstreetmap/osmosis) to extract polygon info for buildings and regions. I employed spatial indexing supported by the PostGIS extension of Postgres in order to provide an efficient index to perform geoqueries like [geo tntersection queries](http://postgis.net/workshops/postgis-intro/spatial_relationships.html#st-intersects-st-disjoint-st-crosses-and-st-overlaps). 

### PostGIS
PostGIS is a spatial database extender for PostgreSQL object-relational database. It adds support for geographic objects allowing location queries to be run in SQL. In order to use PostGIS, you need to install both PostgreSQL and the PostGIS extension. The PostGIS extension is installed by running the `CREATE EXTENSION` command from the `psql` command line or from the `CREATE EXTENSION` command in a SQL script.


```sql
CREATE EXTENSION postgis;
SELECT POSTGIS_VERSION(); # succeeds if PostGIS objects are present.
```

### In-house reverse geocoding
The queries used [ST_intersect](https://postgis.net/docs/en/ST_Intersects.html) to determine the spatial relationships with [ST_AsGeoJSON](https://postgis.net/docs/en/ST_AsGeoJSON.html) used to render [GeoJSON](https://geojson.org/) from the geometry fields indexed using [GIST](http://postgis.net/workshops/postgis-intro/indexing.html) and [ST_GeomFromGeoJSON](https://postgis.net/docs/en/ST_GeomFromGeoJSON.html) to query geometry fields from GeoJSON.

### From coordinates to the name of a place
I'll never forget that 37,-122 is a park in Santa Cruz or 0,0 is the Atlantic ocean off the southern coast of Ghana. With polygons for all of the administrative boundaries around the world indexed with PostGIS, I exposed the data to Web and Mobile clients through a JSON API. This API provided a reverse geocoding service that could be queries in batches of 50 to provide names of places based on the coordinates in order to render place names to users. The could have been done through Google Maps API, but at millions of requests per day this would have cost the company too much money for the UX we were providing. 

```sql
SELECT ST_AsGeoJSON(geom) FROM districts WHERE ST_Intersects(geom, ST_GeomFromGeoJSON('{"type":"Point","coordinates":[-122.431297,37.773972]}'));
```

<script src="https://gist.github.com/TonsOfFun/2a4c7e2ef0c9a667767f.js"></script>
> This is an example of the dataset I collected from OpenStreetMap and indexed in PostGIS showing all of the San Francisco Districts. 

## Reverse geociding at scale
Geo queries even indexed properly are very CPU intenseive operations in the database. Effective caching was the key providing a cost effective and efficient geocoding service. I realized that the [precision of coordinates](https://wiki.openstreetmap.org/wiki/Precision_of_coordinates) would allow for a basic key-value cache to have a high hit rate if you rounded to the nearest four (11.112 meters) or five (1.112 meters) decimal places. This would allow for higher throughput with less pressure on the DB and minimal load on the Redis server, all while still retaining enough precision for boundary intersections. With my solution we could handle millions of requests daily at the operating cost of a small application server, a Postgres server, and a Redis server to cache nearby coordinates results. 

### The cache
I built a simple key-value cache using Redis to store the results of the reverse geocoding queries. The key was a string of the coordinates rounded to the nearest four decimal places. The value was a JSON object with the name of the place and the coordinates of the place. This allowed for a very high hit rate on the cache and a very low load on the Redis server. The cache was also used to store the results of the polygon queries to reduce the load on the Postgres server. 

```ruby
def cache_key(lat, lng)
  "#{lat.round(4)},#{lng.round(4)}"
end

def cache_get(lat, lng)
  key = cache_key(lat, lng)
  value = redis.get(key)
  return nil unless value
  JSON.parse(value)
end

def cache_set(lat, lng, name, coordinates)
  key = cache_key(lat, lng)
  value = { name: name, coordinates: coordinates }.to_json
  redis.set(key, value)
end
```

### Event detection as a service
Now that there was a large geoindexed set of polygons we could build a system to detect when certain venues had a large number of intersecting social media posts in a given time period. This provided the basis for detecting events without needing scheudles from all of the venues around the world by using [NLP (Natural Languange Processing)](https://en.wikipedia.org/wiki/Natural_language_processing) to gleem the context from the geo feed of the venue. This also became a very powerful tool that was eventually used by news and state governments to provide context for disasters, protests, and other unexepected event.

I worked closely with both Data Science and Client teams to achieve incredible things. I got very familiar with the spatial features from MongoDB and PostgreSQL's [PostGIST](http://postgis.net/workshops/postgis-intro/indexing.html) extension. I am proud of the work I did at Banjo and the impact it had on the company. I am also grateful for the opportunity to have worked with such a talented team of engineers. 
