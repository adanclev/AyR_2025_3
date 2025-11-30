import cv2
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class CameraThread(QThread):
    Prediction = pyqtSignal(np.ndarray, tuple)

    def __init__(self, width=300, height=300):
        super().__init__()
        self.running = True
        self.width = width
        self.height = height
        self.eigen_model = cv2.face.EigenFaceRecognizer_create()
        # self.fisher_model = cv2.face.FisherFaceRecognizer_create()
        # self.lbph_model = cv2.face.LBPHFaceRecognizer_create()

        try:
            path = '../E05_FaceTrainer/modelo/modeloEigenFace.xml'
            self.eigen_model.read(path)
            print(f"Modelo cargado correctamente desde: {path}")
            # self.fisher_model
        except Exception as e:
            print(f"Error al cargar el modelo/pesos: {e}")

        self.face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def run(self):
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            print("Error: No se puede acceder a la cámara (Índice 0)")
            self.running = False
            return

        PREDICT_INTERVAL = 0.7  # s
        last_prediction_time = time.time()

        predict = (False, "✖️ Esperando primera predicción...")

        while self.running:
            ret, frame = cam.read()

            if not ret: break

            frame = cv2.flip(frame, 1)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if time.time() - last_prediction_time >= PREDICT_INTERVAL:
                last_prediction_time = time.time()
                predict = self.predict_eigen(frame)
            self.Prediction.emit(rgbImage, predict)

    def stop(self):
        self.running = False
        self.wait()

    def predict_eigen(self, image):
        # 1. Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # --- CORRECCIÓN 1: NO dividir por 255.0 ---
        # gray = gray / 255.0  <-- ESTO ESTABA MAL para predict()

        # --- CORRECCIÓN 2: DETECTAR EL ROSTRO PRIMERO ---
        faces = self.face_classifier.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(faces) == 0:
            return (False, "🔍 Buscando rostro...")

        # Tomamos el primer rostro encontrado (x, y, ancho, alto)
        (x, y, w, h) = faces[0]

        # Recortamos solo la cara (Region of Interest)
        rostro_recortado = gray[y:y + h, x:x + w]

        # Redimensionamos AL TAMAÑO DEL ENTRENAMIENTO (300x300)
        rostro_resized = cv2.resize(rostro_recortado, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

        # Predecimos
        try:
            label_e, conf_e = self.eigen_model.predict(rostro_resized)

            # Opcional: Puedes filtrar por confianza si es muy alta (malo)
            # if conf_e > 8000: return (False, "Desconocido")

            resultado = f"✅ {conf_e:.0f} - "  # Muestra la confianza para depurar

            match label_e:
                case 0:
                    return (True, resultado + "Adán")
                case 1:
                    return (True, resultado + "Poncho")
                case 2:
                    return (True, resultado + "Pavel")
                case 3:
                    return (True, resultado + "Cristobal")
                case _:
                    return (False, "👤 Rostro detectado pero no reconocido")
        except Exception as e:
            return (False, f"Error pred: {e}")