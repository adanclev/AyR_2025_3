from vosk import KaldiRecognizer
import pyaudio
from PyQt5.QtCore import QThread, pyqtSignal
import time

class VoiceThread(QThread):
    command_recognized = pyqtSignal(str)

    def __init__(self, parent=None, model=None):
        super(VoiceThread, self).__init__(parent)
        self.vosk_model = model
        self.running = True

    def run(self):
        recognizer = KaldiRecognizer(self.vosk_model, 16000)
        mic = pyaudio.PyAudio()

        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True,
                          frames_per_buffer=8192)
        stream.start_stream()

        print("🎤 Hilo de Voz iniciado. Escuchando...")

        while self.running:
            try:
                data = stream.read(4096, exception_on_overflow=False)

                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()

                    result = result.replace("\"", "").replace("\n", "")
                    posDosPuntos = result.index(":") + 2
                    comando = result[posDosPuntos:-1].strip()

                    if comando:
                        print(f"COMANDO DETECTADO: {comando}")
                        self.command_recognized.emit(comando)
                else:
                    pass

            except IOError as e:
                pass
            except ValueError:
                print("Error de valor en stream. Reintentando...")
                time.sleep(0.1)

        # Limpieza al detener el hilo
        stream.stop_stream()
        stream.close()
        mic.terminate()
        print("🛑 Hilo de Voz detenido.")

    def stop(self):
        self.running = False
        self.wait()
