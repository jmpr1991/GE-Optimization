import constants
import decoder
import evaluation
import initialization
import parent_selection
import crossover
import mutation
import survival_elitism
import statistics_plots

import sys, copy, re, random, math, operator
import numpy as np


def main():

    np.random.seed(2)  # seed of the random function to avoid errors in the vector generator

    # Read grammar
    bnf_grammar = decoder.Grammar("arithmetic.pybnf")

    # initialize variables for statistical analysis
    all_parent_vectors = np.zeros((constants.N_EXECUTIONS, constants.POPULATION_SIZE, constants.N_CODONS))
    all_parent_distances = np.zeros((constants.N_EXECUTIONS, constants.POPULATION_SIZE))
    all_min_distances = []
    all_mean_distances = []
    all_std_distances = []
    total_generations = []

    # initialize success rate and success mean evaluations number (pex) parameters
    success_rate = 0
    pex = []

    for execution_i in range(constants.N_EXECUTIONS):
        print("execution {}".format(execution_i+1), "on going")

        # initialize the population
        parent_vector = initialization.initialization_function()

        parent_fitness = np.zeros(constants.POPULATION_SIZE)
        for ind in range(len(parent_vector)):
            output, _ = bnf_grammar.generate(parent_vector[ind])
            parent_fitness[ind] = evaluation.eval_function(output)

        # initialize variables
        min_distance = []
        mean_distance = []
        std_distance = []
        number_generations = 0
        termination_generation = 0

        # generation evolution loop
        while number_generations < constants.n_generations:

            # parent selection
            parent_sel_vector, parent_sel_fitness = parent_selection.parent_selection_function(parent_vector, parent_fitness)

            # crossover
            child_vector, child_fitness = crossover.crossover_function(parent_sel_vector, parent_sel_fitness, constants.N_CODONS)

            # mutation
            child_mutated_vector, child_mutated_fitness = mutation.mutation_function(child_vector, child_fitness, constants.N_CODONS)

            # survival selections and elitism
            new_parent_vector, new_parent_fitness = survival_elitism.survival_elitism_function(child_mutated_vector, child_mutated_fitness, parent_vector, parent_fitness)

            # compute the min distance and mean distance
            min_distance.append(min(new_parent_fitness))
            mean_distance.append(np.mean(new_parent_fitness))
            std_distance.append(np.std(new_parent_fitness))

            # compute termination condition if best individual does not change for a number of generations
            if min(new_parent_fitness) == min(parent_fitness):
                # check convergence
                termination_generation = termination_generation + 1
                if termination_generation == constants.end_condition:
                    total_generations.append(number_generations)
                    parent_vector = new_parent_vector
                    parent_fitness = new_parent_fitness
                    break

                #check if the optimum distance has been achieved (only for the square shaped cities)
                if constants.square_cities:
                    if min(new_parent_fitness) <= constants.square_size * 4 + constants.delta:
                        total_generations.append(number_generations)
                        parent_vector = new_parent_vector
                        parent_fitness = new_parent_fitness
                        break
            else:
                termination_generation = 0

            # create next generation
            number_generations = number_generations + 1
            parent_vector = new_parent_vector
            parent_fitness = new_parent_fitness

        # save values for statistical analysis
        all_parent_vectors[execution_i,:,:,:] = parent_vector
        all_parent_distances[execution_i, :] = parent_fitness
        all_min_distances.append(min_distance)
        all_mean_distances.append(mean_distance)
        all_std_distances.append(std_distance)

        # compute success rate if square shaped city
        if constants.square_cities:
            if all_min_distances[execution_i][-1] <= 4 * constants.square_size + constants.delta:
                success_rate = success_rate + 1
                pex.append(number_generations)

    # print statistics and plots
    statistics_plots.statistics(all_min_distances, total_generations, success_rate, pex)
    statistics_plots.graphics(all_min_distances, all_mean_distances, all_std_distances, all_parent_vectors, all_parent_distances)


if __name__ == "__main__":
    main()



