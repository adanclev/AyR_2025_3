import sys
from PyQt5.QtWidgets import QApplication
from graph_view import GraphView
import random as rand

if __name__ == "__main__":
    rand.seed(9)
    app = QApplication(sys.argv)
    window = GraphView()
    window.show()
    sys.exit(app.exec_())

    # 040912