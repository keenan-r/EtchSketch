import pickle
import serial
import time

ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
time.sleep(1)

def wait_for_finish(sent):
    moved = False
    while moved is False:
        cmd = ser.readline()
        print(cmd)
        if cmd == b'Done\r\n':
            return

def map(val, in_min, in_max, out_min, out_max):
    return out_min + (val - in_min) * (out_max - out_min) / (in_max - in_min)

with open("points.txt", "rb") as fp:
    points = pickle.load(fp)


time.sleep(1)
for point in points:
    x = map(point[0], 0, 1080, 0, 15000)
    y = map(point[1], 0, 720, 0, 11000)
    command = "move " + str(int(x)) + " " + str(int(y)) + "\r"
    command = str.encode(command)
    print(command)
    ser.write(command)
    wait_for_finish(command)


ser.close()