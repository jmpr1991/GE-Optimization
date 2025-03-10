import constants

import numpy as np


def parent_selection_function(individuals_vector, distance_vector, n_cities):
    """
    This function select the parents by tournament. Configuration parameters can be found in constants.py
    :param individuals_vector: vector containing the different vector permuted
    :param distance_vector: vector with the distance of the permuted vectors
    :param n_cities: number of cities (number of points)
    :return: parent_vector: vector with the parent selection
    :return: parent_distance: vector with the parent distance
    """

    # initialize the variables
    parent_vector = np.zeros((constants.n_permutations, n_cities, constants.dimension))
    parent_distance = np.zeros(constants.n_permutations)
    list_parents = [i for i in range(constants.n_permutations)]

    # tournament loop
    for i in range(constants.n_tournaments):
        # select 2 random individuals together with their distance within the list, avoiding repetition
        tournament_individuals = np.zeros(constants.n_individuals, int)
        tournament_distance = np.zeros(constants.n_individuals)
        for k in range(constants.n_individuals):
            tournament_individuals[k] = int(np.random.choice(list_parents))
            tournament_distance[k] = distance_vector[tournament_individuals[k]]
            list_parents.remove(int(tournament_individuals[k]))

            # create a new list if list is empty. This is done because each individual has 2 tournaments
            if not list_parents:
                list_parents = [i for i in range(constants.n_permutations)]

        # chose the individual with the smallest distance
        index = np.argmin(tournament_distance)

        # build the parent vector and parent distance
        parent_vector[i, :, :] = individuals_vector[tournament_individuals[index], :, :]
        parent_distance[i] = min(tournament_distance)

    return parent_vector, parent_distance


     


