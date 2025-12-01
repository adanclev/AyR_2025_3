#vector inicial
p0 = [0.3, 0.2, 0.5]

# A = Hacer la tarea
# B = Dormir
# C = Jugar
#    A     B     C
T = [
    [0.1, 0.3, 0.6],
    [0.2, 0.5, 0.3],
    [0, 0.5, 0.5]
]

p1 = []

for i in range(len(T)):  #fila
    probabilidad = 0
    for j in range(len(T[i])): #columna
        suma = p0[j] * T[j][i]
        probabilidad += suma
    p1.append(probabilidad)

print("                         A    B   C")
print(f" Resultado de la p1: {p1}")
print(f" El valor mas grande es: {max(p1)}")
