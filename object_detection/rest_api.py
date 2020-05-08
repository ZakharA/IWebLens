from flask import Flask, g
from flask import request
from object_detection import Object_detection
import time
from datetime import datetime

app = Flask(__name__)
app.debug = True


@app.before_request
def before_request_func():
    g.request_start_time = time.time()
    app.logger.info("started processing at {}".format(
        datetime.fromtimestamp(g.request_start_time)))
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.after_request
def after_request(response):
    app.logger.info("finished processing request {} / ".format(
        time.time() - g.request_start_time, datetime.fromtimestamp(time.time())))
    return response


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
    app.run(host='0.0.0.0', port=1025, threaded=True)
