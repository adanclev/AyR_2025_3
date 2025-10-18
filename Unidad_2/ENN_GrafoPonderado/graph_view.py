import random
import math
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QGraphicsScene,QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QMainWindow
)
from PyQt5.QtGui import QPen, QBrush, QPainter, QFont
from PyQt5.QtCore import Qt, QPointF, QLineF
from local_search_thread import LSThread
from config import NODE_TYPE

qtCreatorFile = "graph_view.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class GraphView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.scene = QGraphicsScene()
        self.graph_view.setScene(self.scene)
        self.graph_view.setRenderHint(QPainter.Antialiasing)

        self.btn_new.setEnabled(False)
        self.btn_new.clicked.connect(self.new_graph)

        self.nodes = []  # [(id, type), ...]
        self.edges = []  # [(nodo1, nodo2, peso, is_selected), ...]
        self.posiciones = []
        self.nodes_to_draw = {}  # {id: (pos, type)}

        self.Worker = None
        self.new_graph()

    def new_graph(self):
        self.btn_new.setEnabled(False)

        # Detener thread anterior si existe
        if self.Worker is not None and self.Worker.isRunning():
            self.Worker.terminate()
            self.Worker.wait()

        # Crear y arrancar nuevo thread
        self.nodes_to_draw = {}
        self.Worker = LSThread()
        self.Worker.Graph.connect(self.worker_conn)
        self.Worker.finished.connect(self.thread_finished)  # señal cuando termina
        self.Worker.start()

    def thread_finished(self):
        # Rehabilitar botón cuando el thread termine
        self.btn_new.setEnabled(True)

    def worker_conn(self, nodes, edges, weight, path):
        self.nodes = nodes
        self.edges = edges
        self.btn_new.setEnabled(not self.Worker.running)

        if not self.nodes_to_draw:
            self.posiciones = self.generar_posiciones_circulo()
            self.nodes_to_draw = self.asignar_posiciones_aleatorias()

        self.lbl_best.setText(str(weight))
        self.lbl_path.setText(path)

        self.scene.clear()
        self.dibujar_grafo()

    def generar_posiciones_circulo(self):
        n = len(self.nodes)
        center_x = self.graph_view.width() / 2
        center_y = self.graph_view.height() / 2
        radio = min(self.graph_view.width(), self.graph_view.height()) / 2 - 80
        posiciones = []
        for i in range(n):
            angulo = 2 * math.pi * i / n
            x = center_x + radio * math.cos(angulo)
            y = center_y + radio * math.sin(angulo)
            posiciones.append(QPointF(x, y))
        return posiciones

    def asignar_posiciones_aleatorias(self):
        posiciones_disponibles = self.posiciones.copy()
        random.shuffle(posiciones_disponibles)
        return {id: (posiciones_disponibles[i], type)
                for i, (id, type) in enumerate(self.nodes)}

    def dibujar_grafo(self):
        if not self.nodes or not self.edges:
            return

        outline_color_green = Qt.green
        outline_color_red = Qt.red
        outline_color_black = Qt.black
        brush_nodo = QBrush(Qt.white)
        fuente_nodo = QFont("Arial", 14)
        fuente_peso = QFont("Arial", 16)

        # Dibujar aristas
        for origen, destino, peso, is_selected in self.edges:
            p1 = self.nodes_to_draw[origen][0]
            p2 = self.nodes_to_draw[destino][0]

            linea = QGraphicsLineItem(p1.x(), p1.y(), p2.x(), p2.y())
            linea.setPen(QPen(Qt.yellow if is_selected else Qt.black, 2))
            self.scene.addItem(linea)

            # Texto del peso
            line = QLineF(p1, p2)
            mid_x = (p1.x() + p2.x()) / 2
            mid_y = (p1.y() + p2.y()) / 2
            dx = line.dy()
            dy = -line.dx()
            longitud = (dx**2 + dy**2) ** 0.5
            if longitud != 0:
                dx /= longitud
                dy /= longitud
            desplazamiento = 20
            peso_pos_x = mid_x + dx * desplazamiento
            peso_pos_y = mid_y + dy * desplazamiento
            texto_peso = QGraphicsTextItem(str(peso))
            texto_peso.setFont(fuente_peso)
            texto_peso.setPos(peso_pos_x - 10, peso_pos_y - 10)
            self.scene.addItem(texto_peso)

        # Dibujar nodos
        for id, (pos, typeof) in self.nodes_to_draw.items():
            if typeof == NODE_TYPE.get("START"):
                pen_outline = QPen(outline_color_green, 3)
            elif typeof == NODE_TYPE.get("END"):
                pen_outline = QPen(outline_color_red, 3)
            else:
                pen_outline = QPen(outline_color_black, 3)

            node = QGraphicsEllipseItem(pos.x() - 25, pos.y() - 25, 50, 50)
            node.setBrush(brush_nodo)
            node.setPen(pen_outline)
            self.scene.addItem(node)

            text = QGraphicsTextItem(id)
            text.setFont(fuente_nodo)
            text.setPos(pos.x() - 10, pos.y() - 15)
            self.scene.addItem(text)

        bounding_rect = self.scene.itemsBoundingRect()
        padding = 50
        bounding_rect.adjust(-padding, -padding, padding, padding)
        self.scene.setSceneRect(bounding_rect)
        self.graph_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)