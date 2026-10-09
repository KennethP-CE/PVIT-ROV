import pygame
import time
from pyfirmata2 import ArduinoMega

max = 20
min = 21
vlmax = 22
vrmax = 23
vlmin = 18
vrmin = 18.5
frmin = 18

board = ArduinoMega('COM3')
print("0")
T1 = board.get_pin('d:2:s')
print("1")
T2 = board.get_pin('d:4:s')
print("2")
T3 = board.get_pin('d:6:s')
print("3")
T4 = board.get_pin('d:8:s')
print("4")
T5 = board.get_pin('d:10:s')
print("5")
T6 = board.get_pin('d:12:s')
print("6")

print("ESC Set Up")
T1.write(91)
T2.write(91)
T3.write(91)
T4.write(91)
T5.write(91)
T6.write(91)
time.sleep(5)


pygame.init()
pygame.joystick.init()


joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Using controller: {joystick.get_name()}\n")


try:
    while True:
        pygame.event.pump()


        left_h = round(joystick.get_axis(0), 2)
        left_v = -1 * round(joystick.get_axis(1), 2)
        right_v = -1 * round(joystick.get_axis(3), 2)
        D = round(joystick.get_axis(4), 2)


        right_h = round(joystick.get_axis(2), 2) if joystick.get_numaxes() > 2 else 0
        right_trigger = round(joystick.get_axis(5), 2) if joystick.get_numaxes() > 5 else 0

        left_trigger = round(joystick.get_axis(5), 2) if joystick.get_numaxes() > 5 else 0

        Left_button = joystick.get_button(4)
        Right_button = joystick.get_button(5)
        a_button = joystick.get_button(0)
        b_button = joystick.get_button(1)
        x_button = joystick.get_button(2)
        y_button = joystick.get_button(3)


        print(
            f"LH: {left_h:>5} | LV: {left_v:>5} | RH: {right_h:>5} | RV: {right_v:>5} | "
            f"LB: {Left_button} | RB: {Right_button} | " 
            f"A:{a_button} B:{b_button} X:{x_button} Y:{y_button}"
            f"LT: {left_trigger} "
        )
        if left_v > 0.25:
            Power = (max*left_v)
            write = 91 + Power
            T1.write(write)
            T2.write(write)
            T3.write(write)
            T4.write(write)
            T5.write(91)
            T6.write(91)
        elif left_v < -0.25:
            Power = (min*left_v)
            write = 91 + Power
            WriteFR = 91 + -1*(frmin*left_v)
            T1.write(write)
            T2.write(WriteFR)
            T3.write(write)
            T4.write(write)
            T5.write(91)
            T6.write(91)
        elif left_h > 0.25:
            Power = (max*left_h)
            oPower = -1*(min*left_h)
            WriteF = 91 + Power
            WriteB = 91 + oPower
            WriteFR = 91 + -1*(frmin*left_h)
            T1.write(WriteF)
            T2.write(WriteFR)
            T3.write(WriteB)
            T4.write(WriteF)
            T5.write(91)
            T6.write(91)
        elif left_h < -0.25:
            Power = (min*left_h)
            oPower = -1*(max*left_h)
            WriteF = 91 + Power
            WriteB = 91 + oPower
            T1.write(WriteF)
            T2.write(WriteB)
            T3.write(WriteB)
            T4.write(WriteF)
            T5.write(91)
            T6.write(91)
        elif right_h > 0.25:
            Power = (max*right_h)
            oPower = -1*(min*right_h)
            WriteF = 91 + Power
            WriteB = 91 + oPower
            WriteFR = 91 + -1*(frmin*right_h)
            T1.write(WriteF)
            T2.write(WriteFR)
            T3.write(WriteF)
            T4.write(WriteB)
            T5.write(91)
            T6.write(91)
        elif right_h < -0.25:
            Power = (min*right_h)
            oPower = -1*(max*right_h)
            WriteF = 91 + Power
            WriteB = 91 + oPower
            T1.write(WriteF)
            T2.write(WriteB)
            T3.write(WriteF)
            T4.write(WriteB)
            T5.write(91)
            T6.write(91)
        elif y_button == 1:
            T5.write(91 + vlmax)
            T6.write(91 + vrmax)
            T1.write(91)
            T2.write(91)
            T3.write(91)
            T4.write(91)
        elif a_button == 1:
            T5.write(91 - vlmin)
            T6.write(91 - vrmin)
            T1.write(91)
            T2.write(91)
            T3.write(91)
            T4.write(91)
        else:
            T5.write(91)
            T6.write(91)
            T1.write(91)
            T2.write(91)
            T3.write(91)
            T4.write(91)

        time.sleep(0.1)


except KeyboardInterrupt:
    print("\nExiting...")
finally:
    pygame.quit()