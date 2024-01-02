---
layout: post
published: true
title: GreenThumb IO
date: 2015-03-01
datetime: March 1, 2015
categories: career
tags:
  - ActionCable
  - OpenCV
  - PostGIS
  - PostgreSQL
  - Python
  - Starups
  - WebSockets
  - hackathons
  - raspberrypi
  - ruby-on-rails
  - sidekiq
---

## Intro to AgTech through a series of hacakthons
I founded GreenThumb.io after participating in a series of hackathons called Apps for Ag. I placed 3rd in the first hackathon in Coalinga, California. My placing in the second hackathon at UC Davis earned me the incorporation costs for GreenThumb, which were paid for by the event sponsor. I volunteered as an advisor and mentor for the participants in the third event of that series in Salinas.

### AgTech 101: intro to the union of agriculture and technology
Initially GreenThumb IO was designed in collaboration with agronomists to track records of consumables used by storing details in a geo-spatial index. This provided agronomists and farmers with location based feeds of notes and accumulated fertilizer and pestiside applications to ensure targets were met, tracked, and archived for reference.

### Cannabis computer vision application
GreenThumb became a computer vision product that was purpose built for monitoring cannabis plant health through [leaf area](/greenthumb/leaf-area) and [bud area](/greenthumb/bud-area/) analysis. 

![GreenThumb IO](https://res.cloudinary.com/tonsoffun/image/upload/v1697299678/greenthumb-graph_pc5wfd.gif)

### The vision
GreenThumb had enourmous potential for cultivators because it helps them to monitor their crops and identify potential problems early on. The product could also used by researchers to study plant growth and development. Ultimately I was only able to get the product in the hads of a few agronomists, but was unable to tap the large market with my limited self funding. I made the decision to put this dream on a self and take a full time role at Cainthus.

<img src="https://res.cloudinary.com/tonsoffun/image/upload/v1697302623/greenthumb-io_gmrbku.gif" alt="GreenThumb Timelapse" style="width: 720px;">

### The technology
I used Ruby, Rails, Sidekiq, Python, OpenCV, Postgres, PostGIS, Redis, Raspberry Pi, WebSockets - ActionCable (AnyCable-Go) to build the product. I also used real-time image processing with Rails and Sidekiq, and custom Python OpenCV algorithms exposed in an image service via Thumbor OpenCV engine using Google Cloud Run (GCR) on Google Cloud Platform (GCP). I also used a Raspberry Pi to capture and preprocess images from a camera and send them to the server for further processing.


I am proud of the work that I have done on GreenThumb. It is a product that has the potential to make a real difference in the world. I am excited to continue working on it as a part of showcase of computer vision applications built with VisorCV. It will be interesting to see how it will be received this time around.
