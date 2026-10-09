import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import json
import requests
import threading
import time
# import gi
# gi.require_version('Gst', '1.0')
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gst, Gtk, GLib
import pygame
from multiprocessing import Process 

#from modules.ps4.ps4 import PS4
# from controls.cam import Cam

BRAIN_IP = "192.168.1.50"

# callback function for PS4 controller
def eventChangeHandler(status):
    try:
        url = f"http://{BRAIN_IP}:5000/controller"
        controller_status = { "data": status }
        response = requests.post(url, json = controller_status)
        # result = requests.get(url)
        result = json.loads(response.text)

        if "data" in result.keys():
            control = status["control"]
            val = status["state"]
            print(f"{control}: {val}")
        elif "error" in result.keys():
            print(result["error"])
    except:
        pass

    return 

def on_controller_left_clicked(button):
    status = controllerStatus
    eventChangeHandler(status)

def ps4ButtonHandler(id, val):
    status = {
        "control": id,
        "state": val
    }
    eventChangeHandler(status)

def ps4HatHandler(lr, ud):
    status = {
        "control": "hatLRState",
        "state": lr
    }
    eventChangeHandler(status)
    time.sleep(1)
    status = {
        "control": "hatUDState",
        "state": ud
    }
    eventChangeHandler(status)

def ps4StickHandler(id, lr, ud):
    status = {
        "control": f"{id}LR",
        "state": lr
    }
    eventChangeHandler(status)
    time.sleep(1)
    status = {
        "control": f"{id}UD",
        "state": ud
    }
    eventChangeHandler(status)

# callback function which displays PS4 status during initialization
def initStatus( status ):
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format( status ) )

cam1 = None
cam2 = None
Status = None
ps4 = None
controllerStatus = {
    "leftTriggerPos": -1.0,
    "rightTriggerPos": -1.0,
    "leftStickLR": 0,
    "leftStickUD": 0,
    "rightStickLR": 0,
    "rightStickUD": 0,
    "leftBtn1State": 0,
    "rightBtn1State": 0,
    "leftBtn2State": 0,
    "rightBtn2State": 0,
    "hatLRState": 0,
    "hatUDState": 0,
    "leftStickPressedState": 0,
    "rightStickPressedState": 0,
    "optionsBtnState": 0,
    "homeBtnState": 0,
    "startBtnState": 0,
    "triangleBtnState": 0,
    "squareBtnState": 0,
    "circleBtnState": 0,
    "crossXBtnState": 1
}

# def init_cams():
#     # create cams
#     cam1 = Cam("cam1", "FRONT LEFT")
#     cam2 = Cam("cam2", "FRONT RIGHT")

#     # add cams to a container
#     main_container = Gtk.Grid()
#     main_container.add(cam1.get_container())
#     main_container.add(cam2.get_container())

#     return main_container

def init_ps4():
    keepRunning = False
    ps4 = PS4("PVIT ROV Controller", initStatus,
        btnChanged=ps4ButtonHandler,
        hatChanged=ps4HatHandler,
        stickChanged=ps4StickHandler )

    if ps4.initialised :
        keepRunning = True
    else:
        keepRunning = False

    while keepRunning == True :
        # trigger stick events and check for quit
        keepRunning = ps4.controllerStatus()

        # time.sleep(0.1)
        
    pygame.quit()

# def init_toolbar():
#     toolbar = Gtk.Box(spacing=10)
#     controller_left = Gtk.Button.new_with_label("Left")
#     controller_left.connect("clicked", on_controller_left_clicked)
#     toolbar.pack_start(controller_left, True, False, 2)
#     status = Gtk.Entry()
#     status.set_text("")
#     toolbar.pack_start(status, True, False, 2)
#     return toolbar, status

if __name__ == '__main__':
    # initialize ps4 controller
    #init_ps4()

    # # create main commander window
    # window = Gtk.ApplicationWindow()
    # window.set_title("PVIT ROV Commander")
    # # window.set_default_size(2000, 700)
    # window.connect("destroy", Gtk.main_quit)

    # # create cams and add to window
    # container = Gtk.Grid()
    # container.set_orientation(Gtk.Orientation.VERTICAL)
    # # cams = init_cams()
    # # container.add(cams)
    # toolbar, Status = init_toolbar()
    # container.add(toolbar)
    # window.add(container)

    # # render
    # window.show_all()

    # # show application ui
    # Gtk.main()