import serial
import time

ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
time.sleep(1)
def wait_for_finish(sent):
    start_time = time.monotonic()
    moved = False
    while moved is False:
        cmd = ser.readline()
        print(cmd)
        if cmd == b'Done\r\n':
            return

time.sleep(1)

while True:
    print(1)
    ser.write(b'move -12000 -1000\r')
    wait_for_finish(b'\r')


ser.close()
