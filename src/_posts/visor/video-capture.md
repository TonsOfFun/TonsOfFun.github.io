---
layout: post
published: false
title:  Capturing video for realtime computer vision
date: 2023-08-02
datetime: August 2, 2023
description: Processing video streams in realtime presents a unique set of challenges... 
categories: 
    - visor
tags:
    - ml
    - cv
---

```python
import cv2
import queue
import threading

frame_queue = queue.Queue()

def read_frames(cap):
    while True:
        ret, frame = cap.read()
        frame_queue.put(frame)

threading.Thread(target=read_frames, args=(cap,)).start()

while True:
    if not frame_queue.empty():
        frame = frame_queue.get()
        processed_frame = some_processing_function(frame)
        cv2.imshow('Processed Feed', processed_frame)
```
## Processing images takes time
One of the biggest challenges is processing every frame without them queuing up and lagging behind. 
Having a constant framerate turns out to be a gift and a curse. 
This turns out to also be a benefit that can be used to model the requirements of the application.

The framerate determines our offered traffic

Instead of reimplementing solutions

It might take seconds on CPU and milliseconds on GPU, but how fast is fast enough. Depending on the frame rate you need to run the processing at you can determine the maximum service time required to process in realtime without missing data. 

### We want to capture frames from video for analysis
Say you need to perform a task on every frame and the frame rate is 24 FPS. This means that in 1000ms you need to perform the task 24 times. 24 jobs go into 1000ms 41.67 times, so you have 41ms to perform the function or your will lag behind realtime.

### Using OpenCV we can capture frames and run
OpenCV is *the* standard library for computure vision  processing. It's feature set includes capturing frames from videos, running neural networks, manipulating images, writing videos, and much much more.

### What? (maybe link to the final solution?)
Ok, so we can just use OpenCV and we should be fine
## Security camera that detects if a person is in frame
### You want to make a camera that detects people
### You have to read each frame and run a detector
### You create capture class to reads the frames
### You run inference to detect people in each frame
## Naive Code Example, to provide aid the premise (How? suboptimal)
### Encode, detect, do something
Reading the frame
Detection
Log the detection
### Solution
### Detections take time
If the inference time takes longer than the interval between frames, you'll miss frames and miss people
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


# ChatGPT Draft
## Intro: Seamless Streaming: The Art of Lag-Free RTSP Feeds
### The Battle Against Buffer
In the age of real-time surveillance and analytics, a lagging camera feed is unacceptable.

### Untangling the Knot
Using OpenCV to process RTSP feeds is straightforward, but what happens when processing time exceeds the frame interval?

### A Glimmer of Genius
Enter threading with queue buffering, a promising remedy for the lagging dilemma.

## Background: RTSP & OpenCV: A Powerful Yet Tricky Duo
### A World Watching
With RTSP, surveillance systems stream video over the internet, but real-time processing demands can bottleneck the feed.

### Mission Statement
Deliver smooth, uninterrupted RTSP streams while performing on-the-fly video analytics.

### Initial Configuration
Using OpenCV's VideoCapture method to tap into the RTSP feed.

### The Speed Bump
While efficient, certain processing tasks on frames led to noticeable lags.

```python
import cv2

cap = cv2.VideoCapture('rtsp://username:password@camera_ip:port/streaming/channels/1')

while True:
    ret, frame = cap.read()
    # Some processing on the frame
    cv2.imshow('Live Feed', frame)
```
Initial Approach: A Straightforward Struggle
Juggling Frames
Reading and processing on a single thread means sometimes missing out on new frames.

The Direct Route
Reading frames and processing them sequentially.

```python
while True:
    ret, frame = cap.read()
    processed_frame = some_processing_function(frame)  # This takes time
    cv2.imshow('Processed Feed', processed_frame)
```

### Reality Check
The time taken by some_processing_function might exceed the frame interval, causing lag.

## Learning Curve: Threading - The Beacon of Buffering
### Double Duty
Using one thread to read frames and another to process ensures no frame is missed.

### The Multi-Threaded Magic
Introducing Python's threading module alongside a queue to store frames for processing.

```python
import cv2
import queue
import threading

frame_queue = queue.Queue()

def read_frames(cap):
    while True:
        ret, frame = cap.read()
        frame_queue.put(frame)

threading.Thread(target=read_frames, args=(cap,)).start()

while True:
    if not frame_queue.empty():
        frame = frame_queue.get()
        processed_frame = some_processing_function(frame)
        cv2.imshow('Processed Feed', processed_frame)
```
### Eureka with a Caveat
Frame reading and processing are decoupled, but care is needed to ensure the queue doesn’t overflow if processing is too slow.

## Elevated Approach: Perfecting the Processing Pipeline
### A Harmonious Balance
Keeping a check on the queue size ensures it doesn't become too large, which can cause memory issues or too much delay between reading and displaying.

### Refined Code with Controls
```python
MAX_QUEUE_SIZE = 10

def read_frames(cap):
    while True:
        ret, frame = cap.read()
        if frame_queue.qsize() < MAX_QUEUE_SIZE:
            frame_queue.put(frame)

# The rest remains similar
```
### Guardrails in Place
This approach ensures smooth streaming but requires tuning based on the specific processing demands and system resources.

## Resource Guide: GitHub's Advanced RTSP Stream Processor
### Pre-Flight Checklist
You'll need OpenCV installed, and an understanding of Python's threading module will help.

### Dive into the Deep End
Comprehensive documentation and code snippets await, tailored for real-world applications.

### Happy Streaming, Responsibly
While this solution addresses lag, always monitor system resources and adjust the MAX_QUEUE_SIZE accordingly.

## Wrap-Up: Real-Time Processing for Real-Time Streams
### Why This Matters
In surveillance and analytics, every frame counts. Lag compromises data integrity and user trust.

### The Road Travelled
From single-threaded simplicity to multi-threaded mastery, the journey was filled with lessons and breakthroughs.

### Next Gen Surveillance
Armed with OpenCV and Python's threading magic, developers are now poised to create advanced real-time video analytics systems with confidence.