from matplotlib import pyplot as plt
import numpy as np

def plot (*plots) :
    """ A function that will plot only one line with the generations on the X-axis
    and the mean of each generation on the Y-axis.
    Args:
        *plots: plots, that we want to show
    """
    for _ in range(len(plots)):
        fitness_mean = np.mean(plots,axis=1)
        plt.plot(fitness_mean)
    plt.xticks(range(1,len(fitness_mean)))
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Evolution of the fitnees alog the generations')
    plt.show()


