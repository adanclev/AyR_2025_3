from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import mediapipe as mp
import numpy as np
import math
from config import *

class CameraThread(QThread):
    Statement = pyqtSignal(np.ndarray, list)

    def __init__(self):
        super().__init__()
        self.running = True

        try:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
                max_num_hands=1
            )
            self.mp_draw = mp.solutions.drawing_utils
        except Exception as e:
            print(f'Error al cargar el modelo: {e}')
            self.mp_hands = None
            self.mp_draw = None

    def run(self):
        cam = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cam.read()
            if not ret: return

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            states = list()

            # self.draw_lines(rgb_frame, height, width)

            if self.hands:
                results = self.hands.process(rgb_frame)
                if results.multi_hand_landmarks:
                    self.draw_landmarks(rgb_frame, results, height, width, states)

            self.Statement.emit(rgb_frame, states)

        cam.release()

    def stop(self):
        self.running = False
        self.wait()

    def draw_lines(self, frame, height, width):
        x_lim_izq = int(width * MARGEN_IZQUIERDO)
        cv2.line(frame, (x_lim_izq, 0), (x_lim_izq, height), (255, 255, 0), 2)

        x_lim_der = int(width * MARGEN_DERECHO)
        cv2.line(frame, (x_lim_der, 0), (x_lim_der, height), (255, 255, 0), 2)

    def draw_landmarks(self, frame, results, height, width,states):
        for hand_landmarks in results.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            # self.move_detector(frame, hand_landmarks, height, width, states)
            self.analizar_gesto(hand_landmarks, states)

    def move_detector(self, frame, hand_landmarks, height, width, states):
        x4 = int(hand_landmarks.landmark[4].x * width)
        y4 = int(hand_landmarks.landmark[4].y * height)

        x8 = int(hand_landmarks.landmark[8].x * width)
        y8 = int(hand_landmarks.landmark[8].y * height)
        distancia = math.hypot(x8 - x4, y8 - y4)

        # Punto medio del pellizco
        cx, cy = (x4 + x8) // 2, (y4 + y8) // 2

        pos_relativa = cx / width

        if distancia < UMBRAL_PELLIZCO:
            states.append(STATES.get("FORWARD"))

            if pos_relativa < MARGEN_IZQUIERDO:
                states.append(STATES.get("LEFT"))
            elif pos_relativa > MARGEN_DERECHO:
                states.append(STATES.get("RIGHT"))

    def analizar_gesto(self, landmarks, states):
        dedos = []

        # --- 0. PULGAR ---
        if landmarks.landmark[4].x < landmarks.landmark[3].x:
            dedos.append(1)
        else:
            dedos.append(0)

        # --- 1. ÍNDICE ---
        # Si la punta (8) está más ARRIBA que la articulación (6) en el eje Y
        if landmarks.landmark[8].y < landmarks.landmark[6].y:
            dedos.append(1)
        else:
            dedos.append(0)

        # --- 2. MEDIO ---
        if landmarks.landmark[12].y < landmarks.landmark[10].y:
            dedos.append(1)
        else:
            dedos.append(0)

        # --- 3. ANULAR ---
        if landmarks.landmark[16].y < landmarks.landmark[14].y:
            dedos.append(1)
        else:
            dedos.append(0)

        # --- 4. MEÑIQUE ---
        if landmarks.landmark[20].y < landmarks.landmark[18].y:
            dedos.append(1)
        else:
            dedos.append(0)

        # Caso: Todos levantados
        if dedos == [1, 1, 1, 1, 1] or dedos == [0, 1, 1, 1, 1]:
            states.append(STATES.get("STOP"))
            return

        # Caso: Pulgar
        if dedos[0] == 1:
            states.append(STATES.get("FORWARD"))

        # Caso: Mano Cerrada
        if dedos == [0, 0, 0, 0, 0] or dedos == [0, 1, 0, 0, 0] or dedos == [0, 0, 0, 0, 1]:
            states.append(STATES.get("BACKWARD"))

        # Caso: Índice
        if dedos[1] == 1:
            states.append(STATES.get("LEFT"))

        # Caso: Meñique
        if dedos[4] == 1:
            states.append(STATES.get("RIGHT"))

        return
