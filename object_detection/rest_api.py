from flask import Flask
from flask import request
from object_detection import object_detection

app = Flask(__name__)


@app.route('/api/detection/', methods=['POST'])
def image_validation():
    error = None
    if request.method == "POST":
        images = request.files['files'].read()
        if images is None:
            error = "No image to process"
        else:
            net = object_detection(images)
            return net.detect_objects()
    else:
        error = "Invalid request"
        return error
