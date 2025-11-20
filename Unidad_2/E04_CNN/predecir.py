import os

import numpy as np
#from keras.preprocessing.image import load_img, img_to_array  #deprecated en tf 2.9
#from tensorflow.keras.utils import load_img  #alternative 1
from keras.utils import load_img, img_to_array #alternative 2

from keras.models import load_model

# Convolutional Neuronal Network
alto, largo = 300, 300
modelo = "../E04_CNN/modelo/modelo.keras" #./modelo/modelo.h5'
pesos = '../E04_CNN/modelo/pesos.weights.h5'

cnn = load_model(modelo)
cnn.load_weights(pesos)
UMBRAL = 0.85

def predict(file):
    imagen_a_predecir = load_img(file, target_size = (alto, largo), color_mode="grayscale")
    imagen_a_predecir = img_to_array(imagen_a_predecir)
    imagen_a_predecir = imagen_a_predecir / 255.0 ## nueva
    imagen_a_predecir = np.expand_dims(imagen_a_predecir, axis=0) #agrega una dimension adicional
    arreglo = cnn.predict(imagen_a_predecir) ## [[1,0,0,0,0,0]]
    resultado = arreglo[0]
    #print(resultado)

    probabilidad_maxima = np.max(arreglo[0])

    respuesta = np.argmax(resultado) #indice del valor mas alto

    if probabilidad_maxima >= UMBRAL:
        match respuesta:
            case 0:
                return 'C1-Adan'
            case 1:
                return 'C2-Poncho'
            case 2:
                return 'C3-Pavel'
            case 3:
                return 'C4-Cristobal'
            case _:
                return '----'
    else:
        print("Desconocido")

#predict('/Users/alejandrohumbertogarciaruiz/Desktop/introTensorFlow/F3-Prueba/2-cisne/cisne_31.jpg')

def get_folders_name_from(from_location):
    list_dir = os.listdir(from_location)
    # folders = [archivo for archivo in listDir if os.path.splitext(archivo)[1] == ""]
    # the above is equals to ....
    folders = []
    for file in list_dir:
        temp = os.path.splitext(file)
        if temp[1] == "":
            folders.append(temp[0])
    folders.sort()
    # folders.remove('.DS_Store') #solo en mac
    return folders

#foto cuando fue creado el modelo, foto eficiencia y foto
# Proyecto 1 - Tensorflow -> 85 %
# proyecto 2 - Entrenar
def probar_red_neuronal():
    base_location = "../../Archivos/Clases-individuos/F3-Prueba/" #'./F3-Prueba/'
    #base_location = "../E04_CNN/F3-Prueba/" #'./F3-Prueba/'

    folders = get_folders_name_from(base_location)

    correct = 0
    count_predictions = 0
    for folder in folders:
        files = [archivo for archivo in os.listdir(base_location + '/' + folder) if archivo.endswith(".jpg") or archivo.endswith(".jpeg") or archivo.endswith(".png")]
        for file in files:
            composed_location = base_location + folder + '/' + file
            prediction =  predict(composed_location)
            print('Folder Name: ', folder, ' Prediction: ',  prediction, " Resulto: ", prediction in folder)
            count_predictions += 1
            if prediction in folder:
                correct +=1

    print("Efficiency: ", (correct/count_predictions*100))

probar_red_neuronal()
#predicho = predict("../E04_CNN/F3-Prueba/C1-Adan/adan_foto_0.png")
#predicho = predict("../E04_CNN/F3-Prueba/C2-Poncho/Alfonso_foto_10.png")
#predicho = predict("../E04_CNN/F3-Prueba/C4-Cristobal/cristobal_foto_50.png")
#predicho = predict("../E04_CNN/F3-Prueba/C3-Pavel/Pavel_foto_2.png")
#predicho = predict("../../Archivos/Images/poncho1.png")
#predicho = predict("../../Archivos/Images/persona1.jpg")
#print(predicho)