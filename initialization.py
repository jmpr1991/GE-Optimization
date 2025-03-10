import constants
import evaluation

import numpy as np


def initialization_function(vector, n_cities):
    """
    this function initialize the initial vector of the by shuffling it
    :param vector: vector with coordinates
    :param n_cities: number of cities or number of points
    :return: init_vector: matrix built with permutations of the initial vector
    :return: init_distance: distance of the different permutated vectors
    """

    # vector initialization
    init_vector = np.zeros((constants.n_permutations, n_cities, constants.dimension))
    init_distance = np.zeros(constants.n_permutations)

    # shuffle the input vector and create permutations
    for i in range(constants.n_permutations):
        np.random.shuffle(vector)
        init_vector[i, :, :] = vector

        init_distance[i] = evaluation.evaluation_function(init_vector[i, :, :])

    return init_vector, init_distance

