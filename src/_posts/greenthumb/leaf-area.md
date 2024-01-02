---
layout: post
published: true
title: GreenThumb Leaf Area Analysis
description: In this blog post, we'll dive into a fascinating application of computer vision to analyze plant growth with OpenCV. We'll walk through the code and techniques used to measure the growth of plants over time.
image_url: https://miro.medium.com/v2/resize:fit:720/format:webp/1*IjHOnf9J_k7-kbel4AXEKA.jpeg
date: 2018-05-22
datetime: March 1, 2015
categories: greenthumb
tags:
  - OpenCV
  - Python
  - greenthumb 
  - GoogleColab
  - Docker
  - iPythonNotebook
  - matplotlib
---
> This blog was originally published on [Medium](https://medium.com/greenthumbio/cannabis-leaf-area-analysis-d6449dbda07f).

## Intro

In this post I'm going to show you how to use openCV and some basic HSV color space analysis used to mask out non leaf pixels. We can use the mask to measure the leaf area in pixels. You can use basic trig to find out the pixel to millimeter value using the distance and angle of the field of view. I've broken my Jupiter notebook into smaller pieces to overcome the limitations of medium's support for rendering long notebooks (though it did seem to render fine on mobile, I couldn't see it properly on my MacBook Pro using Chrome). Anyway, I also have a full version of the [notebook](https://gist.github.com/TonsOfFun/9ed35c29de2ef32884b7e5cea4144c2e) available for anyone interested.

![Leaf Area Analysis](https://miro.medium.com/v2/resize:fit:720/format:webp/1*IjHOnf9J_k7-kbel4AXEKA.jpeg)

## Dependencies
We're going to utilize the imutils convenience package to resize the images for processing as well as for finding our HSV calibration values. OpenCV will be used for preprocessing the image and pixel selection by range. We use matplotlib is used from rendering images and graphs.

```python
import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt
%matplotlib inline 
```

## Leaf Masking
This is a basic function that converts the BGR (OpenCV is BGR, not RGB) image to HSV. Using the `leaf_lower` and `leaf_upper` HSV colorspace values defined using the range-detector helper tool found in imutils. These calibration settings work on both of my NestCams situated under the same type of HPS light. This is basically pulled from this PyImageSearch article on tracking a green ball.

```python

# Defined bounds using https://github.com/jrosebr1/imutils/blob/master/bin/range-detector
leaf_lower = (29, 0, 0)
leaf_upper = (255, 255, 128)

def leaf_mask(bgr_image):
    frame = imutils.resize(bgr_image, width=500)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, leaf_lower, leaf_upper)
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=2)
    return mask
```

The erosions and dilations are to cleanup any smaller blobs picked up by the HSV range. In the next blogpost we will go over how to do additional filtering by analyzing the contours and their sizes. I'm not going to apply that here since the results of the post processing on the mask seem adequate for this stage. We will be replacing this model with a custom trained TensorFlow maks RCNN model. Checkout this blogpost on making a toy detector that can output a pixel-wise mask.

<script src="https://gist.github.com/TonsOfFun/e2e283b3a229a898e0fae217c276e48b.js"></script>

You can see the function working on the two sample images, above from week one and below from week 2. They represent the plants at two time periods 5 days apart. Now let's checkout what insights the data has to offer.

<script src="https://gist.github.com/TonsOfFun/ececab5fd38f1db618847e7431a284f2.js"></script>

## Health Reports and Graphs
Below you can checkout a leaf growth report. 10 square inches or 30 square centimeters of growth assuming our camera was hung at the correct height and give or take some variance due to inconsistent leaf distances from the lens. This gives a cultivator great insight into the general health of their crop just by graphing growth. You might also notice that I scaled the images down for processing so the results would have to be scaled up proportionately. That's an exercise for another time as this post is just to get the concept of monitoring and graphing plant growth with smart cameras.

We can now have the ability to provide reports on performance as well as alerts when growth has plateaued or even dropped off which is a clear sign of stress in any plant. We can also provide historical performance reviews so a cultivator can see how the current crop is vegging in comparison with previous crops at the same stage of growth.
Let's plot these data points from our two leaf area analyses. Since we only have our two data points from this time series our line graph will be a little boring, but you can imagine the growth being more engaging when plotting a point every minute instead of every 5 days. A realtime growth chart would include oscillations from the circadian rhythms induced by the light cycles, as well as fluctuating from variable environmental conditions. The decentralized AI will have to compensate for variability dynamically at each camera.

<script src="https://gist.github.com/TonsOfFun/4b4a7a0f6d4708ba46a89c457c41a115.js"></script>

With this functionality we increase the farmers awareness of problem areas in there grow sites and give them metrics to back their business's performance overtime. We can now take photos of cannabis plants and produce metrics on our devices. It's the first step on our path to a decentralized cannabis AI and there is enormous potential value in a trusted data source of cannabis cultivation metrics from seed to harvest. I'll be putting out an article later this month talking about GreenThumb IO's plans to empower the farmers with their own crop data with GTIO Security Tokens.

<script src="https://gist.github.com/TonsOfFun/9ed35c29de2ef32884b7e5cea4144c2e.js"></script>

![cannabis leaves](https://miro.medium.com/v2/resize:fit:720/format:webp/1*jc0efTe4Ug77dOpmlj4T3A.jpeg)