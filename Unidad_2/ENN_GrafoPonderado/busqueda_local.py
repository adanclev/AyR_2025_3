# 03 marzo 2025
import random as rand

minimo = -10
maximo = 10
n = 5

def funcion_objetivo(solucion):
    fo = sum(s**2 for s in solucion)
    return fo

def vecindario(solucion):
    index = rand.randint(0, n - 1)
    new_solucion = solucion.copy()
    new_solucion[index] = rand.randint(minimo, maximo)
    return new_solucion

def crea_solucion():
    solucion = [rand.randint(minimo, maximo) for _ in range(n)]
    return solucion

if __name__ == '__main__':
    it = 100
    solucion_inicial = crea_solucion()
    best_solucion = solucion_inicial.copy()
    best_vo = funcion_objetivo(solucion_inicial)
    print(f'Solución inicial: {solucion_inicial}')
    print(f'Best vo: {best_vo}')

    while it > 0 and best_vo != 0:
        solucion_temp = vecindario(solucion_inicial)
        vo_temp = funcion_objetivo(solucion_temp)

        if vo_temp < best_vo:
            best_solucion = solucion_temp.copy()
            best_vo = vo_temp
        solucion_inicial = solucion_temp
        it -= 1

    print(f'Best Solución: {best_solucion}')
    print(f'Best valor: {best_vo}')