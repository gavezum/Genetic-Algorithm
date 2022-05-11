from random import uniform, choice, choices
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # sorting the pop in ascending manner
        sort_pop = sorted(population, key=attrgetter("fitness"), reverse=False)
        prop_fitness = [1/(i / total_fitness) for i in sort_pop]
        return choices(population=sort_pop, weights=prop_fitness, k=1)[0]

    else:
        raise Exception("No optimization specified (min or max).")


def tournament(population, size=10):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: Best individual in the tournament.
    """

    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for i in range(size)]
    # Check if the problem is max or min
    if population.optim == 'max':
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == 'min':
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")


def rank(population):

    """Rank selection implementation.

        Args:
            population (Population): The population we want to select from.

        Returns:
            Individual: selected individual.
        """
    # check if is max or min and sort the population in the right order
    if population.optim == 'min':
        sort_pop = sorted(population, key=attrgetter("fitness"), reverse=True)
    elif population.optim == 'max':
        sort_pop = sorted(population, key=attrgetter("fitness"), reverse=False)

    # Summing all the rankd. sum 1 because the index starts at zero.
    total_rank = sum([i+1 for i in range(len(population))])
    #calculating the propability of being selected.
    prop_fitness = [(i+1)/total_rank for i in range(len(population))]
    return choices(population=sort_pop, weights=prop_fitness, k=1)[0]