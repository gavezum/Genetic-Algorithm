from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from data.tsp_data import distance_matrix
from copy import deepcopy
from charles.selection import fps, tournament
from charles.mutation import swap_mutation, inversion_mutation
from charles.crossover import cycle_co, pmx_co
from matplotlib import pyplot as plt
import numpy as np


def get_fitness(self):
    """A simple objective function to calculate distances
    for the TSP problem.

    Returns:
        int: the total distance of the path
    """
    fitness = 0
    for i in range(len(self.representation)):
        fitness += distance_matrix[self.representation[i - 1]][self.representation[i]]
    return int(fitness)


def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switches
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]

    for count, i in enumerate(n):
        i[count], i[count + 1] = i[count + 1], i[count]

    n = [Individual(i) for i in n]
    return n


# Monkey patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

fitness_eval = []
for i in range(0,50):
    pop = Population(
        size=60,
        sol_size=len(distance_matrix[0]),
        valid_set=[i for i in range(len(distance_matrix[0]))],
        replacement=False,
        optim="min",
    )

    fitness_eval.append(pop.evolve(
        gens=300,
        select=tournament,
        crossover=pmx_co,
        mutate=inversion_mutation,
        co_p=0.9,
        mu_p=0.1,
        elitism=True
                ))

fitness_mean = np.mean(fitness_eval,axis=0)
fitness_mean = [ i/1000 for i in fitness_mean]
plt.plot(fitness_mean)
plt.xticks(range(1,len(fitness_mean),50))
plt.xlabel('Generation')
plt.ylabel('Fitness in Thousands')
plt.title('Evolution of the fitness alog the generations')
plt.show()