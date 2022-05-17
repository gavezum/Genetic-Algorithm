from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from data.tsp_data import distance_matrix
from copy import deepcopy
from charles.selection import fps, tournament, rank
from charles.mutation import swap_mutation, inversion_mutation,center_inverse_mutation
from charles.crossover import cycle_co, pmx_co, order_x1_co
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

def evolve(population,gen,select,crossover,mutate,prob_mut,elit=True ):
    fitness_eval = []
    for _ in range(0,50):

        pop = Population(
            size=population,
            sol_size=len(distance_matrix[0]),
            valid_set=[j for j in range(len(distance_matrix[0]))],
            replacement=False,
            optim="min",
        )

        fitness_eval.append(pop.evolve(
            gens=gen,
            select=select,
            crossover=crossover,
            mutate=mutate,
            co_p=cros_prob,
            mu_p=prob_mut,
            elitism=True
                 ))
        #print(i)
    fitness_mean = np.mean(fitness_eval, axis=0)
    fitness_mean = [k / 1000 for k in fitness_mean]
    return fitness_mean
print(1)
mean_orderx1_tournament=evolve(120,350,tournament,order_x1_co,inversion_mutation,0.1)
print(1)
mean_orderx1_tournament_elitf=evolve(120,350,tournament,order_x1_co,inversion_mutation,0.2)
#mean_orderx1_fps =evolve(120,350,fps,order_x1_co,inversion_mutation)



plt.plot(mean_orderx1_tournament,'g')
plt.plot(mean_orderx1_tournament_elitf,'r')
plt.xticks(range(1,len(mean_orderx1_tournament),50))
plt.xlabel('Generation')
plt.ylabel('Fitness in Thousands')
plt.title('Different Mutation Probabilities')
plt.legend(['P_mu = 0.1','P_mu = 0.2'])
plt.show()
