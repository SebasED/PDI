# ----------Conceptos básicos de PDI--------------------------------------------------------------------------
# ----------Por: John Sebastian Estrada Durango. johns.estrada@udea.edu.co  ----------------------------------
# -----------Daniel Steve Blandón Sánchez.  Steve.blandon@udea.edu.co-----------------------------------------
# -----------Curso de Procesamiento Digital de Imágenes ------------------------------------------------------
# ---------- 17 de Agosto de 2021 ----------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# 1. IMPORTANDO LAS LIBRERÍAS NECESARIAS
# ------------------------------------------------------------------------------------------------------------
import cv2
import mediapipe as mp
import numpy as np
from model import SingLenguageDigitsModel

# ------------------------------------------------------------------------------------------------------------
# 2. INICIALIZAR VARIABLES
# ------------------------------------------------------------------------------------------------------------

# Iniciar variables para usar la libreria mediapipe
mp_drawing = mp.solutions.drawing_utils # Instanciar método para dibujar puntos y lineas de las manos
mp_hands = mp.solutions.hands # Instanciar método para llamar la deteción de las manos

model_c = SingLenguageDigitsModel("model.json", "model.h5") # Instanciar el modelo

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Captura la imagen de nuestra camara, streaming
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Definir el ancho del frame
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # Definir el alto del frame

with mp_hands.Hands(max_num_hands = 1) as hands: # Se configura para que capture una sola mano

    while True:
        ret, frame = cap.read() # Leemos la imagen de entrada
        if ret == False: # Si no hay imagen sale del ciclo
            break

        height, width, _ = frame.shape # Obtenemos el alto y ancho de la imagen
        frame = cv2.flip(frame, 1) # Usamos la función flip para poner la imagen en espejo
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Pasamos de BGR a RGB
        copia = frame.copy() # Se hace una copia del frame
        results = hands.process(color) # Usamos process para obtener la información de las manos
        posiciones = [] # Lista para almacenar las coordenadas de los puntos des las manos

        if results.multi_hand_landmarks is not None: # Se verifica que se este capturando una mano
            for hand_landmarks in results.multi_hand_landmarks: # Iteramos entre la listas de manos que da el descriptor
                for id, lm in enumerate(hand_landmarks.landmark): # Obtener información de cada mano 
                    corx, cory = int(lm.x * width), int(lm.y * height) # Obtenemos la ubicación en pixeles de los puntos de la mano 
                    posiciones.append([id, corx, cory]) # Agregamos las coordenadas al arreglo
                """ mp_drawing.draw_landmarks( # Función para dibujar los puntos y lineas de la mano
                        frame, hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )"""
                if len(posiciones) != 0: # Verificar que tengamos coordenadas
                    pto_central = posiciones[9] # Determinamos el punto central de la mano
                    start_point = (pto_central[1] - 200, pto_central[2] - 220) # Punto inicial para el rectangulo
                    end_point = (pto_central[1] + 200, pto_central[2] + 220)  # Punto final para el rectangulo
                    cv2.rectangle(frame, start_point,end_point, (0, 255, 0), 3) # Rectangulo que contiene la mano
                    
                    signal = copia[pto_central[2] - 190 : pto_central[2] + 160, pto_central[1] - 150 : pto_central[1] + 150] # Creamos un frame con el recuadro que contiene la mano
                    
                    try:
                        signal_gray = cv2.cvtColor(signal, cv2.COLOR_BGR2GRAY) # Pasamos la imagen a escala de grises
                        signal_gray = cv2.resize(signal_gray, (64, 64), interpolation=cv2.INTER_CUBIC) # Damos dimensiones especificas a la imagen
                        x = np.asarray(signal_gray) # Convertimos nuestra imagen en un matriz
                        cv2.imshow("gray", x) # Mostramos la imagen de la mano en escala de grises
                        x=x.reshape(-1, 64, 64, 1) # Ajustamos las dimenciones de la matriz 
                        y=model_c.predict_digit(x) # Hacemos la predicción 
                        cv2.putText(frame, y, start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2) # Mostramos la predicción
                    except:
                        break

        cv2.imshow("Frame", frame) # Función para mostrar el frame          
        
        if cv2.waitKey(1) & 0xFF == 27: # Salir del ciclo
            break

cap.release()
cv2.destroyAllWindows()# Finaliza y termina todas las ventanas