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

import matplotlib.pyplot as plt
import numpy as np
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
            [[i, j, 1] for i in range(n) for j in range(n)])
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
        k_n.remove(arista_nueva)
        agm.append(arista_nueva)
        if arista_nueva[0] in vertices:
            vertices.append(arista_nueva[1])
        else:
            vertices.append(arista_nueva[0])

    return map(
            lambda l: [l[0], l[1], random.randint(0,MAX_PESO)],
            agm if k_n == [] else agm + random.sample(k_n, m - len(agm)))

def correr_programa(binario):
    p = subprocess.Popen("cat " + archivo + " | " + binario,
                         shell = True,
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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
        f_n = 0
        try: f_n = f(n)
        except: pass

        if f_n == 0: continue
        tiempo_normalizado = tiempo / f(n)
        ks.append(tiempo_normalizado)
    return median(ks)

def graficar(posiciones, datos, f, texto):
    puntos = zip(map(float, posiciones), map(median, datos))
    k = encontrar_k(puntos, lambda n: f(n))
    posiciones_ints = map(int, posiciones)

    plt.figure()
    plt.subplot(1,2,1)
    plt.plot(posiciones_ints, map(median, datos), label="Nuestro algoritmo")
    plt.plot(posiciones_ints, map(lambda n: k * f(n), posiciones_ints),
            label=str(k) + " * " + texto)
    plt.ylabel("Tiempo (us)")
    plt.xlabel("Tamano de la entrada")
    plt.legend(loc=2)

    plt.subplot(1,2,2)
    plt.plot(posiciones_ints, map(lambda (n, tiempo): tiempo / f(n),
        zip(posiciones_ints, map(median, datos))),
            label="Nuestro algoritmo")
    plt.ylabel("Tiempo (us) / " + texto)
    plt.ylim([0, k * 1.5])
    plt.xlabel("Tamano de la entrada")
    plt.legend(loc=2)

    plt.show()

def generar1(n, cual):
    m_min = n - 1
    m_max = n * (n - 1) // 2
    grafo = grafo_random(n, m_min) if cual == "mejor" else \
                (grafo_random(n, m_max) if cual == "peor" else \
                    grafo_random(n, random.randint(m_min, m_max)))

    f = open(archivo, "w")
    f.write(str(n) + " " + str(len(grafo)) + "\n")
    caminos_especiales = random.randint(1, len(grafo))
    for i in range(len(grafo)):
        ai = grafo[i][0]
        bi = grafo[i][1]
        ei = int(caminos_especiales > 0)
        caminos_especiales -= 1
        f.write(str(ai) + " " + str(bi) + " " + str(ei) + "\n")
    return len(grafo)


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
        if tamanio_muestra == 0: tamanio_muestra = cero
        mediciones = []
        for seed in range(cantidad_muestras):
            random.seed(seed)
            generador(tamanio_muestra, cual)
            mediciones.append(min([correr_programa(binario) for _ in range(m)]))
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
    posiciones, datos = general(2, 10, generar1, "promedio", None, None, False)

    puntos = zip(map(float, posiciones), map(max, datos))
    k = encontrar_k(puntos, lambda n: f(n))
    posiciones_ints = map(int, posiciones)

    plt.figure()
    plt.subplot(1,2,1)
    plt.boxplot(posiciones_ints, map(median, datos), label="Nuestro algoritmo")
    plt.plot(posiciones_ints, map(lambda n: k * f(n), posiciones_ints),
            label=str(k) + " * " + texto)
    plt.ylabel("Tiempo (us)")
    plt.xlabel("Tamano de la entrada")
    plt.legend(loc=2)

    plt.subplot(1,2,2)
    plt.plot(posiciones_ints, map(lambda (n, tiempo): tiempo / f(n),
        zip(posiciones_ints, map(median, datos))),
            label="Nuestro algoritmo")
    plt.ylabel("Tiempo (us) / " + texto)
    plt.ylim([0, k * 1.5])
    plt.xlabel("Tamano de la entrada")
    plt.legend(loc=2)

    plt.show()


if problema == 1:
    main1peor()
elif problema == 2:
    main2()
else:
    main3()



