# -*- coding: utf-8 -*-
"""ejercicio2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JPLKBxW3Gj_feRDxmzv_2YUDrfkcqeOq
"""

import numpy as np
import random

entrada_a_oculta = np.random.rand(9, 50)
oculta_a_salida = np.random.rand(50, 9)
sesgo_oculto = np.random.rand(50)
sesgo_salida = np.random.rand(9)


memoria_jugadas = []

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def propagacion_adelante(entrada, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida):
    capa_oculta = sigmoid(np.dot(entrada, entrada_a_oculta) + sesgo_oculto)
    salida = sigmoid(np.dot(capa_oculta, oculta_a_salida) + sesgo_salida)
    return capa_oculta, salida


def retropropagacion(entrada, salida_esperada, salida, capa_oculta, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida, tasa_aprendizaje=0.1):
    error_salida = salida_esperada - salida
    derivada_salida = salida * (1 - salida)
    gradiente_salida = error_salida * derivada_salida

    error_oculta = np.dot(gradiente_salida, oculta_a_salida.T)
    derivada_oculta = capa_oculta * (1 - capa_oculta)
    gradiente_oculta = error_oculta * derivada_oculta

    oculta_a_salida += np.outer(capa_oculta, gradiente_salida) * tasa_aprendizaje
    entrada_a_oculta += np.outer(entrada, gradiente_oculta) * tasa_aprendizaje
    sesgo_salida += gradiente_salida * tasa_aprendizaje
    sesgo_oculto += gradiente_oculta * tasa_aprendizaje

    return entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida

def convertir_a_numerico(tablero):
    return np.array([1 if celda == 'X' else -1 if celda == 'O' else 0 for celda in tablero])

def almacenar_memoria(tablero, jugada, recompensa):
    estado_tablero = convertir_a_numerico(tablero)
    memoria_jugadas.append((estado_tablero, jugada, recompensa))

def obtener_recompensa(tablero, jugador):
    if ganador(tablero, jugador):
        return 1
    elif tablero_lleno(tablero):
        return 0
    else:
        return -0.1


def predecir(tablero, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida):
    capa_oculta, salida = propagacion_adelante(np.array([convertir_a_numerico(tablero)]), entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida)
    return salida

def ganador(tablero, jugador):
    combinaciones_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for comb in combinaciones_ganadoras:
        if tablero[comb[0]] == tablero[comb[1]] == tablero[comb[2]] == jugador:
            return True
    return False

def tablero_lleno(tablero):
    return ' ' not in tablero

def imprimir_tablero(tablero):
    print('-------------')
    for i in range(3):
        print('|', end='')
        for j in range(3):
            print(' ' + tablero[i*3 + j] + ' |', end='')
        print('\n-------------')

def movimiento_computadora(tablero, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida, epsilon=0.1):
    movimientos_disponibles = [i for i, x in enumerate(tablero) if x == ' ']

    if not movimientos_disponibles:
        return None

    if random.random() < epsilon:
        return random.choice(movimientos_disponibles)
    else:
        salida = predecir(tablero, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida)
        movimiento = np.argmax(salida)
        if tablero[movimiento] == ' ':
            return movimiento
        return random.choice(movimientos_disponibles)


def movimiento_jugador(tablero):
    movimiento = -1
    while movimiento < 0 or movimiento > 8 or tablero[movimiento] != ' ':
        try:
            movimiento = int(input('Ingresa tu movimiento (0-8): '))
        except ValueError:
            print('Movimiento inválido. Intenta de nuevo.')
    return movimiento

def entrenar_batch(memoria_jugadas, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida, tasa_aprendizaje=0.2):
    for estado_tablero, jugada, recompensa in memoria_jugadas:
        salida_esperada = np.zeros(9)
        salida_esperada[jugada] = 1
        capa_oculta, salida = propagacion_adelante(estado_tablero, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida)

        salida_esperada[jugada] = recompensa

        entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida = retropropagacion(
            estado_tablero, salida_esperada, salida, capa_oculta, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida, tasa_aprendizaje)

    memoria_jugadas.clear()


def jugar_con_ia():
    tablero = [' '] * 9
    turno = 'X'
    while True:
        imprimir_tablero(tablero)

        if turno == 'X':
            movimiento = movimiento_jugador(tablero)
            tablero[movimiento] = 'X'
            almacenar_memoria(tablero, movimiento, 0)
            if ganador(tablero, 'X'):
                imprimir_tablero(tablero)
                print('¡Ganaste!')
                break
            turno = 'O'
        else:
            movimiento = movimiento_computadora(tablero, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida)

            if movimiento is None:
                print("Empate!")
                break

            tablero[movimiento] = 'O'
            recompensa = obtener_recompensa(tablero, 'O')
            almacenar_memoria(tablero, movimiento, recompensa)
            if ganador(tablero, 'O'):
                imprimir_tablero(tablero)
                print('¡La computadora ganó!')
                break
            elif tablero_lleno(tablero):
                imprimir_tablero(tablero)
                print('¡Empate!')
                break
            turno = 'X'

        entrenar_batch(memoria_jugadas, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida, tasa_aprendizaje=0.1)


for i in range(1000):
    jugar_con_ia()
    entrenar_batch(memoria_jugadas, entrada_a_oculta, oculta_a_salida, sesgo_oculto, sesgo_salida, tasa_aprendizaje=0.1)