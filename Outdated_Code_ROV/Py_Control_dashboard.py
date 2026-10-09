from base64 import encode
import sys
import time
import os
sys.path.append('/usr/local')
from flask import Flask, Response, redirect, request, url_for
from flask import render_template
import threading
import argparse
import datetime
import imutils
import cv2
import json
import numpy as np
import requests
import threading
import uuid
from modules.rov_streamer.rov_streamer import RovCamStreamer, RovVideoStreamer, RovVisionStreamer, CAMVIEW
from modules.rov_vision.rov_vision import RovVision

BRAIN_IP = "192.168.1.50"

# line direction class
class DIRECTION:
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2

# video stream resolution
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

# computer vision library functions
vision = RovVision()

# video stream references
ref_dome: RovCamStreamer = None
ref_down: RovCamStreamer = None
ref_front_right: RovCamStreamer = None
ref_front_left: RovCamStreamer = None
ref_morts: RovVideoStreamer = None

# initialize the flask web application
app = Flask(__name__)

@app.route("/")
def index():
	# return the rendered template
	return render_template("dashboard.html")

@app.route("/all", methods = ['GET'])
def all():
    return render_template("all_videos.html")

@app.route("/dashboard", methods = ['GET'])
def dashboard():
    return render_template("dashboard.html")

@app.route("/docking", methods = ['GET'])
def docking():
    return render_template("docking.html")

@app.route("/dome", methods = ['GET'])
def dome():
    return render_template("dome.html")

@app.route("/down", methods = ['GET'])
def down():
    return render_template("down.html")

@app.route("/fishlength", methods = ['GET'])
def fishlength():
    pass

@app.route("/front_left", methods = ['GET'])
def front_left():
    return render_template("front_left.html")

@app.route("/front_right", methods = ['GET'])
def front_right():
    return render_template("front_right.html")

@app.route("/morts", methods = ['GET'])
def morts():
    return render_template("morts.html")

@app.route("/mosaic", methods = ['GET'])
def mosaic():
    return render_template("mosaic.html")

@app.route("/mosaic_reset", methods = ['POST'])
def mosaic_reset():
    folder = '/home/brain/static/mosaic'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return render_template("mosaic.html")

@app.route("/mosaic_snap", methods = ['POST'])
def mosaic_snap():
	# grab global references to the output frame and lock variables
    global ref_down

    if ref_down is not None:
        pic = request.form["pic"]
        if pic is not None:
            print(f"snap pic: {pic}")
            ref_down.snap(pic)

    return render_template("mosaic.html")

@app.route("/mosaic_stitch", methods = ['POST'])
def mosaic_stitch():
    folder = '/home/brain/static/mosaic'
    images = []
    
    try:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            img = cv2.imread(file_path, 0) 
            images.append(img)
    
        if (len(images) == 8):
            RovVision.stitch(images, "/home/brain/static/mosaic/mosaic.jpg")
    except:
        pass

    return render_template("mosaic.html")

@app.route("/stereo", methods = ['GET'])
def stereo():
    return render_template("stereo.html")

@app.route("/transect_red", methods = ['GET'])
def transect_red():
    return render_template("transect_red.html")

@app.route("/transect_endurance", methods = ['GET'])
def transect_endurance():
    return render_template("transect_endurance.html")

@app.route("/view_docking")
def view_docking():
    global ref_front

    # return the response generated along with the specific media type (mime type)
    if ref_front is not None and ref_front.initialized:
        frame = RovVisionStreamer.generate_docking(ref_front)
        return Response(frame, mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_dome")
def view_dome():
    global ref_dome

    # return the response generated along with the specific media type (mime type)
    if ref_dome is not None and ref_dome.initialized:
        return Response(ref_dome.generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_down")
def view_down():
    global ref_down

    # return the response generated along with the specific media type (mime type)
    if ref_down is not None and ref_down.initialized:
        return Response(ref_down.generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_front_left")
def view_front_left():
    global ref_front_left

    # return the response generated along with the specific media type (mime type)
    if ref_front_left is not None and ref_front_left.initialized:
        return Response(ref_front_left.generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_front_right")
def view_front_right():
    global ref_front_right

    # return the response generated along with the specific media type (mime type)
    if ref_front_right is not None and ref_front_right.initialized:
        return Response(ref_front_right.generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_morts")
def view_morts():
    global ref_morts

    # return the response generated along with the specific media type (mime type)
    if ref_morts is not None and ref_morts.initialized:
        return Response(ref_morts.generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_stereo")
def view_stereo():
    global ref_front_left, ref_front_right

    # return the response generated along with the specific media type (mime type)
    if ref_front_left is not None and ref_front_left.initialized and ref_front_right is not None and ref_front_right.initialized:
        return Response(RovVisionStreamer.generate_stitched(ref_front_left, ref_front_right), mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_transect_red")
def view_transect_red():
    global ref_front

    # return the response generated along with the specific media type (mime type)
    if ref_front is not None and ref_front.initialized:
        frame = RovVisionStreamer.generate_transect_red(ref_front)
        return Response(frame, mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

@app.route("/view_transect_endurance")
def view_transect_endurance():
    global ref_front

    # return the response generated along with the specific media type (mime type)
    if ref_front is not None and ref_front.initialized:
        frame = RovVisionStreamer.generate_transect_endurance(ref_front)
        return Response(frame, mimetype = "multipart/x-mixed-replace; boundary=frame")
    else:
        return None

def get_sensor_data():
    try:
        url = f"http://{BRAIN_IP}:5000/controller/sensors"
        response = requests.get(url)
        result = json.loads(response.text)

        if "data" in result.keys():
            data = result["data"]
            depth = data["depth"]
            pressure = data["pressure"]
            temperature = data["temperature"]
            return depth, pressure, temperature
        elif "error" in result.keys():
            print(result["error"])
            return 0, 0, 0
    except:
        return 0, 0, 0

def sensor_thread():
    depth = []
    pressure = []
    temperature = []
    while True:
        time.sleep(5)
        try:
            depth, pressure, temperature = get_sensor_data()
            depth.append(depth)
            pressure.append(pressure)
            temperature.append(temperature)
            print(f"Depth: {depth}, Pressure: {pressure}, Temperature: {temperature}")
        except:
            pass

# helper function that stitches the two front camera images into a single image
def stitch_frames(img1, img2):
    stitched_img = None
    images = []

    images.append(img1)
    images.append(img2)

    # initialize OpenCV's image stitcher object and then perform the image stitching
    # print("[INFO] stitching images...")
    stitcher = cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)

    # if the status is '0', then OpenCV successfully performed image stitching
    if status == 0:
        stitched_img = stitched
    # otherwise the stitching failed, likely due to not enough keypoints being detected
    else:
        print("[INFO] image stitching failed ({})".format(status))

    return stitched_img

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # create all streams
    pipeline = 'udpsrc port={0} caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! avdec_h264 ! videoconvert ! appsink drop=1'
    # pipeline_front_left = 'udpsrc port=5600 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! avdec_h264 ! videoconvert ! appsink drop=1'
    # ref_front_left = RovCamStreamer(CAMVIEW.FRONT_LT, pipeline_front_left)

    pipeline_front_right = pipeline.format('5600')
    ref_front_right = RovCamStreamer(CAMVIEW.FRONT_RT, pipeline_front_right)

    pipeline_dome = pipeline.format('5601')
    ref_dome = RovCamStreamer(CAMVIEW.DOME, pipeline_dome)

    pipeline_down = pipeline.format('5602')
    ref_down = RovCamStreamer(CAMVIEW.DOWN, pipeline_down)

    # ref_morts = RovVideoStreamer("/home/files/fish12.mp4")

    # start sensors thread
    # sensors = threading.Thread(target=sensor_thread)
    # sensors.daemon = True
    # sensors.start()

    # start the flask app
    print("Starting web server ...")
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True, use_reloader=False)