import sys
import logging
import os
sys.path.append('/usr/local/lib/python3.9/site-packages')
import time
from flask import Flask, request, jsonify, session
from dill import dumps, loads
from modules.br_thrusters.br_thrusters import Propulsion, SIGNAL
from modules.rov_sensors.rov_sensors import RovSensors

app = Flask(__name__)

# define session secret key
app.secret_key = 'rovsabrain4e22022!Ew@@pvit'
logger = None
thrusters = None
propulsion = None
sensors = None

@app.get("/controller")
def get_controller():
    return { "status": 200, "data": {"message": "Hello from PVIT ROV!"} }, 200

@app.get("/controller/depth")
def get_depth():
    try:
        depth = sensors.getDepth(True)
        logger.info(f"Depth: {depth}")
        return { "status": 200, "data": { "depth": depth } }, 200
    except:
        message = "Unable to get depth."
        logger.error(message, exc_info=True)
        return { "status": 500, "error": message }, 500

@app.get("/controller/pressure")
def get_presssure():
    try:
        pressure = sensors.getPressure(True) 
        logger.info(f"Pressure: {pressure}")
        return { "status": 200, "data": {"pressure": pressure} }, 200
    except:
        message = "Unable to get pressure."
        logger.error(message, exc_info=True)
        return { "status": 500, "error": message }, 500

@app.get("/controller/sensors")
def get_sensors():
    try:
        depth, pressure, temperature = sensors.getSensors(True)
        logger.info(f"Sensors: {depth}(depth), {pressure}(pressure), {temperature}(temperature)")
        return { "status": 200, "data": { "depth": depth, "pressure": pressure, "temperature": temperature } }, 200
    except:
        message = "Unable to get sensor data."
        logger.error(message, exc_info=True)
        return { "status": 500, "error": message }, 500

@app.get("/controller/temperature")
def get_tempature():
    try:
        temperature = sensors.getTempature(True)
        logger.info(f"Temperature: {temperature}")
        return { "status": 200, "data": {"tempetature": temperature} }, 200
    except:
        message = "Unable to get temperature."
        logger.error(message, exc_info=True)
        return { "status": 500, "error": message }, 500

@app.route("/controller", methods = ['POST'])
def set_controller():
    status = True
    try:
        if request.is_json:
            data = request.get_json()
            if "data" in data:
                status = data["data"]
                message = "Arduino not present"

                if propulsion != None:
                    status = propulsion.set_button_status(status)

                if status == True:
                    return { "status": "Ok", "data": {"message": "Ok"} }, 200
                else:
                    message = "Unable to set button state"
                    logger.error(message)
                    return { "status": "Error", "data": { "message": message } }, 500
            else:
                message = "No controller data"
                logger.error(message)
                return { "status": "Error", "error": message }
        else:
            status = request.form["data"]
            for key in status:
                if status[key] != 0:
                    logger.info(f"{key} = {status[key]}")

            return { "status": "Ok", "data": {"message": f"Received: {key} = {status[key]}"} }, 200
    except:
        logger.error("set_controller exception", exc_info=True)
        return { "error": "Request must be in JSON format." }, 415

@app.route("/controller/autonomous", methods = ['POST'])
def autonomous():
    status = True
    try:
        if request.is_json:
            data = request.get_json()
            if "data" in data:
                model = data["data"]

                if propulsion != None:
                    propulsion.autoMove(model)
            else:
                message = "No autonomous data"
                logger.error(message)
                return { "status": "Error", "error": message }
    except:
        logger.error("autonomous exception", exc_info=True)
        return { "error": "Request must be in JSON format." }, 415

if __name__ == '__main__':
    log_path = '/home/pi/Desktop/rov.log'

    try:
        # ensure log file is created if it doesn't already exist
        if not os.path.exists(log_path):
            open(log_path, 'w+').close()

        # open a custom logger
        logger = logging.getLogger('brain')

        # create logging handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_path, "a+")
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)

        # create formatters and add it to handlers
        console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # create propulsion to integrate with thrusters
        propulsion = Propulsion()
        propulsion.setLogger(logger)
        
        # run flask web server
        app.run(host='0.0.0.0', port=5000)
    except:
        logger.error("Main program exception", exc_info=True)
        pass