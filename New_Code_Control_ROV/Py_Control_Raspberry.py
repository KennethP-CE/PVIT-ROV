"""Raspberry Pi control program.

Receives operator inputs over UDP from the desk program (Py_Control_Desk),
converts the dictionary to a numeric CSV line, and sends it over serial to
the Arduino Mega attached at /dev/ttyACM0. While no input arrives it sends
a row of zeros so the ROV stops.
"""

import json
import math
import serial
import socket
import time

SERIAL_PORT = "/dev/ttyACM0"
SERIAL_BAUD = 115200
SOCKET_PORT = 5000

# Canonical column order for the CSV. Keep in sync with the sender,
# Py_Control_Desk.collectInputs(), which builds the dictionary in this order.
CONTROL_KEYS = (
    "left_x",
    "left_y",
    "right_x",
    "right_y",
    "a_button",
    "b_button",
    "x_button",
    "y_button",
    "left_button",
    "right_button",
)

receptor = None
ser = None


def connectSocket(port=SOCKET_PORT):
    global receptor
    receptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receptor.bind(("0.0.0.0", port))
    receptor.settimeout(1)
    print("Socket established")


def connectSerial(port=SERIAL_PORT, baud=SERIAL_BAUD):
    global ser
    ser = serial.Serial(port, baud, timeout=1)
    time.sleep(2)
    print("Serial established")


def readInputs():
    data, _address = receptor.recvfrom(2048)
    return json.loads(data.decode("utf-8"))


def _to_number(value):
    """Coerce any JSON value to a plain int/float.

    Non-numeric data becomes 0, so the CSV line carries numeric fields only
    (no strings).
    """
    if isinstance(value, bool):
        return int(value)
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return 0
    return 0


def dictToCSV(message, keys=CONTROL_KEYS):
    """Return the control dictionary as a CSV line of numeric values only.

    Columns always appear in CONTROL_KEYS order; missing keys are emitted as
    0 so the Arduino always receives a full row.
    """
    if not isinstance(message, dict):
        message = {}
    fields = []
    for key in keys:
        number = _to_number(message.get(key, 0))
        if not math.isfinite(number):
            number = 0
        fields.append(f"{number:g}")
    return ",".join(fields)


def sendCSV(csv_line):
    if ser is None:
        return
    try:
        ser.write((csv_line + "\n").encode("utf-8"))
        print("Sent CSV:", csv_line)
    except serial.SerialException as exc:
        print("Serial write failed:", exc)


def readConfirmation():
    """Print any confirmation message the Arduino sends back."""
    if ser is None:
        return
    try:
        line = ser.readline().decode("utf-8", errors="replace").strip()
    except (serial.SerialException, UnicodeDecodeError):
        return
    if line:
        print("Arduino:", line)


def finishProgram():
    if receptor is not None:
        receptor.close()
    if ser is not None:
        ser.close()


def main():
    connectSocket()
    connectSerial()
    try:
        while True:
            try:
                inputs = readInputs()
            except socket.timeout:
                print("Stopped receiving data")
                inputs = {key: 0 for key in CONTROL_KEYS}
            except json.JSONDecodeError as exc:
                print("Invalid JSON from socket:", exc)
                continue
            except UnicodeDecodeError as exc:
                print("Undecodable UDP packet:", exc)
                continue
            print(inputs)
            sendCSV(dictToCSV(inputs))
            readConfirmation()
    except KeyboardInterrupt:
        finishProgram()


if __name__ == "__main__":
    main()
