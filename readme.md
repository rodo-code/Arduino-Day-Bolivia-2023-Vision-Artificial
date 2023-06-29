# Arduino Day Bolivia 2023 - Taller Introducción a la Visión Artificial

## Software Requerido
- Python 3.x
- Arduino IDE
- IDE para Python de preferencia (PyCharm, VS Code, etc)

## Instalar las librerias

Para instalar las librerias se recomienda utilizar un entorno virtual de Python, el mismo se puede crear mediante el comando, ejecutado en la raiz del proyecto

```bash
python -m venv .venv
```

Luego se debe activar el entorno se puede utilizar los scritps ubicados en la carpeta `.venv/Scripts` para Windows usar el archivo `.bat`

Para asegurarse que el entorno virtual este activido debe ver un `(.venv)` antes de la ruta en la que esta.

Finalmente para instalar las librerias necesarias debe ejecutar, en la raiz del proyecto.

```bash
pip install -r requirements.txt
```

## Explicación del Código

1. Importamos las librerias
   ```python
   import cv2
   import numpy as np
   import serial
   import time
   ```

2. Creamos la funcion para comunicarnos con nuestro Arduino
   ```python
   def mandar_arduino_obtener_respuesta(msg):
      ser.write(bytes(msg, 'utf-8'))
      time.sleep(0.01)
      data = ser.readline()
      print(data)
   ```
3. Configuracion para la comunicación Serial con Arduino
      ```python
      COM = 'com5'
      BAUD = 115200
      ser = serial.Serial(port=COM, baudrate=BAUD,timeout=.1)
      ```
4. Configuramos la fuente de video con el método `VideoCapture()` cuyo parámetro usualmente es 0, 1 o 2 dependiendo de la cantidad de dispositivos de captura de video que tenga tu computadora.
   ```python
   cap = cv2.VideoCapture(0)
   ```
5. Configuramos la detección de color para el objeto que vamos a trackear, debemos seleccionar el color en formato HSV (Tinte, Saturacion, Brillo), para lo cual puede revisar esta [fuente](https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv?lq=1)
   ```python
   colorBajo = np.array([90, 100, 20], np.uint8)
   colorAlto = np.array([120, 255, 255], np.uint8)
   ```
6. Dentro de un ciclo constante (while True) colocamos la captura de video mediante, donde `ret` es un valor booleano que es `True` si es que la imagen se capturó correctamente o `False` en caso contrario y `frame` contiene la imagen capturada.
   ```python
    ret, frame = cap.read()
   ```
7. Si la imagen es correcta procedemos a reconocer el contorno haciendo
    ```python
    frame = cv2.flip(frame, 1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(frameHSV, colorBajo, colorAlto)
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contornos, -1, (255, 0, 0), 4)
    ```
    - Donde `frame = cv2.flip(frame, 1)` hara que la imagen se refleje para que tengamos una vista directa del movimiento.
    - Con `frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)` convertiremos el color del frame de *BGR* a *HSV* esto debido a que para la detección requerimos el frame en *HSV*.
    - Con `mascara = cv2.inRange(frameHSV, colorBajo, colorAlto)` crearemos una máscara que solo detectará el color que elegimos dentro del rango de `colorBajo` y `colorAlto`.
    - Posteriromente encontramos los contornos con `contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)` donde el primer parámetro es la máscara, la segunda es el modo de obtener el color y la tercera método de aproximación del contorno.
    - Finalmente se dibuja el contorno con `cv2.drawContours(frame, contornos, -1, (255, 0, 0), 4)` donde el primer parámetro es la imagen donde se dibujará, la segunda los contornos, la tercera es para indicar que contornos dibujar si es $-1$ se dibujan todos los contornos, el cuarto parámetro es el color en BGR y el último es el grosor del contorno dibujado.
8. Para todos los contornos calculamos su área mediante
   ```python
   area = cv2.contourArea(c)
   ```
   Si el área es mayor a 600 pixeles entonces sabremos que es el objeto que estamos trackeando, esto para evitar algunos objetos pequeños o pequeños colores en el frame.
9.  Si el area es mayor a 600 calculamos para ese contorno sus momentos y centroides haciendo
   ```python
   M = cv2.moments(c)
   if M["m00"] == 0:
	   M["m00"] = 1
   x = int(M["m10"] / M["m00"])
   y = int(M['m01'] / M['m00'])
   ```
10. Dibujamos la informacion del centroide mediante
   ```python
   cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
   font = cv2.FONT_HERSHEY_SIMPLEX
   cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
   nuevoContorno = cv2.convexHull(c)
   cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)
   ``` 
11. Pondremos rangos basados en el eje x de la posición de nuestro objeto
   ```python
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
   ```
12. Mostramos el frame utilizando
    ```python
    cv2.imshow('frame', frame)

    ```
13. Creamos un método de salida para la ejecución en este caso si apretamos la tecla s el programa terminará
      ```python
      if cv2.waitKey(1) & 0xFF == ord('s'):
         ser.close()
         break
      ```
14. Finalmente se libera la cámara y se cierra la ventana haciendo
      ```python
      cap.release()
      cv2.destroyAllWindows()
      ```
15. En Arduino utilziremos el siguiente código para ver como a través de la comunicación serial nuestro código de python se comunica con la placa Arduino.
   ```c
   int x;
   void setup() {
      Serial.begin(115200);
      Serial.setTimeout(1);
   }
   void loop() {
      if(Serial.available()){
         x = Serial.readString().toInt();
         if(x==1){
            Serial.print("Mover a la izquierda 100%");
         }
         else if(x==2){
            Serial.print("Mover a la izquierda 60%");
         }
         else if(x==3){
            Serial.print("Mover a la izquierda 30%");
         }
         else if(x==4){
            Serial.print("Centro");
         }
         else if(x==5){
            Serial.print("Mover a la derecha 30%");
         }
         else if(x==6){
            Serial.print("Mover a la derecha 60%");
         }
         else if(x==7){
            Serial.print("Mover a la derecha 100%");
         }
      }
   }
   ```
16. Mandamos nuestro programa en Arduino a la placa
17. Corremos el script de python utilizando `python main.py`
18. Analizamos el feedback desde Arduino