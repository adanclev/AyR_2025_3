import sys
from PyQt5.QtWidgets import QApplication
from path_view import PathView
import random as rand

if __name__ == "__main__":
    #rand.seed(5)
    app = QApplication(sys.argv)
    window = PathView()
    window.show()
    sys.exit(app.exec_())
