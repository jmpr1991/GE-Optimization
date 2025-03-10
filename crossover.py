import constants
import evaluation

import numpy as np

def crossover_function(parent_vector, parent_distance, n_cities):
    """
    This function recombinates the different parent vectors with the Partially Mapped Crossover method
    :param parent_vector: input vector
    :param parent_distance: input distance
    :param n_cities: vector size
    :return: child_vector: vector with the parents recombination
    :return: child_distance: vector with the child distances
    """

    # initialize the variables
    child_vector = np.full((constants.n_permutations, n_cities, constants.dimension), np.nan)
    child_distance = np.zeros(constants.n_permutations)
    n_children = 0
    list_parents = [i for i in range(constants.n_permutations)] # list parents for crossover

    # loop to create the next generation
    while n_children < constants.n_permutations:
        # generate a crossover probability with uniform distribution
        crossover_prob_i = np.random.uniform(0.0,1.0)

        # select the parents to recombinate and delete them from the list to avoid repetition
        parents_crossover = np.zeros(constants.n_individuals, int)
        for k in range(constants.n_individuals):
            parents_crossover[k] = np.random.choice(list_parents)
            list_parents.remove(int(parents_crossover[k]))

        # perform the crossover if the following condition is met
        if crossover_prob_i <= constants.pc:

            # generate the segment for crossover avoiding the edges
            s0 = np.random.randint(2, n_cities - 2)
            sf = np.random.randint(s0 + 1, n_cities - 1)

            # create the first child
            child_vector[n_children, :, :] = pmx_crossover(parent_vector[parents_crossover[0], :, :],
                                                           parent_vector[parents_crossover[1], :, :],
                                                           s0, sf)

            child_distance[n_children] = evaluation.evaluation_function(child_vector[n_children, :, :])

            # create the second child
            n_children = n_children + 1

            child_vector[n_children, :, :] = pmx_crossover(parent_vector[parents_crossover[1], :, :],
                                                           parent_vector[parents_crossover[0], :, :],
                                                           s0, sf)

            child_distance[n_children] = evaluation.evaluation_function(child_vector[n_children, :, :])

            # go to the next iteration
            n_children = n_children + 1

        # clone the parents if the following condition is met
        else:
            #clone parent 1
            child_vector[n_children, :, :] = parent_vector[parents_crossover[0], :, :]
            child_distance[n_children] = parent_distance[parents_crossover[0]]
            n_children = n_children + 1

            # clone parent 2
            child_vector[n_children, :, :] = parent_vector[parents_crossover[1], :, :]
            child_distance[n_children] = parent_distance[parents_crossover[1]]
            n_children = n_children + 1

    return child_vector, child_distance


def pmx_crossover(parent1, parent2, s0, sf):
    """
    This function implement the partial mapped crossover
    :param parent1: first parent
    :param parent2:second parent
    :param s0: first edge of the segment
    :param sf: last edge of the segment
    :return: offspring: child solution
    """

    offspring = np.full((constants.n_cities, constants.dimension), np.nan)

    offspring[s0 - 1:sf, :] = parent1[s0 - 1:sf, :]

    # implementation of the partial mapped crossover
    left_candidates = []
    for i in np.concatenate([np.arange(0, s0 - 1), np.arange(sf, constants.n_cities)]):
        candidate = parent1[i, :]
        if candidate.tolist() not in parent2[s0 - 1:sf, :].tolist():
            array_index = np.where(candidate == parent2[:, :])[0]
            unique, counts = np.unique(array_index, return_counts=True)
            index = int(unique[np.where(counts > 1)])
            offspring[index, :] = candidate
        else:
            left_candidates.append(candidate)

    for candidate in left_candidates:
        index = np.argwhere(np.isnan((offspring[:, :])))[0][0]
        offspring[index, :] = candidate

    return offspring