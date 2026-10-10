import pygame
import time
import socket
import json

def connectController():
    pygame.init()
    pygame.joystick.init()
    while True:
        count = pygame.joystick.get_count()
        if count == 0:
            print("No controllers detected")
            time.sleep(1)
        else:
            print("Controller detected")
            global Xbox 
            Xbox = pygame.joystick.Joystick(0)
            Xbox.init()
            print("Controller connected")
            break

def connectSocket():
    global pi
    print("Connecting to pi")
    pi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pi.connect(("192.168.50.2", 5000))
    print("Connected to pi")

def deadzone(axis):
    if abs(axis) < 0.1:
        return 0
    else:
        return axis

def collectInputs():
    pygame.event.pump()
    lx = deadzone(round(Xbox.get_axis(0), 2))
    ly = deadzone(-1*round(Xbox.get_axis(1), 2))
    rx = deadzone(round(Xbox.get_axis(2), 2))
    ry = deadzone(-1*round(Xbox.get_axis(3), 2))
    ab = Xbox.get_button(0)
    bb = Xbox.get_button(1)
    xb = Xbox.get_button(2)
    yb = Xbox.get_button(3)
    lb = Xbox.get_button(4)
    rb = Xbox.get_button(5)
    input_dictionary = {
        "left_x": lx,
        "left_y": ly,
        "right_x": rx,
        "right_y": ry,
        "a_button": ab,
        "b_button": bb,
        "x_button": xb,
        "y_button": yb,
        "left_button": lb,
        "right_button": rb
    }
    return input_dictionary

def sendInputs(m):
    message = m
    json_message = json.dumps(message)
    data = json_message.encode("utf-8")
    pi.send(data)
    print("Sent: ", message)

def finishProgram():
    pygame.quit()
    pi.close()

connectController()
connectSocket()
try:
    while True:
        inputs = collectInputs()
        sendInputs(inputs)
        time.sleep(0.05)
except KeyboardInterrupt:
    finishProgram()