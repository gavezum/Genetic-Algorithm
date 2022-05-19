from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from data.tsp_data import distance_matrix
from copy import deepcopy
from charles.selection import fps, tournament, rank
from charles.mutation import swap_mutation, inversion_mutation,center_inverse_mutation
from charles.crossover import cycle_co, pmx_co, order_x1_co
from matplotlib import pyplot as plt
import numpy as np
from copy import deepcopy

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

def evolve(population,gen,select,crossover,mutate,prob_mut,optim_op,elit=True ):
    fitness_eval = []
    if optim_op == 'max':
        best_fit = 0
    elif optim_op == 'min':
        best_fit= 99e99
    for _ in range(0,50):

        pop = Population(
            size=population,
            sol_size=len(distance_matrix[0]),
            valid_set=[j for j in range(len(distance_matrix[0]))],
            replacement=False,
            optim=optim_op,
        )

        pop_envolve, best_sol =pop.evolve(
            gens=gen,
            select=select,
            crossover=crossover,
            mutate=mutate,
            co_p=0.90,
            mu_p=prob_mut,
            elitism=True
                 )

        fitness_eval.append(pop_envolve)

        if (optim_op == "max") & (best_sol.fitness > best_fit):
            elit = deepcopy(best_sol)
        elif (optim_op == "min") & (best_sol.fitness < best_fit):
            elit = deepcopy(best_sol)

        best_fit = elit.fitness
    fitness_mean = np.mean(fitness_eval, axis=0)
    fitness_mean = [k / 1000 for k in fitness_mean]

    return fitness_mean, elit

#mean_pmx=evolve(120,350,tournament,pmx_co,inversion_mutation, 'min' ,0.1)
mean_o1,best_sol=evolve(120,350,tournament,order_x1_co,inversion_mutation,0.2,'min')
#mean_cycle=evolve(120,350,tournament,cycle_co,inversion_mutation,'min',0.1)




plt.plot(mean_pmx,'g')
plt.plot(mean_o1,'b')
plt.plot(mean_cycle,'r')
plt.xticks(range(1,len(mean_pmx),50))
plt.xlabel('Generation')
plt.ylabel('Fitness in Thousands')
plt.title('Different cross over algorithms')
plt.legend(['PMX','O1','Cycle'])
plt.show()
