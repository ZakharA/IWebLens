from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/api/detection/', methods=['POST'])
def image_validation():
    error = None
    if request.method == "POST":
        images = request.files['files'].read()
        if images is None:
            error = "No image to process"
        else:
            pass  # TODO implement object detection
    else:
        error = "Invalid request"
        return error  # TODO return results
