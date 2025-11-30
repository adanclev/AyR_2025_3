import sys
from PyQt5.QtWidgets import QApplication
from control_bocina import ControlBocinaView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ControlBocinaView()
    window.show()
    sys.exit(app.exec_())