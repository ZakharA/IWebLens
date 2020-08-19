
## Table of contents
* [Project description](#project-description)
* [Technologies](#technologies)
* [Setup](#setup)


## Project description
 IWeblens allows end-users to send an image via http request to a web service hosted in a Docker container and receive a list of objects detected in their
uploaded image.The project makes use of YOLO  and OpenCV to perform required image
operations/transformations and object detection.Additionally, Kubernetes is used as the container orchestration system.The object
detection web service is also designed using a RESTful API that can use Python’s FLASK library. 

 
## Technologies
Project is created with:
 * Python 3.6
 * Flask
 * OpenCV
 * YOLO tiny
 * Docker
 * Kubernetes

## Setup
To run this project:
1. use kind-config to konfigure k8s on a local machine
2. build an image using Dockerfile
3. configure k8s service using service.yaml
4. apply deployment.yaml
5. that's it, you can run test script to send images and recieve object with detected objects
