import os
import time
import json
import cv2
import numpy as np


class object_detection:
    def __init__(self, image):
        self.objects = {"objects": []}
        self.image = image
        self.labels = open(
            "yolo-coco/coco.names").read().strip().split("\n")
        self.weightsPath = os.path.abspath(
            'yolo-coco/yolov3-tiny.weights')
        self.configPath = os.path.abspath(
            'yolo-coco/tiny.cfg')
        self.initiate_net()

    def initiate_net(self):
        self.net = cv2.dnn.readNetFromDarknet(
            self.configPath, self.weightsPath)

    def convert_to_blob(self):
        npimg = np.fromstring(self.image, np.uint8)
        # convert numpy array to image
        image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        (self.H, self.W) = image.shape[:2]
        return cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)

    def run_net(self, blob):
        self.net.setInput(blob)
        ln = self.net.getLayerNames()
        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.layerOutputs = self.net.forward(ln)

    def process_result(self):
        boxes = []
        confidences = []
        classIDs = []

        for output in self.layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > 0.5:
                    box = detection[0:4] * \
                        np.array([self.W, self.H, self.W, self.H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    self.objects["objects"].append(
                        {"label": f"{self.labels[classID]}", "accuracy": f"{confidence:.2f}"})
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        self.idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    def detect_objects(self):
        blob = self.convert_to_blob()
        self.run_net(blob)
        self.process_result()
        return self.fromat_json()

    def fromat_json(self):
        return json.dumps(self.objects)


if __name__ == "__main__":
    object_detection = object_detection(
        "object_detection/inputfolder/000000012807.jpg")
    x = object_detection.detect_objects()
    print(x)
