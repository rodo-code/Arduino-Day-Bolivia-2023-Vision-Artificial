# Importando la libreria
import cv2
import numpy as np
import serial
import time

def mandar_arduino_obtener_respuesta(msg):
    ser.write(bytes(msg, 'utf-8'))
    time.sleep(0.01)
    data = ser.readline()
    print(data)

# Configuracion para la comunicación Serial con Arduino
COM = 'com5'
BAUD = 115200
ser = serial.Serial(port=COM, baudrate=BAUD,timeout=.1)

# Configuramos la fuente de video
cap = cv2.VideoCapture(0)

# Configuramos la detección de color
colorBajo = np.array([90, 100, 20], np.uint8)
colorAlto = np.array([110, 255, 255], np.uint8)

while True:
    ret, frame = cap.read() # ret es un booleaeno que indica si se
    if ret:
        frame = cv2.flip(frame, 1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(frameHSV, colorBajo, colorAlto)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contornos, -1, (255, 0, 0), 4)

        for c in contornos:
            area = cv2.contourArea(c)
            if area > 6000:
                M = cv2.moments(c)
                if M["m00"] == 0:
                    M["m00"] = 1
                x = int(M["m10"] / M["m00"])
                y = int(M['m01'] / M['m00'])
                cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)

                if x < 80:
                    mandar_arduino_obtener_respuesta("1")
                elif 80 <= x < 160:
                    mandar_arduino_obtener_respuesta("2")
                elif 160 <= x < 240:
                    mandar_arduino_obtener_respuesta("3")
                elif 240 <= x < 360:
                    mandar_arduino_obtener_respuesta("4")
                elif 360 <= x < 440:
                    mandar_arduino_obtener_respuesta("5")
                elif 440 <= x < 520:
                    mandar_arduino_obtener_respuesta("6")
                elif x >= 520:
                    mandar_arduino_obtener_respuesta("7")
        # cv2.imshow('mascaraAzul', mascara)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            ser.close()
            break
cap.release()
cv2.destroyAllWindows()