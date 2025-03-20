import constants

import numpy as np

def penalty_update_function (fitness_vector, function, generation):

    # select the best individual of the parent vector
    index_best_individual = np.argmin(fitness_vector[:])
    best_function = function[index_best_individual]

    # compute penalty
    x = constants.X_CONSTRAINT
    penalty = abs(float(eval(best_function)) - constants.F0)

    if penalty < constants.DELTA:
        constraint_met = constraint_met + 1