import constants
import evaluation

import numpy as np

def diversity_check_function (child_mutated_vector, child_mutated_fitness, equations, grammar, penalty_weight):

    for ind in range(constants.POPULATION_SIZE):

        # replace individuals with same fitness
        if (np.isin(child_mutated_fitness, fitness)).any() or (np.isin(equations, fun)).any() or fitness > constants.MAX_EVAL_FUN:
            while (np.isin(child_mutated_fitness, fitness)).any() or (np.isin(equations, fun)).any() or fitness > constants.MAX_EVAL_FUN:
                child_mutated_vector[ind] = np.random.randint(2 ** constants.CODON_BITS, size=constants.N_CODONS)
                fun, _ = grammar.generate(child_mutated_vector[ind].astype(int))
                fitness = evaluation.eval_function(fun, penalty_weight)

    return child_mutated_vector, child_mutated_fitness, equations