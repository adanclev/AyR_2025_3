import sys
from PyQt5.QtWidgets import QApplication
from graph_view import GraphView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphView()
    window.show()
    sys.exit(app.exec_())