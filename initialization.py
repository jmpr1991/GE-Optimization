import constants
import evaluation

import numpy as np
import random

from constants import MAX_EVAL_FUN


def initialization_function(grammar):
    """
    this function initialize the initial vector
    :return: grammar: grammar
    :return: init_vector: individual vector (genotype)
    :return: parent_fitness: fitness of the intialized vectors
    :return: equations: equations (phenotype)
    """

    # vector initialization
    init_vector = np.zeros((constants.POPULATION_SIZE, constants.N_CODONS))
    parent_fitness = [None for i in range(constants.POPULATION_SIZE)]
    equations = [None for i in range(constants.POPULATION_SIZE)]

    # initialize the population
    i = 0
    while parent_fitness[i] is None or parent_fitness[i] >= constants.MAX_EVAL_FUN:

        init_vector[i, :] = np.random.randint(2**constants.CODON_BITS, size=constants.N_CODONS)

        output, n_codons_used = grammar.generate(init_vector[i, :].astype(int))

        if output is not None and n_codons_used > constants.N_CODONS_2_USE:
            parent_fitness[i] = evaluation.eval_function(output, constants.INITIAL_PENALTY)
            equations[i] = output
            if parent_fitness[i] < constants.MAX_EVAL_FUN:
                i = i + 1

                # termination condition
                if i == constants.POPULATION_SIZE:
                    break

    return init_vector.astype(int), parent_fitness, equations

