import constants
import evaluation

import numpy as np

def mutation_function(child_vector, child_distance, n_cities):
    """
    Mutation function permuting 2 random positions of the vector
    :param child_vector: input vector
    :param child_distance: total distance
    :param n_cities: number of points of the vector
    :return: child_mutated_vector: new vector after mutation
    :return: child_mutated_distance: new distance after mutation
    """
    # initialize the variables
    child_mutated_vector = np.zeros((constants.n_permutations, n_cities, constants.dimension))
    child_mutated_distance = np.zeros(constants.n_permutations)

    for i in range(constants.n_permutations):
        # generate a crossover probability with uniform distribution
        mutation_prob_i = np.random.uniform(0.0, 1.0)

        # proceed with the mutation
        if mutation_prob_i <= constants.pm:

            # generate randomly to set of points
            p0 = np.random.randint(0, n_cities)
            p1 = np.random.randint(0, n_cities)

            # mutate the child
            child_mutated_vector[i, :, :] = child_vector[i, :, :]
            child_mutated_vector[i, p0, :] = child_vector[i, p1, :]
            child_mutated_vector[i, p1, :] = child_vector[i, p0, :]

            child_mutated_distance[i] = evaluation.evaluation_function(child_mutated_vector[i, :, :])

        # no mutation
        else:
            child_mutated_vector[i, :, :] = child_vector[i, :, :]
            child_mutated_distance[i] = child_distance[i]

    return child_mutated_vector, child_mutated_distance
