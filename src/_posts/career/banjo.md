---
layout: post
published: false
title: Banjo (Large-scale Geo Information Systems)
description: hi
date: 2023-12-01
datetime: December 1, 2023
categories:
  - career
tags:
  - PostGIS
  - PostgreSQL
  - Rails
  - Ruby
  - Startups
  - mongodb
  - redis
  - sidekiq
  - sinatra
  - AI
---

From 2012 to 2013, I held the position of Lead Senior Ruby Software Engineer at Banjo. I built the platform, algorithms, and geo indexes that formed the foundation of the Banjo event detection platform - social media feeds indexed by location, specifically public spaces like event centers, restaurants, and bars.

My contributions enabled the app to efficiently consume and process millions of location-based social posts daily. This allowed users to discover events nearby and provided context about events happening around the world. **The product was later adopted by local governments to monitor and detect security threats in real-time and by news organizations to stay abreast of unexpected events like natural disasters.**

I also helped the company **save millions of dollars in annual costs (~$29M)** by reducing reliance on third-party APIs.

## Reverse Geocoding: Research and Development

### What is Reverse Geocoding

Geocoding is the process of taking the name of a location and providing its corresponding geographical coordinates. Conversely, **reverse geocoding means taking coordinates and rendering them as a recognizable place name.** 

At Banjo, we needed to render place names in the UI, but the social media APIs only provided us with coordinates. Reverse geocoding was a critical component of the product so we could provide users with the names of locations linked to various events.

### Challenge: Indexing MultiPolygons 
My first task was collecting a dataset of global administrative boundaries. I discovered that OpenStreetMap had an open source data set of global map information, including lines for streets, coordinates for places of interest, `Polygons` for buildings, and `MultiPolygons` for things like administrative boundaries.

`MultiPolygon`s are necessary for representing many administrative boundaries, such as the boundaries of San Francisco, which include Treasure Island - a `Polygon` that exists outside of the main `Polygon`. Another example is Rome, which is a `MultiPolygon` with a gap in the middle of it for the Vatican.

<script src="https://gist.github.com/TonsOfFun/2a4c7e2ef0c9a667767f.js"></script>
> This is an example of the dataset I collected from OpenStreetMap and indexed in PostGIS showing all of the San Francisco Districts, including Treasure Island. 
>

We needed to index `MultiPolygons` in order to efficiently query for our reverse geocoding service - otherwise we would have to load all of the geometry objects into memory to perform the calculations and determine where a set of given coordinates was located. Although OpenStreetMap offered an index of `MultiPolygons`, our database was unable to index and query them efficiently. 

#### Overcoming database limitations with PostGIS

At the time we used [MongoDB](https://www.mongodb.com/), which had many geospatial features out of the box, but the implementation was limited to `Polygon` types.

[PostGIS](https://postgis.net/) is a spatial database extension for the [PostgreSQL](https://www.postgresql.org/) (Postgres) relational database. PostGIS leverages libGEOS to support these GIS concepts in Postgres. I discovered that [GEOS](https://libgeos.org/) had the features we needed to achieve our goals - namely, support for indexing `MultiPolygons`.

Using PostGIS, I designed and built a number of low-latency, high-throughput services to analyze geolocation information and determine events based on [OpenStreetMap (OSM)](https://www.openstreetmap.org/) data **(this data set was also the foundation for the popular map and navigation app Waze).** I used [osmosis](https://github.com/openstreetmap/osmosis) (a tool for interfacing with the OSM data and processing it into GeoJSON format) to extract `MultiPolygon` info for buildings and regions. 

I created a table of `regions` which included the `MultiPolygon` in a column of the type geom. I then indexed this geometry field so that we could query with coordinates and receive results with regions that the coordinates intersected with. **This provided us with the backend service we needed to take coordinates and return place names in our UI.**

#### Batching queries for place names
After working at Banjo, I'll never forget that 37,-122 are the coordinates for a park in Santa Cruz, or that 0,0 represents the Atlantic ocean off the southern coast of Ghana. 

With `MultiPolygons` for all of the administrative boundaries around the world indexed with PostGIS, I exposed the data to web and mobile clients through a JSON API. This API provided a reverse geocoding service that could be queried in batches of 50 to provide names of places based on the coordinates in order, which rendered place names to users. **So instead of 20 million queries a day, we did 400,000 in batches of 50.**

### Saving $29M annually in reverse geocoding queries

Google offers a reverse geocoding service, but using it to reverse geocode millions of social posts each day would have cost more money than the feature was worth. Today, Google's service costs $4 per 1,000 queries. **Back then, we were running 20 million queries each day, which would cost $80,000 daily, or $29 million annually. Currently, there are many more than 20 million geocoded social media posts per day, making the potential costs even higher.**  

## Optimizing database performance with caching 
To optimize our database operations at Banjo, I focused on reducing the CPU load caused by intensive geoqueries. These are very CPU-intensive operations, even with proper indexing and batching of queries. Implementing caching was crucial to alleviate the strain on our Postgres database and reduce overall costs. 

### Implementing Redis for efficient caching

To achieve these optimizations, I built a Redis-based cache. **The solution was based on devising a cache key that offered a high hit-to-miss ratio while still providing the correct place names for the coordinates.** This allowed for higher throughput with less pressure on the database and minimal load on the Redis server, all while retaining enough precision for boundary intersections.

By rounding coordinates to the nearest four (11.112 meters) or five (1.112 meters) decimal places, I was able to ensure precision and efficiency in retrieving results. 

<script src="https://gist.github.com/TonsOfFun/fa340776be31838e794b681878276086.js"></script>
>Here's an example with a baseball field in San Francisco: rounding coordinates to four decimal places was sufficient to keep the cache accurate within the field’s boundaries.
>

This strategy significantly increased throughput while minimizing database pressure and Redis server load.

### Building a microservive architecture

**To house this system, we developed a Ruby/Sinatra application integrated with Redis and Postgres.** We didn't require a full Rails application - a Sinatra application was enough, because it simply needed to check the cache, return a query, cache the result, and return the result. 

While the application code could be implemented in any language, Redis as a cache and PostGIS as the geoindexing and querying layer were the optimal tools for the job. 

The Redis cache key using coordinates rounded to four decimal places and paired with JSON objects of place names and coordinates helped us achieved an impressive hit rate and significantly reduced the load on both Redis and Postgres servers. Additionally, it was able to efficiently store the results of `Polygon` queries, further easing the burden on the Postgres server.

This microservice architecture, consisting of a dedicated application server, cache, and database, was very cost-effective, allowing us to handle millions of daily requests with minimal operational costs.

> Update the redis example to support batching

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

## Developing event detection as a service

At Banjo, I leveraged PostGIS's advanced spatial indexing support to provide a more efficient index for performing geoqueries like [geo intersection queries](http://postgis.net/workshops/postgis-intro/spatial_relationships.html#st-intersects-st-disjoint-st-crosses-and-st-overlaps). This was crucial for identifying events based on geographical data.

### Understanding geo intersections

Geo intersection involves pinpointing when one geometry intersects with another. For example, if you posted on Instagram from a Taylor Swift concert at the Levi's Stadium, your post coordinates would be within the boundaries of the Levi's Stadium polygon. 

Our system at Banjo utilized these geo intersections to detect events. Posts made within a venue's boundaries during a specific event, even without directly mentioning the event, were identified as part of that event. This method allowed us to detect events without relying on scheudles from all of the venues around the world. We then employed [NLP (Natural Language Processing)](https://en.wikipedia.org/wiki/Natural_language_processing) in order to gleam the context from the geo feed of the venue. 

### Using NLP for contextual analysis

We further enhanced our service by integrating Natural Language Processing (NLP). This allowed us to glean deeper insights from the geographic data of venues. 

**More than just showing users what events were happening nearby, this helped transform Banjo into a powerful tool that was later used by news organizations and local governments to provide context for natural disasters, security threats, and other unexpected events.**

### Installing PostGIS for spatial querying

To support our event detection system, PostGIS was essential. This extension, added to PostgreSQL, enables complex location queries using SQL. 

In order to use PostGIS, you need to install both PostgreSQL and the PostGIS extension. The PostGIS extension is installed by running the `CREATE EXTENSION` command from the `psql` command line or from the `CREATE EXTENSION` command in a SQL script.


```sql
CREATE EXTENSION postgis;
SELECT POSTGIS_VERSION(); # succeeds if PostGIS objects are present.
```

PostGIS's spatial querying capabilities extend beyond geo intersections, offering functions like nearby, within, and distance - which can be found here.

### In-house reverse geocoding
The geoqueries to support Banjo's event detection system used [ST_intersect](https://postgis.net/docs/en/ST_Intersects.html) to determine the spatial relationships with [ST_AsGeoJSON](https://postgis.net/docs/en/ST_AsGeoJSON.html) used to render [GeoJSON](https://geojson.org/) from the geometry fields indexed using [GIST](http://postgis.net/workshops/postgis-intro/indexing.html) and [ST_GeomFromGeoJSON](https://postgis.net/docs/en/ST_GeomFromGeoJSON.html) to query geometry fields from GeoJSON.
 

```sql
SELECT ST_AsGeoJSON(geom) FROM districts WHERE ST_Intersects(geom, ST_GeomFromGeoJSON('{"type":"Point","coordinates":[-122.431297,37.773972]}'));
```

This query provides results for districts that intersect with the queried GeoJSON coordinates. 

## Conclusion
With a comprehensive geoindexed dataset, we built a system capable of detecting significant social media activity at specific venues within a given timeframe. 

My role at Banjo, working alongside data science and client teams, contributed significantly to the company's growth to a $1B+ valuation. This work not only impacted our company but also provided valuable tools for local governments and news organizations, and I am grateful for the experience and opportunity to have worked with such a talented team of engineers. 
