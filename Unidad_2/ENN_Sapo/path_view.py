from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRect
from sapo_thread import SapoThread
from config import STATES

qtCreatorFile = "path_view.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class PathView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Window")

        self.levels = list()
        self.connections = list()

        self.Worker = SapoThread()
        self.Worker.Signal.connect(self.worker_conn)
        self.Worker.start()

    def worker_conn(self, nodes, tupla):
        self.levels = nodes
        self.define_connections()

        self.lbl_best.setText(str(tupla[0]))
        self.lbl_current.setText(str(tupla[1]))

        self.update()

    def define_connections(self):
        if not self.levels:
            return

        self.connections.clear()
        for i in range(len(self.levels)):
            current_level = self.levels[i]
            next_level_index = i + 1
            if next_level_index > len(self.levels) - 1:
                break

            if len(self.levels[i]) == 1:
                for j in range(len(self.levels[next_level_index])):
                    self.connections.append((i, 0, next_level_index, j))
            else:
                for j in range(len(current_level)):
                    self.connections.append((i, j, next_level_index, 0))

    def paintEvent(self, event):
        if not self.levels:  # No hay nada que dibujar
            return

        painter = QPainter(self)
        painter.translate(10, 25)
        painter.setFont(QFont('Arial', 12))

        # Calcular posiciones de nodos
        self.posiciones = []
        ancho = self.width()
        alto_total = self.height()
        niveles_totales = len(self.levels)
        for nivel_index, nivel in enumerate(self.levels):
            x = 50 + nivel_index * (ancho // (niveles_totales+1))
            n_nodos = len(nivel)
            fila = []
            for i, cost_and_state in enumerate(nivel):
                y = (i+1) * (alto_total // (n_nodos+1))
                fila.append((x, y, cost_and_state[0], cost_and_state[1]))
            self.posiciones.append(fila)

        # Dibujar conexiones
        painter.setPen(QColor(0, 0, 0))
        for con in self.connections:
            n1, i1, n2, i2 = con
            x1, y1, *_ = self.posiciones[n1][i1]
            x2, y2, *_ = self.posiciones[n2][i2]
            painter.drawLine(x1, y1, x2, y2)

        # Dibujar nodos
        for nivel in self.posiciones:
            for x, y, cost, state in nivel:
                if state == STATES.get("SELECTED"):
                    painter.setBrush(QColor(56, 176, 0))
                elif state == STATES.get("BLOCKED"):
                    painter.setBrush(QColor(186, 24, 27))
                else:
                    painter.setBrush(QColor(113, 17, 171))
                painter.drawEllipse(x-20, y-20, 40, 40)

                if cost == 0:
                    continue

                painter.setPen(QColor(255, 255, 255))
                rect = QRect(x - 20, y - 20, 40, 40)
                painter.drawText(rect, Qt.AlignCenter, str(cost))