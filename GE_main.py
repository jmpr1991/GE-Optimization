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


def main():

    np.random.seed(2)  # seed of the random function to avoid errors in the vector generator

    # Read grammar
    bnf_grammar = decoder.Grammar("arithmetic.pybnf")

    # initialize variables for statistical analysis
    all_min_fitness = []
    all_mean_fitness = []
    all_std_fitness = []
    total_generations = []

    # initialize success rate and success mean evaluations number (pex) parameters
    success_rate = 0
    pex = []

    for execution_i in range(constants.N_EXECUTIONS):
        print("execution {}".format(execution_i+1), "on going")

        # initialize the population
        parent_vector, parent_fitness = initialization.initialization_function(bnf_grammar)

        # initialize variables
        min_fitness = []
        mean_fitness = []
        std_fitness = []
        number_generations = 0
        termination_generation = 0

        # generation evolution loop
        while number_generations < constants.N_GENERATIONS:

            # parent selection
            parent_sel_vector = parent_selection.parent_selection_function(parent_vector, parent_fitness)

            # crossover
            child_vector = crossover.crossover_function(parent_sel_vector)

            # mutation
            child_mutated_vector = mutation.mutation_function(child_vector)
            child_mutated_fitness = np.zeros(constants.POPULATION_SIZE)
            for ind in range(len(parent_vector)):
                output, _ = bnf_grammar.generate(child_mutated_vector[ind])
                child_mutated_fitness[ind] = evaluation.eval_function(output)

            # survival selections and elitism
            new_parent_vector, new_parent_fitness = survival_elitism.survival_elitism_function(child_mutated_vector,
                                                                                               child_mutated_fitness,
                                                                                               parent_vector,
                                                                                               parent_fitness,
                                                                                               bnf_grammar)

            # compute the min distance and mean distance
            min_fitness.append(min(new_parent_fitness))
            mean_fitness.append(np.mean(new_parent_fitness))
            std_fitness.append(np.std(new_parent_fitness))

            # compute termination condition if best individual does not change for a number of generations
            if min(new_parent_fitness) == min(parent_fitness):
                # check convergence
                termination_generation = termination_generation + 1
                if termination_generation == constants.END_CONDITION:
                    total_generations.append(number_generations)

                    index_best_ind = list(new_parent_fitness).index(min(new_parent_fitness))
                    solution, _ = bnf_grammar.generate(child_mutated_vector[index_best_ind])
                    print(solution)
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
    statistics_plots.statistics(all_min_fitness, total_generations, success_rate, pex)
    statistics_plots.graphics(all_min_fitness, all_mean_fitness, all_std_fitness)


if __name__ == "__main__":
    main()



