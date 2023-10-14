---
layout: post
published: false
title:  Scaling Rails with Puma and Sidekiq on Heroku
date: 2022-09-11
datetime: September 11, 2022
description: Born and raised on the peninsula in the San Francisco Bay Area, I was fortunate to be exposed to both business and technology at a very young age. Video games were a huge influence on my interest in computers and programming. I used to play games like DOOM, Quake, Hexen, and Duke Nukem 3D at my dad's office with the tech support crew at the end of the work day. 
categories: 
    - deployment
tags:
    - performance
    - scaling
    - heroku
    - concurrency
    - ruby
    - rails
---

## Heroku Postgres
### Current Provision IOPs
https://devcenter.heroku.com/articles/heroku-postgres-production-tier-technical-characterization#performance-characteristics
2000 read/write operations per second. Even with more than 500 connections we cannot exceed the PIOPS or CPU load of our current DB tier. We need to continually work to improve query execution time (increase IOPS throughout by decreasing IO time) and query count (fewer IOPS) per web/job requests/transactions.
### Connection Limit
500 connections; this is the maximum for all tiers of Heroku Postgres
### Dyno Scaling Limitations
1 Web dyno uses 10 connection (2 processes x 5 threads) (WEB_CONCURRENCY=2)
1 Sidekiq dyno uses 5 connection (1 processes x 5 threads) (SIDEKIQ_COUNT=1)
We can use up to 50 web dynos (if we have 0 sidekiq dynos)
We can use up to 100 sidekiq dynos (if we have 0 web dynos)
We could run 25 web dynos with 50 sidekiq dynos
## PgBouncer
### Enabling PgBouncer
Set DATABASE_CONNECTION_POOL_URL to the appropriate connection pool attachment for our current production DB
Disabling PgBouncer
Change DATABASE_CONNECTION_POOL_URL to NO_DATABASE_CONNECTION_POOL_URL or remove the ENV entirely
Connection Limit
10,000 connections
Current Dyno Scaling Limitations
We are limited to 100 dynos by default.
On 2x Dynos
We could run 50 web and 50 sidekiq processes or any combination under 100
On P-L Dynos
We can run 8 puma processes per dyno (8 processes x 5 threads) (WEB_CONCURRENCY=8)
100 P-L web dynos would use 4,000 connections
We can run 8 sidekiq processes per dyno (8 processes x 5 threads) (SIDEKIQ_COUNT=8)
100 P-L sidekiq dynos would use 4,000 connections
Considerations for Massive Scale
PIOPS Limits
We are currently around our maximum PIOPS during high job throughput. Scaling our dynos beyond our PIOPS will incur significant performance degradation across DB operations.
vCPU
We are currently near our maximum CPU work load during heavy job processing. We currently have 4 vCPUs any load average above 4 will incur significant performance degradation.
Consider Thread Count
Current recommendations for Sidekiq and Puma are 5 thread on Heroku dynos of all sizes.
https://devcenter.heroku.com/articles/deploying-rails-applications-with-the-puma-web-server#recommended-default-puma-process-and-thread-configuration
Considering increasing dynos?
Be cautious and focus on CPU load and memory utilization metrics.
If we are hitting load averages above our vCPU count scale threads down.
If we are exceeding memory scale threads down.
In Case of Big Influx of Jobs
Sometimes users will introduce datasets that might reveal memory bloat issues such as unlimited none batched or paginated queries. In the emergency event of this happening to our web dynos change dyno type to P-L and adjust WEB_CONCURRENCY appropriately (down to provide for more memory per worker if needed)
Read only job queues
One method I’ve found effective is read only jobs. You can hear Kelly Sutton speak on his experience with this on Sidekiq in Practice episode 2. The idea is taking jobs which only need to read from the database and performing them on secondary databases. This is great for jobs that generate reporting dataset CSV files or index to a third party data store like elastic search. 

Consider file processing and storing thumbnails. Your paths can be constructed so there isn’t anything that needs persisting.  Often times you’ll also perform notification jobs after_commit, so weather you’re broadcasting. The problem can be idempotent considerations. Your file processing could safely be performed twice without consequence or check your bucket before processing a thumbnail, then you could enqueue a job to write back to the database once complete. For broadcasting to ActionCable you probably don’t want to send double notifications and while you could add some complexity with de duplication logic in your frontend code, it might be safer to persist checkpoints for SQL readonly jobs to a separate Redis configured for LRU key eviction or another LRU cache service. Do not do this with Redis side locking, if you find yourself needing to lock records lock on the SQL primary to ensure jobs are performed only once. 
