import sys
from mediapipe5 import MediaPipe5
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MediaPipe5()
    window.show()
    sys.exit(app.exec_())