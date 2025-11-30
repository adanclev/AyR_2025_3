import sys
from PyQt5.QtWidgets import QApplication
from opencv_tiempo_real import OpenCVTiempoReal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenCVTiempoReal()
    window.show()
    sys.exit(app.exec_())