import socket
import json

def connectSocket():
    global receptor
    receptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receptor.bind(("0.0.0.0", 5000))
    receptor.settimeout(1)
    print("Socket established")

def readInputs():
    data, address = receptor.recvfrom(2048)
    json_message = data.decode("utf-8")
    message = json.loads(json_message)
    return message

def finishProgram():
    receptor.close()

connectSocket()
try:
    while True:
        try:
            inputs = readInputs()
        except socket.timeout:
            print("Stopped receiving data")
            inputs = {
                "left_x": 0,
                "left_y": 0,
                "right_x": 0,
                "right_y": 0,
                "a_button": 0,
                "b_button": 0,
                "x_button": 0,
                "y_button": 0,
                "left_button": 0,
                "right_button": 0
            }
        print(inputs)
except KeyboardInterrupt:
    finishProgram()