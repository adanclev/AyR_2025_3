import cv2

path_img = '../../Archivos/Images/poncho1.png'
alto, largo = 300, 300

clases = {
    0: "Adan",
    1: "Poncho",
    2: "Pavel",
    3: "Cristobal"
}

print("Cargando modelos...")
eigen_model = cv2.face.EigenFaceRecognizer_create()
# fisher_model = cv2.face.FisherFaceRecognizer_create()
# lbph_model = cv2.face.LBPHFaceRecognizer_create()

try:
    eigen_model.read('modelo/modeloEigenFace.xml')
    # fisher.model.read('modelo/modeloFisherFace.xml')
    # lbph_model.read('modelo/modeloLBPHFace.xml')
    print("Modelos cargados exitosamente")
except Exception as e:
    print(f"Error cargando modelos: {e}")
    exit()

img = cv2.imread(path_img)
# img = img / 255.0
if img is None:
    print("Error: No se encuentra la imagen.")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = gray / 255.0

img_resized = cv2.resize(gray, (largo, alto), interpolation=cv2.INTER_CUBIC)

# predecir
lab_e, conf_e = eigen_model.predict(img_resized)
# lab_f, conf_f = fisher.predict(img_resized)
#lab_l, conf_l = lbph.predict(img_resized)

print("\n" + "="*30)
print(f"RESULTADOS PARA: {path_img}")

print(f"[EigenFace]  Identificó a: {clases.get(lab_e)} | Confianza: {conf_e:.2f}")
# print(f"[FisherFace] Identificó a: {clases.get(lab_f)} | Confianza: {conf_f:.2f}")
#print(f"[LBPH]       Identificó a: {clases.get(lab_l)} | Confianza: {conf_l:.2f}")