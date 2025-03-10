"""
This file contain the constants of the tsp problem
"""

import numpy as np

#  randon_vector_generator constants
random_cities = False # random shaped city
square_cities = True # square shaped city
n_executions = 1  #number of executions
n_cities = 30  #number of cities
dimension = 2      # space dimension (do not change this value)
square_size = 1  # size of square in where the vectors are located
np.random.seed(2) #seed of the random function to avoid errors in the vector generator

# Initialization
n_permutations = 10 # population size (select an even number of permutations to avoid errors)

# parent selection
n_tournaments = n_permutations  # number of tournaments, lambda in the literature
n_individuals = 2  # number of individuals participating in the tournament (do not change this value)

# crossover
pc = 1 # crossover probability

# mutation
pm = 1 # probability of mutation

# termination condition
n_generations = 20000 #number of generations
end_condition = 1000 # max number of generations without improvement

# Success rate
delta = 0.01