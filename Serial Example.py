import serial
ser = serial.Serial('/dev/cu.wchusbserial1420', 9600)
while True:
    print(ser.readline())