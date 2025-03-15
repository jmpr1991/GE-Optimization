import constants
import evaluation

import numpy as np

def mutation_function(child_vector):
    """
    Mutation function for integer representation of the individuals
    :param child_vector: input vector
    :return: child_mutated_vector: new vector after mutation
    """
    # initialize the variables
    child_mutated_vector = np.zeros((constants.POPULATION_SIZE, constants.N_CODONS))

    for ind in range(constants.POPULATION_SIZE):

        for i in range(constants.N_CODONS):

            # generate a crossover probability with uniform distribution
            mutation_prob_i = np.random.uniform(0.0, 1.0)

            # proceed with the mutation
            if mutation_prob_i <= constants.PM:

                # mutate the child
                child_mutated_vector[ind, i] = np.random.randint(2**constants.CODON_BITS)

            # no mutation
            else:
                child_mutated_vector[ind, i] = child_vector[ind, i]

    return child_mutated_vector.astype(int)
