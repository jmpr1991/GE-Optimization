import constants
import evaluation

import numpy as np

def survival_elitism_function(child_mutated_vector, child_mutated_fitness, parent_vector, parent_fitness, equations, penalty_weight, grammar):
    """
    This function creates the new generation with elitism, substituting the worst individual of the new generation with
     the best individual of the current generation and
    :param child_mutated_vector: input vector
    :param child_mutated_fitness: input distance
    :param parent_vector: new generation vector
    :param parent_fitness: new generation distance
    :param equations: equations (phenotype)
    :param grammar: grammar
    :param penalty_weight: penalty weight
    :return: new_parent_vector: new generation vector
    :return: new_parent_fitness: new generation distance
    :return: new_equations: new equations (phenotype)
    """

    #select the best individual of the  current population if this condition is met
    if min(parent_fitness) < min(child_mutated_fitness):
        #select the best individual of the parent vector
        index_best_individual = np.argmin(parent_fitness[:])
        best_individual = parent_vector[index_best_individual]

        #select the worst individual of the current generation
        index_worst_individual = np.argmax(child_mutated_fitness)

        # create new generation
        new_parent_vector = child_mutated_vector
        new_parent_vector[index_worst_individual] = best_individual
        new_parent_fitness = child_mutated_fitness
        new_parent_fitness[index_worst_individual] = parent_fitness[index_best_individual]
        new_equations = equations
        new_equations[index_worst_individual], _ = grammar.generate(best_individual)

    # create the new generation without elitism
    else:
        new_parent_vector = child_mutated_vector
        new_parent_fitness = child_mutated_fitness
        new_equations = equations

    #substitute invalid individuals with new ones
    #for ind in range(constants.POPULATION_SIZE):
    #    if new_parent_fitness[ind] is np.nan or new_equations[ind] is None or new_parent_fitness[ind] >= constants.MAX_EVAL_FUN:
    #        while new_parent_fitness[ind] is np.nan or new_equations[ind] is None or new_parent_fitness[ind] >= constants.MAX_EVAL_FUN:
    #            new_parent_vector[ind, :] = np.random.randint(2**constants.CODON_BITS, size=constants.N_CODONS)
    #            new_equations[ind], _ = grammar.generate(new_parent_vector[ind])
    #            new_parent_fitness[ind] = evaluation.eval_function(new_equations[ind], penalty_weight)

    return new_parent_vector, new_parent_fitness, new_equations