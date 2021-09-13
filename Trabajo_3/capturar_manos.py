import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands = 2,
    min_detection_confidence = 0.5) as hands:
    
    ret, image = cap.read()
    #image = cv2.imread("imagen_0001,jpg")
    height, width, _ = image.shape
    image = cv2.flip(image, 1)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    results = hands.process(image_rgb)

    # HANDEDNESS
    print("Handedness: ", results.multi_handedness)
    #HAND LANDMARKS
    #print("Hand landmarks:", results.multi_hand_landmarks)

    if results.multi_hand_landmarks is not None:
        #-----------------------------------------
        #Dibujar puntos y conexiones con mediapipe
        """for hand_landmarks in results.multi_hand_landmarks:
            print(hand_landmarks)
            mp_drawing.draw_landmarks(
                image, hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255,255,0), thickness=4, circle_radius=5),
                mp_drawing.DrawingSpec(color=(255,0,255), thickness=4))"""
        #-------------------------------------------
        # Accediendo a los puntos clave, de acuerdo a su nombre
        """for hand_landmarks in results.multi_hand_landmarks:
            x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
            y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)
            
            x2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
            y2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

            x3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)
            y3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)

            x4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * width)
            y4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * height)

            x5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width)
            y5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)
            
            cv2.circle(image, (x1, y1), 3, (255, 0, 0), 3)
            cv2.circle(image, (x2, y2), 3, (255, 0, 0), 3)
            cv2.circle(image, (x3, y3), 3, (255, 0, 0), 3)
            cv2.circle(image, (x4, y4), 3, (255, 0, 0), 3)
            cv2.circle(image, (x5, y5), 3, (255, 0, 0), 3)"""
        #-------------------------------------------
        #Accediendo a puntos clave de acuerdo a indice
        index = [4, 8, 12, 16, 20]
        for hand_landmarks in results.multi_hand_landmarks:
            for (i, points) in enumerate(hand_landmarks.landmark):
                if i in index:
                    x = int(points.x * width)
                    y = int(points.y * height)
                    cv2.circle(image, (x, y), 3, (255, 0, 0), 3)

    image = cv2.flip(image,1)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()