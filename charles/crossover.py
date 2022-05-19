from random import randint, uniform, sample


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def cycle_co(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p2)
    # While there are still None values in offspring, get the first index of
    # None and start a "cycle" according to the cycle crossover method
    while None in offspring1:
        index = offspring1.index(None)

        val1 = p1[index]
        val2 = p2[index]

        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2


def pmx_co(p1, p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_points = sample(range(len(p1)), 2)
    co_points.sort()

    # where pmx happens
    def pmx(x, y):
        o = [None]*len(x)
        o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

        z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] != None:
                temp = index
                index = y.index(x[temp])
            o[index] = i

        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    o1, o2 = pmx(p1,p2), pmx(p2,p1)
    return o1, o2


def arithmetic_co(p1, p2):
    """Implementation of arithmetic crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)
    # Set a value for alpha between 0 and 1
    alpha = uniform(0, 1)
    # Take weighted sum of two parents, invert alpha for second offspring
    for i in range(len(p1)):
        offspring1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        offspring2[i] = p2[i] * alpha + (1 - alpha) * p1[i]

    return offspring1, offspring2


def order_x1_co(p1,p2):
    """Implementation of partially matched/mapped crossover.

        Args:
            p1 (Individual): First parent for crossover.
            p2 (Individual): Second parent for crossover.

        Returns:
            Individuals: Two offspring, resulting from the crossover.
        """
    co_points = sample(range(len(p1)), 2)
    co_points.sort()

    o1 = [None] * len(p1)
    o2 = [None] * len(p2)

    o1[co_points[0]:co_points[1]] = p1[co_points[0]:co_points[1]]
    o2[co_points[0]:co_points[1]] = p2[co_points[0]:co_points[1]]

    def ox1(p,o):
        invert_p = p[co_points[1]:] + p[:co_points[1]]
        values_co_o = [i for i in invert_p if i not in o]
        for i, element in enumerate(o[co_points[1]:]):
            o[co_points[1]+i]= values_co_o[i]
        if None not in o:
            return o

        for i, element in enumerate(o[:co_points[0]]):
            o[i] = values_co_o[len(o[co_points[1]:])+i]
        return o

    offspring1 = ox1(p2,o1)
    offspring2 = ox1(p1,o2)
    return offspring1, offspring2
if __name__ == '__main__':
    p1, p2 = [9, 8, 4, 5, 7, 6, 1, 3, 2, 10], [8, 10, 4, 5, 6, 7, 1, 2, 9, 3]
    #p1, p2 = [1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 3, 7, 8, 2, 6, 5, 1, 4]
    #p1, p2 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3]
    o1, o2 = pmx_co(p1, p2)
    print(o1,o2)