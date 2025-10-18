from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtSvg import QSvgRenderer
from camera_thread import CameraThread
from config import STYLES, MODELO, PESOS

qtCreatorFile = "Interfaz_Verificacion.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CNNTiempoRealView(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("CNN Tiempo Real")

        self.lbl_predict.setText("Esperando cámara ...")

        self.btn_action.clicked.connect(self.toggle_camera)

        self.is_running = False

        self.Worker = None

    # Área de los Slots
    def toggle_camera(self):
        if self.Worker is None or not self.Worker.isRunning():
            self.is_running = True
            self.Worker = CameraThread(model_path=MODELO, weights_path=PESOS)

            self.Worker.Prediction.connect(self.worker_conn)
            self.Worker.start()
            self.btn_action.setText("Detener cámara")
            self.btn_action.setStyleSheet(STYLES.get("btn_action","") + "background-color: rgb(255, 0, 0);")
        elif self.Worker is not None:
            self.Worker.stop()
            self.is_running = False
            self.btn_action.setText("Iniciar cámara")
            self.btn_action.setStyleSheet(STYLES.get("btn_action","") + "background-color: rgb(85, 85, 255);")

            self.lbl_predict.setText("Esperando cámara ...")
            self.lbl_predict.setStyleSheet(STYLES.get("lbl_predict","") + "background-color: rgb(122, 122, 122);")

            renderer = QSvgRenderer(":/svgs/Archivos/Images/placeholder.svg")
            pixmap = QtGui.QPixmap(self.lbl_cam.width(), self.lbl_cam.height())
            pixmap.fill(QtCore.Qt.transparent)

            painter = QtGui.QPainter(pixmap)
            renderer.render(painter)
            painter.end()

            self.lbl_cam.setPixmap(pixmap)

    def worker_conn(self, img, predict):
        if not self.is_running:
            return
        self.update_label_frame(img)
        self.update_label_predict(predict)

    def update_label_frame(self, img):
        h, w, ch = img.shape
        bytesPerLine = ch * w
        convertToQtFormat = QtGui.QImage(img.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(convertToQtFormat)
        self.lbl_cam.setPixmap(pixmap.scaled(self.lbl_cam.size(), QtCore.Qt.KeepAspectRatio))

    def update_label_predict(self, prediction):
        if prediction[0]:
            self.lbl_predict.setStyleSheet(STYLES.get("lbl_predict", "") + "background-color: rgb(0, 170, 0);")
        else:
            self.lbl_predict.setStyleSheet(STYLES.get("lbl_predict", "") + "background-color: rgb(255, 0, 0);")

        self.lbl_predict.setText(prediction[1])