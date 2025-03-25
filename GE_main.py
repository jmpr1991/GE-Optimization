import constants
import decoder
import evaluation
import initialization
import parent_selection
import crossover
import mutation
import survival_elitism
import statistics_plots

import numpy as np
import math


def main():

    np.random.seed(2)  # seed of the random function to avoid errors in the vector generator

    # Read grammar
    bnf_grammar = decoder.Grammar("arithmetic.pybnf")

    # initialize variables for statistical analysis
    all_min_fitness = []
    all_mean_fitness = []
    all_std_fitness = []
    total_executions = []
    solution = []

    # initialize success rate and success mean evaluations number (pex) parameters
    success_rate = 0
    pex = []

    for execution_i in range(constants.N_EXECUTIONS):
        print("execution {}".format(execution_i+1), "on going")

        # constraints parameters initialization
        constraint_gen_met = 0
        constraint_gen_not_met = 0

        # initialize the population
        parent_vector, parent_fitness, equations = initialization.initialization_function(bnf_grammar)

        #initialize penalty to meet constraints
        penalty_weight = constants.INITIAL_PENALTY

        # initialize variables
        min_fitness = []
        mean_fitness = []
        std_fitness = []
        number_generations = 0
        termination_generation = 0

        # generation evolution loop
        while number_generations < constants.N_GENERATIONS:
            print(number_generations)

            # parent selection
            parent_sel_vector, parent_sel_fitness = parent_selection.parent_selection_function(parent_vector, parent_fitness)

            # crossover
            child_vector, child_fitness = crossover.crossover_function(parent_sel_vector, parent_sel_fitness, parent_fitness, bnf_grammar, penalty_weight)

            # mutation
            child_mutated_vector, child_mutated_fitness, mutated_equations = mutation.mutation_function(child_vector, child_fitness, bnf_grammar, penalty_weight)

            # survival selections and elitism
            new_parent_vector, new_parent_fitness, new_equations = survival_elitism.survival_elitism_function(child_mutated_vector,
                                                                                               child_mutated_fitness,
                                                                                               parent_vector,
                                                                                               parent_fitness,
                                                                                               mutated_equations,
                                                                                               penalty_weight,
                                                                                               bnf_grammar)

            # update GA parameters
            # select the best individual of the parent vector
            index_best_individual = np.argmin(new_parent_fitness[:])
            best_function = new_equations[index_best_individual]
            print(best_function)
            print(penalty_weight)
            print(new_parent_fitness[index_best_individual])

            # compute penalty
            x = constants.X_CONSTRAINT
            try:
                penalty = abs(eval(best_function) - constants.F0)
            except (ZeroDivisionError, OverflowError, ValueError, RuntimeWarning, TypeError):
                penalty = constants.MAX_EVAL_FUN


            #compute updated constraint_weight
            if penalty < constants.DELTA:
                constraint_gen_not_met = 0
                constraint_gen_met = constraint_gen_met + 1
                if constraint_gen_met == constants.NF:
                    penalty_weight = 1 / constants.BETA2 * penalty_weight
                    constraint_gen_met = 0

                    #revaluate population
                    for ind in range(constants.POPULATION_SIZE):
                        new_parent_fitness[ind] = evaluation.eval_function(new_equations[ind], penalty_weight)
            else:
                constraint_gen_met = 0
                constraint_gen_not_met = constraint_gen_not_met + 1
                if constraint_gen_not_met == constants.NF:
                    penalty_weight = constants.BETA1 * penalty_weight
                    constraint_gen_not_met = 0

                    # revaluate population
                    for ind in range(constants.POPULATION_SIZE):
                        new_parent_fitness[ind] = evaluation.eval_function(new_equations[ind], penalty_weight)

            # compute the min distance and mean distance
            min_fitness.append(min(new_parent_fitness))
            mean_fitness.append(np.mean(new_parent_fitness))
            std_fitness.append(np.std(new_parent_fitness))

            # compute termination condition if best individual does not change for a number of generations
            if min(new_parent_fitness) == min(parent_fitness):
                # check convergence
                termination_generation = termination_generation + 1
                if termination_generation == constants.END_CONDITION:
                    index_best_ind = list(new_parent_fitness).index(min(new_parent_fitness))
                    solution.append(new_equations[index_best_ind])
                    print(new_equations[index_best_ind])
                    break

                if min(new_parent_fitness) < constants.DELTA:
                    total_executions.append(number_generations * constants.POPULATION_SIZE)
                    success_rate = success_rate + 1
                    index_best_ind = list(new_parent_fitness).index(min(new_parent_fitness))
                    solution.append(new_equations[index_best_ind])
                    print(new_equations[index_best_ind])
                    break

            elif number_generations == constants.N_GENERATIONS -1:
                index_best_ind = list(new_parent_fitness).index(min(new_parent_fitness))
                solution.append(new_equations[index_best_ind])
                print(new_equations[index_best_ind])
                break

            else:
                termination_generation = 0

            # create next generation
            number_generations = number_generations + 1
            parent_vector = new_parent_vector
            parent_fitness = new_parent_fitness

        # save values for statistical analysis
        all_min_fitness.append(min_fitness)
        all_mean_fitness.append(mean_fitness)
        all_std_fitness.append(std_fitness)

    # print statistics and plots
    statistics_plots.statistics(all_min_fitness, total_executions, success_rate, pex)
    statistics_plots.graphics(all_min_fitness, all_mean_fitness, all_std_fitness)
    statistics_plots.representation(solution[0])

if __name__ == "__main__":
    main()



