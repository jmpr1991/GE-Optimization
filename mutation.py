import constants
import evaluation

import numpy as np

def mutation_function(child_vector, child_fitness, grammar, penalty_weight):
    """
    Mutation function for integer representation of the individuals
    :param child_vector: input vector
    :return: child_mutated_vector: new vector after mutation
    """
    # initialize the variables
    child_mutated_vector = np.zeros((constants.POPULATION_SIZE, constants.N_CODONS))
    child_mutated_fitness = [None for i in range(constants.POPULATION_SIZE)]
    equations = [None for i in range(constants.POPULATION_SIZE)]

    for ind in range(constants.POPULATION_SIZE):

        # compute the mutation probability per individual
        if constants.ADAPTATIVE_VARIATION is True:
            if child_fitness[ind] >= np.mean(child_fitness):
                mutation_prob = constants.PM_K4
            else:
                mutation_prob = (constants.PM_K2 *
                                 (child_fitness[ind] - min(child_fitness)) / (np.mean(child_fitness) - min(child_fitness)))

        else:
            mutation_prob = constants.PM

        for i in range(constants.N_CODONS):

            # generate a crossover probability with uniform distribution
            mutation_prob_i = np.random.uniform(0.0, 1.0)

            # proceed with the mutation
            if mutation_prob_i <= mutation_prob:

                # mutate the child
                child_mutated_vector[ind, i] = np.random.randint(2**constants.CODON_BITS)

            # no mutation
            else:
                child_mutated_vector[ind] = child_vector[ind]

        fun, _ = grammar.generate(child_mutated_vector[ind].astype(int))
        fitness = evaluation.eval_function(fun, penalty_weight)

        # replace individuals with same fitness
        if (np.isin(child_mutated_fitness, fitness)).any() or (np.isin(equations, fun)).any() or fitness > constants.MAX_EVAL_FUN:
            while (np.isin(child_mutated_fitness, fitness)).any() or (np.isin(equations, fun)).any() or fitness > constants.MAX_EVAL_FUN:
                child_mutated_vector[ind] = np.random.randint(2**constants.CODON_BITS, size=constants.N_CODONS)
                fun, _ = grammar.generate(child_mutated_vector[ind].astype(int))
                fitness = evaluation.eval_function(fun, penalty_weight)

        child_mutated_fitness[ind] = fitness
        equations[ind] = fun

    return child_mutated_vector.astype(int), child_mutated_fitness, equations