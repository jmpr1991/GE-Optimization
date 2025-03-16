import constants
import evaluation

import numpy as np
import random

from constants import MAX_EVAL_FUN


def initialization_function(grammar):
    """
    this function initialize the initial vector
    :return: init_vector: matrix built with permutations of the initial vector
    :return: init_distance: distance of the different permutated vectors
    """

    # vector initialization
    init_vector = np.zeros((constants.POPULATION_SIZE, constants.N_CODONS))
    parent_fitness = [None for i in range(constants.POPULATION_SIZE)]

    # initialize the population
    i = 0
    while parent_fitness[i] is None or parent_fitness[i] >= constants.MAX_EVAL_FUN:

        init_vector[i, :] = np.random.randint(2**constants.CODON_BITS, size=constants.N_CODONS)

        output, _ = grammar.generate(init_vector[i, :].astype(int))

        if output is not None:
            parent_fitness[i] = evaluation.eval_function(output)
            if parent_fitness[i] < constants.MAX_EVAL_FUN:
                i = i + 1

                # termination condition
                if i == constants.POPULATION_SIZE:
                    break

    return init_vector.astype(int), parent_fitness

