import constants
import evaluation

import numpy as np
import random


def initialization_function():
    """
    this function initialize the initial vector
    :return: init_vector: matrix built with permutations of the initial vector
    :return: init_distance: distance of the different permutated vectors
    """

    # vector initialization
    init_vector = np.zeros((constants.POPULATION_SIZE, constants.N_CODONS))

    # shuffle the input vector and create permutations
    for i in range(constants.POPULATION_SIZE):

        init_vector[i, :] = np.random.randint(2**constants.CODON_BITS, size=constants.N_CODONS)

    return init_vector.astype(int)

