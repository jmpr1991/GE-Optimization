import constants

import numpy as np


def parent_selection_function(individuals_vector, fitness_vector):
    """
    This function select the parents by tournament. Configuration parameters can be found in constants.py
    :param individuals_vector: vector containing the genotype of the individuals of the population
    :param fitness_vector: vector with the individuals fitness
    :return: parent_vector: vector with the parent selection
    :return: parent_fitness: vector with the parent distance
    """

    # initialize the variables
    parent_vector = np.zeros((constants.POPULATION_SIZE, constants.N_CODONS))
    parent_fitness = np.zeros(constants.POPULATION_SIZE)
    list_parents = [i for i in range(constants.POPULATION_SIZE)]

    # tournament loop
    for i in range(constants.N_TOURNAMENTS):
        # select 2 random individuals together with their distance within the list, avoiding repetition
        tournament_individuals = np.zeros(constants.N_INDIVIDUALS, int)
        tournament_fitness = np.zeros(constants.N_INDIVIDUALS)
        for k in range(constants.N_INDIVIDUALS):
            tournament_individuals[k] = int(np.random.choice(list_parents))
            tournament_fitness[k] = fitness_vector[tournament_individuals[k]]
            list_parents.remove(int(tournament_individuals[k]))

            # create a new list if list is empty. This is done because each individual has 2 tournaments
            if not list_parents:
                list_parents = [i for i in range(constants.POPULATION_SIZE)]

        # chose the individual with the smallest distance
        index = np.argmin(tournament_fitness)

        # build the parent vector and parent distance
        parent_vector[i] = individuals_vector[tournament_individuals[index], :]
        parent_fitness[i] = min(tournament_fitness)

    return parent_vector.astype(int), parent_fitness


     


