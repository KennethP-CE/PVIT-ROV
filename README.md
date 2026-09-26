# PVIT-ROV
Programs for the PVIT ROV team.

## Architecture Pipeline
1. Xbox Controller -> Desk Computer
2. Desk Computer <-> Raspberry Pi
3. Raspberry Pi <-> Cameras
4. Raspberry Pi <-> Arduino
5. Arduino -> L298N
6. L298N -> Linear Actuator
7. Arduino -> ESCs
8. ESCs -> Motors

## My Core Contributions
1. Wrote a python program that runs on the desk computer to send controller inputs to the Raspberry Pi.
2. Wrote a python program that runs on the Raspberry Pi that collects controller inputs sent from the desk computer, sends those controller inputs to the Arduino, and streams the attached cameras.
3. Wrote a C++ program that runs on the Arduino to convert controller inputs into pwm and digital signals.
