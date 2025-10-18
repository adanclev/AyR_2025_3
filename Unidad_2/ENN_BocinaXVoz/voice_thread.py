from vosk import KaldiRecognizer
import pyaudio
from PyQt5.QtCore import QThread, pyqtSignal
import time

class VoiceThread(QThread):
    # Señal para enviar el comando reconocido al hilo principal de la UI
    command_recognized = pyqtSignal(str)

    def __init__(self, parent=None, model=None):
        super(VoiceThread, self).__init__(parent)
        self.vosk_model = model
        self.running = True

    def run(self):
        # Inicializar Vosk dentro del hilo (seguro para Vosk y PyAudio)
        recognizer = KaldiRecognizer(self.vosk_model, 16000)
        mic = pyaudio.PyAudio()

        # Abrir stream de audio
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True,
                          frames_per_buffer=8192)  # Aumentamos el buffer para evitar underflows
        stream.start_stream()

        print("🎤 Hilo de Voz iniciado. Escuchando...")

        while self.running:
            try:
                # Leer bloques de audio
                data = stream.read(4096, exception_on_overflow=False)

                if recognizer.AcceptWaveform(data):
                    # Obtener el resultado final
                    result = recognizer.Result()

                    result = result.replace("\"", "").replace("\n", "")
                    posDosPuntos = result.index(":") + 2
                    comando = result[posDosPuntos:-1].strip()

                    if comando:
                        print(f"COMANDO DETECTADO: {comando}")
                        # Emitir la señal al hilo principal de PyQt
                        self.command_recognized.emit(comando)
                else:
                    # Esto se usa para resultados parciales (si quisieras mostrar "estás diciendo...")
                    pass

            except IOError as e:
                # Manejar el error de stream si es necesario
                # print(f"Error de I/O en PyAudio: {e}")
                pass
            except ValueError:
                # El stream puede romperse si la data está mal
                print("Error de valor en stream. Reintentando...")
                time.sleep(0.1)  # Pausar un momento

        # Limpieza al detener el hilo
        stream.stop_stream()
        stream.close()
        mic.terminate()
        print("🛑 Hilo de Voz detenido.")

    def stop(self):
        self.running = False
        self.wait()  # Esperar a que el hilo termine su ejecución
