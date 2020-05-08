FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get upgrade && \
    apt-get -y install python3 python3-pip libgtk2.0-dev

COPY *.py /src/
WORKDIR /src

RUN pip3 install flask numpy opencv-contrib-python opencv-python requests gunicorn gevent
ADD https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names yolo-coco/coco.names
ADD https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg yolo-coco/tiny.cfg
ADD https://pjreddie.com/media/files/yolov3-tiny.weights yolo-coco/yolov3-tiny.weights

EXPOSE 1025
CMD ["python3", "./rest_api.py"]