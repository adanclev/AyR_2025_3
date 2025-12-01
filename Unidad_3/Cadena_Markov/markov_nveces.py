#vector inicial
p_actual = [0.3, 0.2, 0.5]

# A = Hacer la tarea
# B = Dormir
# C = Jugar
#    A     B     C
T = [
    [0.1, 0.3, 0.6],
    [0.2, 0.5, 0.3],
    [0, 0.5, 0.5]
]

for paso in range(5):
    p_siguiente = []

    for i in range(len(T)):  #fila
        probabilidad = 0
        for j in range(len(T[i])): #columna
            suma = p_actual[j] * T[j][i]
            probabilidad += suma
        p_siguiente.append(probabilidad)

    print("                         A    B   C")
    print(f" Resultado del paso {paso + 1}: {p_siguiente}")
    print(f" El valor mas grande es: {max(p_siguiente)}")

    p_actual = p_siguiente
