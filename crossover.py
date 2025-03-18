import constants
import evaluation

import numpy as np

def crossover_function(parent_vector):
    """
    This function recombinates the different parent vectors with the one-point crossover
    :param parent_vector: input vector
    :return: child_vector: vector with the parents recombination
    :return: child_distance: vector with the child distances
    """

    # initialize the variables
    child_vector = np.full((constants.POPULATION_SIZE, constants.N_CODONS), np.nan)
    n_children = 0
    list_parents = [i for i in range(constants.POPULATION_SIZE)] # list parents for crossover

    # loop to create the next generation
    while n_children < constants.POPULATION_SIZE:
        # generate a crossover probability with uniform distribution
        crossover_prob_i = np.random.uniform(0.0,1.0)

        # select the parents to recombinate and delete them from the list to avoid repetition
        parents_crossover = np.zeros(constants.N_INDIVIDUALS, int)
        for k in range(constants.N_INDIVIDUALS):
            parents_crossover[k] = np.random.choice(list_parents)
            list_parents.remove(int(parents_crossover[k]))

        # perform the crossover if the following condition is met
        if crossover_prob_i <= constants.PC:

            # generate the point for crossover
            if constants.LOCAL_SEARCH is True:
                point = constants.CODON_CONSTRAINT * np.random.randint(0, constants.N_CODONS / constants.CODON_CONSTRAINT)
            else:
                point = np.random.randint(0, constants.N_CODONS)

            # create the first child
            child_vector[n_children, :point] = parent_vector[parents_crossover[1], :point]
            child_vector[n_children, point:] = parent_vector[parents_crossover[0], point:]

            # create the second child
            n_children = n_children + 1

            child_vector[n_children, :point] = parent_vector[parents_crossover[0], :point]
            child_vector[n_children, point:] = parent_vector[parents_crossover[1], point:]

            #child_vector[n_children, :(constants.N_CODONS-point)] = parent_vector[parents_crossover[1], point:]
            #child_vector[n_children, (constants.N_CODONS-point):] = parent_vector[parents_crossover[0], :point]

            # go to the next iteration
            n_children = n_children + 1

        # clone the parents if the following condition is met
        else:
            #clone parent 1
            child_vector[n_children, :] = parent_vector[parents_crossover[0], :]
            n_children = n_children + 1

            # clone parent 2
            child_vector[n_children, :] = parent_vector[parents_crossover[1], :]
            n_children = n_children + 1

    return child_vector.astype(int)
