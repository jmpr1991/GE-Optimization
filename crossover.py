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

            child_1 = np.concatenate((parent_sel_vector[parents_crossover_id1, :point], parent_sel_vector[parents_crossover_id0, point:]))
            fun_1, _ = grammar.generate(child_1.astype(int))
            child_fitness_1 = evaluation.eval_function(fun_1, penalty_weight)

            child_2 = np.concatenate((parent_sel_vector[parents_crossover_id0, :point], parent_sel_vector[parents_crossover_id1, point:]))
            fun_2, _ = grammar.generate(child_2.astype(int))
            child_fitness_2 = evaluation.eval_function(fun_2, penalty_weight)

            child_3 = np.concatenate((parent_sel_vector[parents_crossover_id1, :point], parent_sel_vector[parents_crossover_id0, :(constants.N_CODONS-point)]))
            fun_3, _ = grammar.generate(child_3.astype(int))
            child_fitness_3 = evaluation.eval_function(fun_3, penalty_weight)

            child_4 = np.concatenate((parent_sel_vector[parents_crossover_id0, :point], parent_sel_vector[parents_crossover_id1, :(constants.N_CODONS-point)]))
            fun_4, _ = grammar.generate(child_4.astype(int))
            child_fitness_4 = evaluation.eval_function(fun_4, penalty_weight)

            potential_children = [child_1, child_2, child_3, child_4]
            potential_fun = [fun_1, fun_2, fun_3, fun_4]
            potential_children_fitness = [child_fitness_1, child_fitness_2, child_fitness_3, child_fitness_4]

            index1 = np.argmin(potential_children_fitness)

            # create the first child
            child_vector[n_children] = potential_children[index1]
            child_fitness[n_children] = potential_children_fitness[index1]

            # create the second child
            n_children = n_children + 1
            potential_children.pop(index1)
            potential_children_fitness.pop(index1)
            index2 = np.argmin(potential_children_fitness)
            child_vector[n_children] = potential_children[index2]
            child_fitness[n_children] = potential_children_fitness[index2]

            # create the first child
            #child_vector[n_children] = np.concatenate((parent_sel_vector[parents_crossover_id1, :point], parent_sel_vector[parents_crossover_id0, point:]))
            #fun, _ = grammar.generate(child_vector[n_children].astype(int))
            #child_fitness[n_children] = evaluation.eval_function(fun, penalty_weight)

            # create the second child
            #n_children = n_children + 1
            #child_vector[n_children] = np.concatenate((parent_sel_vector[parents_crossover_id0, :point], parent_sel_vector[parents_crossover_id1, point:]))
            #fun, _ = grammar.generate(child_vector[n_children].astype(int))
            #child_fitness[n_children] = evaluation.eval_function(fun, penalty_weight)

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
