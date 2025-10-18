PORCIENTOS = {
    "diez": 10,
    "veinte": 20,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100
}

DICCIONARIO = {
    "accion_estado": ["encender", "apagar", "prende", "apaga"],
    "accion_ajuste": ["sube", "baja", "aumenta", "disminuye", "establece", "establecer"],
    "accion_play": ["reproducir", "pausar", "reproduce", "pausa", "siguiente", "anterior"],
    "accion_mute": ["silenciar", "silencia", "silencio"],
    "objeto_dispositivo": ["bocina", "altavoz"],
    "objeto_magnitud": ["volumen", "canción", "sonido", "audio"],
    "valor": ["máximo", "cero"] + [key for key in PORCIENTOS.keys()]
}

REGLAS = {
    "accion_estado": ["objeto_dispositivo"],
    "accion_ajuste": ["objeto_magnitud", "valor"],
    "accion_play": ["objeto_magnitud"],
    "accion_mute": ["objeto_dispositivo"],
}

VOSK_MODEL_PATH = "model/"

if __name__ == '__main__':
    print(DICCIONARIO)

