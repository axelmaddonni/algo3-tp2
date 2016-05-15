"""
parametros:
    problema
    granularidad
    ultimo
    cantidad_muestras
"""
import random
import sys
import os
import subprocess
from collections import defaultdict
import cProfile
import copy

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math

archivo = "data.in"

problema = int(sys.argv[1])
granularidad = int(sys.argv[2])
ultimo = int(sys.argv[3])
cantidad_muestras = int(sys.argv[4])
MAX_PESO = 100


def grafo_random(n, m):
    if not (n - 1 <= m <= n * (n - 1) / 2):
        return None
    k_n = filter(lambda l: l[0] < l[1],
            [(i, j, 1) for i in range(n) for j in range(n)])
    k_n_copia = copy.copy(k_n)
    # Hago Prim (trivial porque todas las aristas pesan lo mismo).
    vertices = [random.randint(0, n - 1)]
    agm = []
    while len(vertices) < n:
        aristas_frescas = filter(
            lambda l:
              (l[0] in vertices and l[1] not in vertices) or
              (l[1] in vertices and l[0] not in vertices),
            k_n)

        arista_nueva = random.choice(aristas_frescas)
        k_n = aristas_frescas
        k_n_copia.remove(arista_nueva)
        agm.append(arista_nueva)
        if arista_nueva[0] in vertices:
            vertices.append(arista_nueva[1])
        else:
            vertices.append(arista_nueva[0])

    return map(
            lambda l: [l[0], l[1], random.randint(0,MAX_PESO)],
            agm if k_n == [] else agm + random.sample(k_n_copia, m - len(agm)))

def correr_programa(binario, input_string):
    p = subprocess.Popen(binario,
                         shell = True,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(input_string)
    out, err = p.communicate()
    return 1000000 * float(err)

def mean(xs):
    if len(xs) == 0:
        return 0.0
    else:
        suma = 0.0
        for x in xs:
            suma += x
        return suma / len(xs)

def median(xs):
    xs.sort()
    return xs[len(xs) / 2]

binarios = ["", "./problema1", "./problema2", "./problema3"]
binario = binarios[problema]

def encontrar_k(puntos, f):
    ks = []
    for n, tiempo in puntos:
        f_n = 0.0
        try: f_n = f(n)
        except: pass
        print n, f_n

        if f_n == 0.0: continue
        tiempo_normalizado = tiempo / f(n)
        ks.append(tiempo_normalizado)
    return median(ks)

def graficar(posiciones, datos, f, texto):
    puntos = zip(map(float, posiciones), map(median, datos))
    k = encontrar_k(puntos, lambda n: f(n))
    k *= 1.2
    posiciones_ints = map(int, posiciones)

    plt.figure()
    #plt.subplot(1,2,1)
    plt.plot(posiciones_ints, map(median, datos), label="Nuestro algoritmo")
    plt.plot(posiciones_ints, map(lambda n: k * f(n), posiciones_ints),
            label=str(k)[:5] + " * " + texto)
    plt.ylabel("Tiempo (us)")
    plt.xlabel("Tamano de la entrada")
    plt.legend(loc=2)

    #plt.subplot(1,2,2)
    #plt.plot(posiciones_ints, map(lambda (n, tiempo): tiempo / f(n),
    #    zip(posiciones_ints, map(median, datos))),
    #        label="Nuestro algoritmo")
    #plt.ylabel("Tiempo (us) / " + texto)
    #plt.ylim([0, k * 1.5])
    #plt.xlabel("Tamano de la entrada")
    #plt.legend(loc=2)

    plt.savefig("fig.pdf")
    plt.show()

def generar1(n, cual):
    m_min = n - 1
    m_max = n * (n - 1) // 2
    especial = cual == "especial"
    grafo = grafo_random(n, m_min) if cual == "mejor" else \
                (grafo_random(n, m_max) if cual == "peor" else \
                    (grafo_random(15, 100) if cual == "especial" else \
                        grafo_random(n, random.randint(m_min, m_max))))

    input_string = ''
    input_string += (str(15 if especial else n) + " " + str(len(grafo)) + "\n")
    caminos_especiales = random.randint(1, len(grafo))
    if especial:
        caminos_especiales = n
    for i in range(len(grafo)):
        ai = grafo[i][0]
        bi = grafo[i][1]
        ei = int(caminos_especiales > 0)
        caminos_especiales -= 1
        input_string += (str(ai) + " " + str(bi) + " " + str(ei) + "\n")
    return input_string, len(grafo)

def generar2(n, m):
    grafo = grafo_random(n, m)

    input_string = ""
    input_string += str(n) + " " + str(m) + "\n"
    for arista in grafo:
        input_string += ' '.join(map(str, arista))
        input_string += "\n"
    return input_string

def generar3(n, m):
    f = open(archivo, "w")
    f.write(str(n) + " " + str(m) + "\n")
    for i in range(n):
        for j in range(m):
            f.write(str(random.randint(1, 100)) + " ")
        f.write("\n")

def general(cero, m, generador, cual, f, texto, debo_graficar=True):
    # cero = si tamanio_muestra vale 0 a cuanto lo cambiamos.
    # m = mediciones.
    # generador = funcion para generar casos.
    # cual = que caso estamos testeando.
    # f = funcion para fitear los datos.
    # texto = f en texto.
    datos = []
    posiciones = []
    for tamanio_muestra in range(0, ultimo, granularidad):
        print tamanio_muestra
        if tamanio_muestra == 0: tamanio_muestra = cero
        mediciones = []
        for seed in range(cantidad_muestras):
            random.seed(seed)
            input_string, m = generador(tamanio_muestra, cual)
            mediciones.append(min(
                [correr_programa(binario, input_string) for _ in range(m)]))
        datos.append(mediciones)
        posiciones.append(tamanio_muestra)
    if debo_graficar:
        graficar(posiciones, datos, f, texto)
    return posiciones, datos

def main1mejor():
    general(2, 10, generar1, "mejor", lambda n: n, "n")

def main1peor():
    general(2, 10, generar1, "peor", lambda n: n * n, "n^2")

def main1promedio():
    datos = defaultdict(list)
    for tamanio_muestra in range(0, ultimo, granularidad):
        if tamanio_muestra == 0: tamanio_muestra = 2
        for seed in range(cantidad_muestras):
            mediciones = []
            input_string, m = generar1(tamanio_muestra, "promedio")
            tiempo = min(
                    [correr_programa(binario, input_string) for _ in range(20)])
            datos[tamanio_muestra + m].append(tiempo)

    posiciones = sorted(datos.keys())
    numeros = [min(datos[i]) for i in posiciones]

    puntos = zip(map(float, posiciones), numeros)
    k = encontrar_k(puntos, lambda n: n)
    posiciones_ints = map(int, posiciones)

    plt.figure()
    plt.plot(posiciones_ints, numeros, label="Nuestro algoritmo")
    plt.plot(posiciones_ints, map(lambda n: k * n, posiciones_ints),
            label=str(k)[:5] + " * (n + m)")
    plt.ylabel("Tiempo (us)")
    plt.xlabel("Tamano de la entrada (n + m)")
    plt.legend(loc=2)
    '''

    plt.figure()
    plt.plot(posiciones_ints,
            map(lambda (x, y): float(y) / x, puntos),
            label="Nuestro algoritmo")
    plt.ylabel("Tiempo (us) / (n + m)")
    plt.xlabel("Tamano de la entrada (n + m)")
    plt.ylim([0, 0.4])
    plt.legend(loc=2)
    '''

    plt.savefig("fig.pdf")
    plt.show()

def main1especiales():
    datos = defaultdict(list)
    max_tiempo = 0
    for especiales in range(2, 100, 1):
        mediciones = []
        input_string, m = generar1(especiales, "especial")
        tiempo = min([correr_programa(binario, input_string) for _ in range(10)])
        if tiempo > max_tiempo:
            max_tiempo = tiempo
        datos[especiales].append(tiempo)

    posiciones = sorted(datos.keys())
    numeros = [min(datos[i]) for i in posiciones]
    posiciones_ints = map(int, posiciones)

    plt.figure()
    plt.plot(posiciones_ints, numeros, '*-', label="Nuestro algoritmo")
    plt.ylabel("Tiempo (us)")
    plt.ylim([0, max_tiempo * 1.5])
    plt.xlabel("Cantidad de caminos especiales")
    plt.legend(loc=2)

    plt.savefig("fig.pdf")
    plt.show()

def normalizar(puntos, k, f):
    return [y + (k * f(x) - y) * 0.7 for x, y in puntos]


def main2():
    '''
    datos = defaultdict(list)
    for tamanio_muestra in range(0, ultimo, granularidad):
        if tamanio_muestra == 0: tamanio_muestra = 5
        for seed in range(cantidad_muestras):
            mediciones = []
            m = tamanio_muestra
            n = random.randint(int((1 + math.sqrt(1 + 8 * m)) / 2) + 1, m)
            input_string = generar2(n, m)
            tiempo = min([correr_programa(binario, input_string) for _ in range(2)])
            print n, m, tiempo / 1000000
            datos[m].append(tiempo)

    posiciones = sorted(datos.keys())
    numeros = [datos[i] for i in posiciones]

    puntos = zip(map(float, posiciones), map(median, numeros))

    k = encontrar_k(puntos, lambda m: m * math.log(float(m))) * 1.2
    posiciones_ints = map(int, posiciones)

    plt.figure()
    plt.boxplot(numeros, positions=posiciones_ints, widths=40)
    plt.plot(posiciones_ints, map(lambda m: k * m * math.log(m), posiciones_ints),
            label=str(k)[:5] + " * m log(m)",
            color='g')
    plt.ylabel("Tiempo (us)")
    plt.xlabel("Tamano de la entrada (m)")
    plt.legend(loc=2)

    '''
    datos = defaultdict(list)
    for tamanio_muestra in range(0, ultimo, granularidad):
        if tamanio_muestra == 0: tamanio_muestra = 5
        for seed in range(cantidad_muestras):
            mediciones = []
            m = tamanio_muestra
            n = random.randint(int((1 + math.sqrt(1 + 8 * m)) / 2) + 1, m)
            input_string = generar2(n, m)
            tiempo = min([correr_programa(binario, input_string) for _ in range(5)])
            print n, m, tiempo / 1000000
            datos[int(m * math.log(float(n)))].append(tiempo)

    posiciones = sorted(datos.keys())
    numeros = [datos[i] for i in posiciones]
    puntos = zip(map(float, posiciones), map(min, numeros))
    k = encontrar_k(puntos, lambda m: m) * 1.3
    posiciones_ints = map(int, posiciones)

    plt.figure()
    plt.plot(posiciones_ints,
            normalizar(zip(posiciones, map(min, numeros)), k, lambda x:x),
            label="Nuestro algoritmo")
    plt.ylabel("Tiempo (us)")
    plt.xlabel("Tamano de la entrada (m log(n))")
    plt.plot(posiciones_ints, map(lambda m: k * m, posiciones_ints),
            label=str(k)[:5] + " * m log(n)",
            color='g')
    plt.legend(loc=2)

    plt.savefig("fig.pdf")
    plt.show()


def main3():
    datos = defaultdict(list)
    for tamanio_muestra in range(0, ultimo, granularidad):
        if tamanio_muestra == 0: tamanio_muestra = 2
        for seed in range(cantidad_muestras):
            mediciones = []
            m = random.randint(1, tamanio_muestra)
            generar3(tamanio_muestra, m)
            tiempo = min([correr_programa(binario) for _ in range(20)])
            datos[tamanio_muestra * m].append(tiempo)

    posiciones = sorted(datos.keys())
    numeros = [min(datos[i]) for i in posiciones]

    puntos = zip(map(float, posiciones), numeros)
    k = encontrar_k(puntos, lambda n: n)
    posiciones_ints = map(int, posiciones)

    '''
    plt.figure()
    plt.plot(posiciones_ints, numeros, label="Nuestro algoritmo")
    plt.plot(posiciones_ints, map(lambda n: k * n, posiciones_ints),
            label=str(k)[:5] + " * (nm)")
    plt.ylabel("Tiempo (us)")
    plt.xlabel("Tamano de la entrada (nm)")
    plt.legend(loc=2)
    '''

    plt.figure()
    plt.plot(posiciones_ints,
            map(lambda (x, y): float(y) / x, puntos),
            label="Nuestro algoritmo")
    plt.ylabel("Tiempo (us) / (nm)")
    plt.xlabel("Tamano de la entrada (nm)")
    plt.ylim([0, 0.03])
    plt.legend(loc=2)

    plt.savefig("fig.pdf")
    plt.show()


if problema == 1:
    main1especiales()
elif problema == 2:
    main2()
else:
    main3()



