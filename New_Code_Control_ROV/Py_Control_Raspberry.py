import socket
import json

def connectSocket():
    global receptor
    receptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receptor.bind(("0.0.0.0", 5000))
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
        inputs = readInputs()
        print(inputs)
except KeyboardInterrupt:
    finishProgram()