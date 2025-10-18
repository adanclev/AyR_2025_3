import sys
from PyQt5.QtWidgets import QApplication
from cnn_tiempo_real import CNNTiempoRealView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CNNTiempoRealView()
    window.show()
    sys.exit(app.exec_())