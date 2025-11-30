import sys
import os
from vosk import Model
from PyQt5 import uic, QtWidgets, QtMultimedia
from PyQt5.QtCore import QUrl
from config import DICCIONARIO, REGLAS, PORCIENTOS, VOSK_MODEL_PATH
from analizador_comandos import AnalizadorDeComandos
from voice_thread import VoiceThread

if not os.path.exists(VOSK_MODEL_PATH):
    print("Descargar modelo de https://alphacephei.com/vosk/models")
    sys.exit(1)

VOSK_MODEL = Model(VOSK_MODEL_PATH)

qtCreatorFile = "Control_bocina.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ControlBocinaView(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.analizador = AnalizadorDeComandos(DICCIONARIO, REGLAS)

        # Inicializar reproductor y playlist
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setPlaylist(self.playlist)

        self.carpeta_canciones = "sounds"
        self.lista_canciones = []
        self.cargar_canciones()

        # Conectar botones
        self.btn_Encender.clicked.connect(self.encender)
        self.btn_Reproducir.clicked.connect(self.reproducir)
        self.btn_Pausar.clicked.connect(self.pausar)
        self.btn_Siguiente.clicked.connect(self.siguiente)
        self.btn_Anterior.clicked.connect(self.anterior)
        self.btn_Silencio.clicked.connect(self.silencio)
        self.btn_Aumenta.clicked.connect(self.aumenta_volumen)
        self.btn_Disminuye.clicked.connect(self.disminuye_volumen)

        self.slider_Volumen.setValue(50)
        self.player.setVolume(50)
        self.slider_Volumen.valueChanged.connect(self.player.setVolume)
        self.encendida = False

        # Inicializar y Conectar Hilo de Voz
        self.voice_thread = VoiceThread(model=VOSK_MODEL)
        # Conectamos la señal de voz a la función de procesamiento
        self.voice_thread.command_recognized.connect(self.process_voice_command)
        self.voice_thread.start()

    # Sobreescribir el metodo de cierre para detener el hilo
    def closeEvent(self, event):
        print("\nCerrando aplicación y deteniendo hilo de voz...")
        self.voice_thread.stop()
        super().closeEvent(event)

    def process_voice_command(self, command):
        self.analizador.analizar(command)

        # Obtenemos los roles funcionales clave del resultado del análisis
        accion = self.analizador.lex.get(self.analizador.accion_key)
        # objeto = self.analizador.lex.get(self.analizador.objeto_key)
        valor = self.analizador.lex.get(self.analizador.valor_key)

        # Si el análisis semántico falló, detenemos la ejecución
        valido, mensaje = self.analizador._validacion(command)
        if not valido: return

        if self.analizador.accion_key == "accion_estado":
            if accion in ["encender", "prende"]:
                self.encender()
            else:
                if self.encendida: self.encender()

        elif not self.encendida:
            print("Bocina apagada")
            return

        elif self.analizador.accion_key == "accion_play":
                if accion in ["reproducir", "reproduce"]:
                    self.reproducir()
                elif accion in ["pausar", "pausa"]:
                    self.pausar()
                elif accion == "siguiente":
                    self.siguiente()
                elif accion == "anterior":
                    self.anterior()

        elif self.analizador.accion_key == "accion_ajuste":
            value = PORCIENTOS.get(valor, None)
            if accion in ["sube", "aumenta"]:
                if valor == "máximo":
                    self.player.setVolume(100)
                    self.slider_Volumen.setValue(100)
                else:
                    self.aumenta_volumen(value)

            elif accion in ["baja", "disminuye"]:
                if valor == "cero":
                    self.player.setVolume(0)
                    self.slider_Volumen.setValue(0)
                else:
                    self.disminuye_volumen(value)

            elif accion in ["establece", "establecer"]:
                if not valor: return
                if valor == 'máximo':
                    value = 100
                # print(value)
                self.establece_volumen(value)


        elif self.analizador.accion_key == "accion_mute":
            self.silencio()

        else:
            self.statusbar.showMessage("Comando reconocido, pero sin acción mapeada.")
            print("INFO: Comando no mapeado a una función de la GUI.")


    def cargar_canciones(self):
        """Carga los archivos .mp3 o .wav de la carpeta canciones"""
        if os.path.exists(self.carpeta_canciones):
            for archivo in os.listdir(self.carpeta_canciones):
                if archivo.endswith(".mp3") or archivo.endswith(".wav"):
                    ruta = os.path.join(self.carpeta_canciones, archivo)
                    self.lista_canciones.append(ruta)

                    # Usa QListWidget.addItem() (Asumiendo que has corregido el UI)
                    self.listWidget.addItem(archivo)

                    url = QUrl.fromLocalFile(os.path.abspath(ruta))
                    self.playlist.addMedia(QtMultimedia.QMediaContent(url))

            if len(self.lista_canciones) > 0:
                self.playlist.setCurrentIndex(0)
                self.listWidget.setCurrentRow(0)

    def encender(self):
        """Encender o apagar la bocina"""
        if not self.encendida:
            self.encendida = True
            self.statusbar.showMessage("Bocina encendida ✅")
            self.btn_Encender.setText("Apagar")
        else:
            self.encendida = False
            self.player.stop()
            self.statusbar.showMessage("Bocina apagada ❌")
            self.btn_Encender.setText("Encender")

    def reproducir(self):
        """Reproducir canción seleccionada o la actual"""
        if self.encendida and self.lista_canciones:
            indice = self.listWidget.currentRow()
            if indice >= 0:
                self.playlist.setCurrentIndex(indice)
            self.player.play()

            if self.playlist.mediaCount() > 0 and self.playlist.currentMedia().canonicalUrl().fileName():
                actual = self.playlist.currentMedia().canonicalUrl().fileName()
                self.statusbar.showMessage(f"Reproduciendo: {actual} 🎶")
            else:
                self.statusbar.showMessage("Bocina encendida, lista vacía 🎶")

    def pausar(self):
        if self.encendida:
            self.player.pause()
            self.statusbar.showMessage("Música en pausa ⏸")

    def siguiente(self):
        if self.encendida and self.playlist.mediaCount() > 0:
            self.playlist.next()
            self.player.play()
            indice = self.playlist.currentIndex()
            if indice >= 0:
                self.listWidget.setCurrentRow(indice)
                actual = self.playlist.currentMedia().canonicalUrl().fileName()
                self.statusbar.showMessage(f"Siguiente: {actual} ⏭")

    def anterior(self):
        if self.encendida and self.playlist.mediaCount() > 0:
            self.playlist.previous()
            self.player.play()
            indice = self.playlist.currentIndex()
            if indice >= 0:
                self.listWidget.setCurrentRow(indice)
                actual = self.playlist.currentMedia().canonicalUrl().fileName()
                self.statusbar.showMessage(f"Anterior: {actual} ⏮")

    def silencio(self):
        if self.encendida:
            self.player.setMuted(not self.player.isMuted())
            if self.player.isMuted():
                self.statusbar.showMessage("Silencio 🔇")
            else:
                self.statusbar.showMessage(f"Volumen: {self.player.volume()}% 🔊")

    def aumenta_volumen(self, value):
        if self.encendida:
            if self.player.isMuted():
                self.silencio()
            else:
                cantidad = 10 if not value else value
                vol = min(self.player.volume() + cantidad, 100)
                self.player.setVolume(vol)
                self.slider_Volumen.setValue(vol)
                self.statusbar.showMessage(f"Volumen: {vol}% 🔊")

    def disminuye_volumen(self, value):
        if self.encendida:
            cantidad = 10 if not value else value
            vol = max(self.player.volume() - cantidad, 0)
            self.player.setVolume(vol)
            self.slider_Volumen.setValue(vol)
            self.statusbar.showMessage(f"Volumen: {vol}% 🔉")

    def establece_volumen(self, value):
        if self.encendida:
            if self.player.isMuted():
                self.silencio()
            self.player.setVolume(value)
            self.slider_Volumen.setValue(value)
            self.statusbar.showMessage(f"Volumen: {value}% 🔊")