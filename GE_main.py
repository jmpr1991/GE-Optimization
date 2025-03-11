import constants
import decoder
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
    all_parent_vectors = np.zeros((constants.n_executions, constants.population_size, constants.n_codons))
    all_parent_distances = np.zeros((constants.n_executions, constants.population_size))
    all_min_distances = []
    all_mean_distances = []
    all_std_distances = []
    total_generations = []

    # initialize success rate and success mean evaluations number (pex) parameters
    success_rate = 0
    pex = []

    for execution_i in range(constants.n_executions):
        print("execution {}".format(execution_i+1), "on going")

        # initialize the population
        parent_vector = initialization.initialization_function()

        output = []
        for ind in range(len(parent_vector)):
            output[ind], _ = bnf_grammar.generate(parent_vector[ind])

        # initialize variables
        min_distance = []
        mean_distance = []
        std_distance = []
        number_generations = 0
        termination_generation = 0

        # generation evolution loop
        while number_generations < constants.n_generations:

            # parent selection
            parent_sel_vector, parent_sel_distance = parent_selection.parent_selection_function(parent_vector, parent_distance, constants.n_codons)

            # crossover
            child_vector, child_distance = crossover.crossover_function(parent_sel_vector, parent_sel_distance, constants.n_codons)

            # mutation
            child_mutated_vector, child_mutated_distance = mutation.mutation_function(child_vector, child_distance, constants.n_codons)

            # survival selections and elitism
            new_parent_vector, new_parent_distance = survival_elitism.survival_elitism_function(child_mutated_vector, child_mutated_distance, parent_vector, parent_distance)

            # compute the min distance and mean distance
            min_distance.append(min(new_parent_distance))
            mean_distance.append(np.mean(new_parent_distance))
            std_distance.append(np.std(new_parent_distance))

            # compute termination condition if best individual does not change for a number of generations
            if min(new_parent_distance) == min(parent_distance):
                # check convergence
                termination_generation = termination_generation + 1
                if termination_generation == constants.end_condition:
                    total_generations.append(number_generations)
                    parent_vector = new_parent_vector
                    parent_distance = new_parent_distance
                    break

                #check if the optimum distance has been achieved (only for the square shaped cities)
                if constants.square_cities:
                    if min(new_parent_distance) <= constants.square_size * 4 + constants.delta:
                        total_generations.append(number_generations)
                        parent_vector = new_parent_vector
                        parent_distance = new_parent_distance
                        break
            else:
                termination_generation = 0

            # create next generation
            number_generations = number_generations + 1
            parent_vector = new_parent_vector
            parent_distance = new_parent_distance

        # save values for statistical analysis
        all_parent_vectors[execution_i,:,:,:] = parent_vector
        all_parent_distances[execution_i, :] = parent_distance
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



