# -*- coding: utf-8 -*-
"""ejercicio4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JPLKBxW3Gj_feRDxmzv_2YUDrfkcqeOq
"""

!pip install --upgrade deap

#Este ejemplo es usando el camino más corto sin ir a todos los nodos

import numpy as np
import random
from deap import base, creator, tools, algorithms
from deap.tools.crossover import cxOrdered

# Matriz de distancias basada en el grafo proporcionado
MatrizDistancia = np.array([
    [0, 7, 9, 8, 20],  # A
    [7, 0, 10, 4, 11],  # B
    [9, 10, 0, 15, 5],  # C
    [8, 4, 15, 0, 17],  # D
    [20, 11, 5, 17, 0]  # E
])

# Nombres de nodos para referencia
nombres = ['A', 'B', 'C', 'D', 'E']
nodos_relevantes = [0, 2, 4]  # Subconjunto de nodos relevantes (A, C, E)

# Eliminar clases existentes si ya están registradas
if "FitnessMin" in creator.__dict__:
    del creator.FitnessMin
if "Individual" in creator.__dict__:
    del creator.Individual

# Configuración de DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar la distancia
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Generar caminos aleatorios que comiencen en A (0) y terminen en E (4)
def generar_individuo():
    """Genera un camino aleatorio que siempre comienza en A (0) y termina en E (4)"""
    intermedios = nodos_relevantes[1:-1]  # Solo nodos intermedios (C)
    random.shuffle(intermedios)  # Mezcla los nodos intermedios
    return [nodos_relevantes[0]] + intermedios + [nodos_relevantes[-1]]  # A + C + E

toolbox.register("individual", tools.initIterate, creator.Individual, generar_individuo)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalAV(individual):
    """Función objetivo: Calcula el costo total del camino"""
    assert len(individual) == len(nodos_relevantes), "El tamaño del individuo es incorrecto"
    distancia = 0
    for gene1, gene2 in zip(individual[:-1], individual[1:]):  # Costo entre nodos consecutivos
        distancia += MatrizDistancia[gene1][gene2]
    return distancia,  # La coma hace que se retorne una tupla

def mate_fixed(ind1, ind2):
    """Cruce solo para los nodos intermedios (C) usando cxOrdered"""
    inter1 = ind1[1:-1]  # Los nodos intermedios
    inter2 = ind2[1:-1]

    # Verificar si hay al menos dos nodos intermedios para hacer el cruce
    if len(inter1) > 1 and len(inter2) > 1:
        tools.cxOrdered(inter1, inter2)  # Cruce ordenado
        ind1[1:-1] = inter1  # Actualizar los nodos intermedios
        ind2[1:-1] = inter2
    return ind1, ind2

# Registrar las funciones en DEAP
toolbox.register("evaluate", evalAV)
toolbox.register("mate", mate_fixed)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)  # Mutación de índices
toolbox.register("select", tools.selTournament, tournsize=3)  # Selección por torneo

def main():
    random.seed(64)
    pop = toolbox.population(n=300)  # Población inicial de 300 individuos
    hof = tools.HallOfFame(1)  # Mejor individuo encontrado
    stats = tools.Statistics(lambda ind: ind.fitness.values)  # Estadísticas
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # Algoritmo evolutivo
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats, halloffame=hof, verbose=True)
    return pop, hof, log

if __name__ == "__main__":
    pop, hof, log = main()  # Ejecutar el algoritmo
    print("Distancia Mínima a recorrer: %f" % hof[0].fitness.values)  # Mostrar la mejor distancia
    camino_indices = hof[0]
    camino_nombres = [nombres[i] for i in camino_indices]  # Convertir los índices a nombres
    print("Mejor camino (con nombres):", " → ".join(camino_nombres))  # Mostrar el mejor camino con nombres