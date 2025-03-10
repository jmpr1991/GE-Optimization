import constants

import numpy as np


def random_vector_generator_function(n_points):
    """
    This function generates a random vector with the coordinates of the points

    :param n_points: number of points
    :return: vector: vector containing the points coordinates
    """

    vector = np.zeros((n_points, constants.dimension))

    #  build a set of cities with a square shape
    if constants.square_cities:

        vector[0] = [0., 0.]
        vector[1] = [0., constants.square_size]
        vector[2] = [constants.square_size, 0.]
        vector[3] = [constants.square_size, constants.square_size]

        for i in np.linspace(start=4, stop=n_points-1, num=n_points-4, dtype=int):

            axis = np.random.randint(0,4)
            if axis == 0:
                vector[i] = [0, float(np.random.rand(1,1) * constants.square_size)]
            elif axis == 1:
                vector[i] = [float(np.random.rand(1)) * constants.square_size, 0]
            elif axis == 2:
                vector[i] = [float(np.random.rand(1)) * constants.square_size, 1]
            elif axis== 3:
                vector[i] = [1, float(np.random.rand(1) * constants.square_size)]

    # build a random distribution of cities
    elif constants.random_cities:
        for i in range(constants.n_cities):
            vector[i] = np.random.rand(2) * constants.square_size

    return vector

