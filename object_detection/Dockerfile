FROM python:3.8
COPY . /src
WORKDIR /src
RUN pip install flask numpy opencv-contrib-python opencv-python requests
ADD https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names yolo-coco/coco.names
ADD https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg yolo-coco/tiny.cfg
ADD https://pjreddie.com/media/files/yolov3-tiny.weights yolo-coco/yolov3-tiny.weights
EXPOSE 5000
CMD ["python", "./rest_api.py"]
