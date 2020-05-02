from flask import Flask
from flask import request
from object_detection import Object_detection

app = Flask(__name__)


@app.route('/api/object_detection', methods=['POST'])
def image_validation():
    error = None
    if request.method == "POST":
        image = request.files['image'].read()
        if image is None:
            error = "No image to process"
        else:
            net = Object_detection(image)
            return net.detect_objects()
    else:
        error = "Invalid request"
        return error


if __name__ == "__main__":
    app.debug = 1
    app.run(host='0.0.0.0', port=80, threaded=True)
