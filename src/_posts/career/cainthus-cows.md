---
layout: post
published: false
title: Cainthus Cows - Real-time Computer Vision for Animal Health
date: 2017-04-01
datetime: April 1, 2017
categories:
  - career
tags:
  - Python
  - startups
  - celery
  - django
  - mongodb
  - reactjs
  - redis
---

https://www.onecup.ai/
https://ever.ag
https://dairy.com

[Cainthus.com](https://cainthus.com) was acquired by [ever.ag](https://ever.ag) and is now [dairy.com](https://dairy.com).

## Extreme pivot to dairy cow monitoring
When Cainthus decided to pivot away from drone analytics to dairy cow monitoring it was one of the most extreme shifts in product market fit I've ever seen, yet it was also one of the most successful. The business leadership at Cainthus was a pair of Irish twin brothers Ross and David Hunt. Ross Hunt was a former accountant and the CFO, while David Hunt was a former banker and the CEO. Ross proved to be a very tech savy financial operator and he was a vital partner in the development of the technology and infrastructure requirements of the dairy barn computer vision systems.

### Product market fit: attracting the attention of investors and dairy farmers
David Hunt was able to attract the attention of Cargill's Animal Nutrition VC firm that was keenly interested in the dairy barn monitoring product. In addition to my technical work, I also handled the tech due diligence for Series B fundraising. This was a great opportunity to learn about the business side of things.

## Beta barns around the globe
I led the team develop our dairy barn AI analytics platform using realtime computer vision processed on-premise on farms in Italy, Spain, France, Ireland, Canada, and across the US. This was another exciting project, and we were able to develop a product that helped dairy farmers improve their operations by monitoring their cow health through eating and drinking behaviors.

![Cow Computer Vision](https://res.cloudinary.com/tonsoffun/image/upload/v1696214621/vo78h9qubtv13xjj4sjs.png)

We were tasked with building a system that could monitor 100s of cows through networks of dozens of PoE cameras to detect, identify, and observe the eating and drinking behavior of the dairy cows.

# The computer vision platform
## The algorithm
### Cow Face Detector: HAAR Classifier
### Cow Hustle: Eigenfaces for cow face recognition
Principal Component Analysis (PCA) was used to generate eignenvectors for cow faces. The eigenfaces were used to train a Support Vector Machine (SVM) classifier to identify individual cows by their faces. This was a very challenging problem because the cows were often in motion and the lighting conditions were not ideal. We were able to overcome these challenges by using a combination of image processing techniques and machine learning algorithms.


### Cow Eating and Drinking: Optical flow
### 


## The Python OpenCV application
Having had experience with large scale image processing in the past, including <%= link_to('the cainthus drone platform', '_posts/career/cainthus-drones.md') %> and <%= link_to('greenthumb', '_posts/career/greenthumb.md') %>, I started designing the software architecture and infrastructure required to achieve our goals. I was able to leverage my experience with distributed systems and computer vision to design a system that could process the video streams from the cameras in real-time. Power over Ethernet (PoE) cameras provide RTSP streams that we could process with OpenCV and Tensorflow to detect and identify the cows. We used MongoDB for interprocess communication (IPC) and to store the results of the computer vision processing. We used Celery with Redis as a message broker backend to distribute the processing across multiple CPU processes and GPUs. 

## The web application
We used Rails to build a web application to serve an API for a ReactJS frontend designed report the results of the computer vision processing.

I am proud of the work I did at Cainthus, and I am grateful for the opportunity to have worked with such a talented team. I learned a lot during my time there, and I am excited to use my skills and experience to make a positive impact in the world.

Here are some of the key highlights of my time at Cainthus:
Led a team to engineer a product for drone flight mapping and analysis with heat map overlays for agronomists.
Led team developing dairy barn AI analytics using computer vision.
Grew global remote team from 1 to 8 data scientists, engineers, and designers.
Handled the tech due diligence for Series B fundraising with Cargill Animal Nutrition for the dairy barn monitoring product.
Developed distributed Computer Vision microservices (OpenCV, Numpy, Scipy, SciKitLearn) to process agriculture drone imagery on the cloud (Heroku, AWS, and Docker).
Designed, developed & troubleshot dockerized on-premise Python/C++ intensive datapipelines able to process online multiple 10 FPS 4k IP cameras videostreams , using OpenCV, Gstreamer pipelines, Redis for IPC, GPU based Tensorflow-serving/NVIDIA TensorRT deep learning framework using docker-compose, docker Swarm and Ansible.
Improved Engineering Processes with Continuous Integration and Continuous Deployment (CI/CD) pipelines including static code analysis and end-to-end tests.
I am confident that my experience at Cainthus has prepared me for the next chapter in my career. I am excited to see what the future holds!
