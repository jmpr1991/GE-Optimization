import constants
import evaluation

import numpy as np

def survival_elitism_function(child_mutated_vector, child_mutated_fitness, parent_vector, parent_distance, grammar):
    """
    This function creates the new generation with elitism, substituting the worst individual of the new generation with
     the best individual of the current generation and
    :param child_mutated_vector: input vector
    :param child_mutated_fitness: input distance
    :param parent_vector: new generation vector
    :param parent_distance: new generation distance
    :return: new_parent_vector: new generation vector
    :return: new_parent_distance: new generation distance
    """

    #select the best individual of the  current population if this condition is met
    if min(parent_distance) < min(child_mutated_fitness):
        #select the best individual of the parent vector
        index_best_individual = np.argmin(parent_distance)
        best_individual = parent_vector[index_best_individual, :]

        #select the worst individual of the current generation
        index_worst_individual = np.argmax(child_mutated_fitness)

        # create new generation
        new_parent_vector = child_mutated_vector
        new_parent_vector[index_worst_individual,:] = best_individual
        new_parent_fitness = child_mutated_fitness
        new_parent_fitness[index_worst_individual] = parent_distance[index_best_individual]

    # create the new generation without elitism
    else:
        new_parent_vector = child_mutated_vector
        new_parent_fitness = child_mutated_fitness


    for ind in range(constants.N_INDIVIDUALS):
        if new_parent_fitness[ind] >= constants.MAX_EVAL_FUN:
            new_parent_vector[ind, :] = np.random.randint(2**constants.CODON_BITS, size=constants.N_CODONS)
            output, _ = grammar.generate(new_parent_vector[ind])
            child_mutated_fitness[ind] = evaluation.eval_function(output)

    return new_parent_vector, new_parent_fitness