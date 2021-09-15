import cv2
import mediapipe as mp
import numpy as np
from model import SingLenguageDigitsModel

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
model_c = SingLenguageDigitsModel("model.json", "model.h5")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

with mp_hands.Hands(max_num_hands = 1) as hands:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        copia = frame.copy()
        results = hands.process(color) 
        posiciones = []

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    corx, cory = int(lm.x * width), int(lm.y * height)
                    posiciones.append([id, corx, cory])
                    #mp_drawing.draw_landmarks(
#                        frame, hand_landmarks,
#                        mp_hands.HAND_CONNECTIONS
#                    )
                if len(posiciones) != 0:
                    pto_central = posiciones[9]
                    start_point = (pto_central[1] - 200, pto_central[2] - 220)
                    end_point = (pto_central[1] + 200, pto_central[2] + 220)
                    cv2.rectangle(frame, start_point,end_point, (0, 255, 0), 3)
                    
                    signal = copia[pto_central[2] - 190 : pto_central[2] + 160, pto_central[1] - 150 : pto_central[1] + 150]
                    
                    try:
                        signal_gray = cv2.cvtColor(signal, cv2.COLOR_BGR2GRAY)
                        signal_gray = cv2.resize(signal_gray, (64, 64), interpolation=cv2.INTER_CUBIC)
                        x = np.asarray(signal_gray)
                        cv2.imshow("gray", x)
                        x=x.reshape(-1, 64, 64, 1)
                        y=model_c.predict_digit(x)
                        cv2.putText(frame, y, start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    except:
                        break

        cv2.imshow("Frame", frame)          
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()