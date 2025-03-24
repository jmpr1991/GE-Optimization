import constants
import evaluation

import numpy as np

def crossover_function(parent_sel_vector, parent_sel_fitness, all_parent_fitness, grammar, penalty_weight):
    """
    This function recombinates the different parent vectors with the one-point crossover
    :param parent_sel_vector: input vector
    :return: child_vector: vector with the parents recombination
    :return: child_distance: vector with the child distances
    """

    # initialize the variables
    child_vector = np.full((constants.POPULATION_SIZE, constants.N_CODONS), np.nan)
    child_fitness = np.full(constants.POPULATION_SIZE, np.nan)
    n_children = 0
    list_parents = [i for i in range(constants.POPULATION_SIZE)] # list parents for crossover

    # loop to create the next generation
    while n_children < constants.POPULATION_SIZE:
        # generate a crossover probability with uniform distribution
        crossover_prob_i = np.random.uniform(0.0,1.0)

        # select the parents to recombinate and delete them from the list to avoid repetition
        parents_crossover_id0 = np.random.choice(list_parents)
        list_parents.remove(int(parents_crossover_id0))
        parents_crossover_id1 = np.random.choice(list_parents)
        #if (parent_vector[parents_crossover_id0] == parent_vector[parents_crossover_id1]).all():
        #    while (parent_vector[parents_crossover_id0] == parent_vector[parents_crossover_id1]).all():
        #        parents_crossover_id1 = np.random.choice(list_parents)

        list_parents.remove(int(parents_crossover_id1))

        # compute the adaptative crossover probability
        if constants.ADAPTATIVE_VARIATION is True:
            if min([parent_sel_fitness[parents_crossover_id0], parent_sel_fitness[parents_crossover_id1]]) >= np.mean(parent_sel_fitness):
                crossover_prob = constants.PC_K3
            else:
                crossover_prob =  (constants.PC_K1 *
                                   (min([parent_sel_fitness[parents_crossover_id0], parent_sel_fitness[parents_crossover_id1]]) - min(parent_sel_fitness)) /
                                   (np.mean(parent_sel_fitness) - min(parent_sel_fitness)))

        else:
            crossover_prob = constants.PC

        # perform the crossover if the following condition is met
        if crossover_prob_i <= crossover_prob:

            # generate the point for crossover
            if constants.LOCAL_SEARCH is True:
                point = constants.CODON_CONSTRAINT * np.random.randint(0, constants.N_CODONS / constants.CODON_CONSTRAINT)
            else:
                point = np.random.randint(0, constants.N_CODONS)

            # create the first child
            child_vector[n_children] = np.concatenate((parent_sel_vector[parents_crossover_id1, :point], parent_sel_vector[parents_crossover_id0, point:]))
            fun, _ = grammar.generate(child_vector[n_children].astype(int))
            child_fitness[n_children] = evaluation.eval_function(fun, penalty_weight)

            # create the second child
            n_children = n_children + 1
            child_vector[n_children] = np.concatenate((parent_sel_vector[parents_crossover_id0, :point], parent_sel_vector[parents_crossover_id1, point:]))
            fun, _ = grammar.generate(child_vector[n_children].astype(int))
            child_fitness[n_children] = evaluation.eval_function(fun, penalty_weight)

            # go to the next iteration
            n_children = n_children + 1

        # clone the parents if the following condition is met
        else:
            #clone parent 1
            child_vector[n_children] = parent_sel_vector[parents_crossover_id0]
            child_fitness[n_children] = parent_sel_fitness[parents_crossover_id0]
            n_children = n_children + 1

            # clone parent 2
            child_vector[n_children] = parent_sel_vector[parents_crossover_id1]
            child_fitness[n_children] = parent_sel_fitness[parents_crossover_id1]
            n_children = n_children + 1

    return child_vector.astype(int), child_fitness
