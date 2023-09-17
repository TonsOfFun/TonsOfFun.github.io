---
layout: post
published: false
title:  Some engaging title
date: 2022-09-11
datetime: Month DD, YYYY
description: Some engaging description to go with the title and content all with SEO in mind
categories: 
    - visor
    - ml
    - cv
---

## Intro header, to hook the reader (Why, How, What)
### Why?
### How?
### What? (maybe link to the final solution?)
## Background header, to provide context (Why?)
### Situation
### Task
### Action
### Result
## Naive Code Example, to provide aid the premise (How? suboptimal)
### Considerations
### Solution
### Issues
## Experience, to provide reasoning against the naive solution and context for the premise of the refined solution (What? revisit why and how then discuss what the experience was)
### Situation
### Task
### Action
### Result
## Refined Example, to provide an optimal solution to the premise (How?)
### Considerations
### Solution
### Issues
## Link to resource with solution (GitHub repo like VisorCV)
### Considerations
### Solution
### Issues
## Conclusion, recap (Why, How, What)
### Why?
### How?
### What?

```
import ray
import redis

# Create a Redis server
redis_server = redis.Redis()

# Configure Ray to use Redis
ray.init(redis_address=redis_server.host, redis_password=redis_server.password)

# Create an actor that shares memory
@ray.actor(redis_address=redis_server.host, redis_password=redis_server.password)
class MyActor:
    def __init__(self):
        self.x = 1

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

# Create an actor and set its x attribute
actor = MyActor.remote()
actor.set_x.remote(2)

# Get the actor's x attribute
x = actor.get_x.remote()

print(x)
```

```
import multiprocessing
import time
import ray
import numpy as np
import os
import sys


NUM_WORKERS = multiprocessing.cpu_count()
# ray init can take 3 seconds or more to load
ray.init(num_cpus=NUM_WORKERS)
np.random.seed(42)
IMAGE_DIMENSIONS = (1920,1080)
image_data = np.random.randint(0, high=255, size=(IMAGE_DIMENSIONS[0], IMAGE_DIMENSIONS[1], 3), dtype=np.uint8)

@ray.remote
def np_sum_ray2(obj_ref, start, stop):
    return np.sum(obj_ref[start:stop])

  
def benchmark():
    # chunk_size = int(ARRAY_SIZE / NUM_WORKERS)
    futures = []
    obj_ref = ray.put(image_data)
    start_time = time.time_ns()
    for i in range(0, NUM_WORKERS):
        # start = i + chunk_size if i == 0 else 0
        ray_image_data = ray.get(obj_ref)
        # futures.append(np_sum_ray2.remote(obj_ref, start, i + chunk_size))
    # results = ray.get(futures)
    (time.time_ns() - start_time) / 1_000_000



start_time = time.time_ns()
ray_image_data = ray.get(obj_ref)
(time.time_ns() - start_time) / 1_000_000

(ray_image_data == image_data).all()
print(sys.getsizeof(ray_image_data)/1024/1024)
print(sys.getsizeof(image_data)/1024/1024)
```