import constants
import evaluation

import numpy as np


def initialization_function():
    """
    this function initialize the initial vector
    :return: init_vector: matrix built with permutations of the initial vector
    :return: init_distance: distance of the different permutated vectors
    """

    # vector initialization
    init_vector = np.zeros((constants.population_size, constants.n_codons))

    # shuffle the input vector and create permutations
    for i in range(constants.population_size):

        init_vector[i, :] = np.random.randint(2**constants.codon_bits, size=constants.n_codons)

    return init_vector

