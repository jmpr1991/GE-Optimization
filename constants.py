"""
This file contain the constants of the tsp problem
"""

#  randon_vector_generator constants
CODON_BITS = 8 #number of bits of the codons
N_EXECUTIONS = 1  #number of executions
N_CODONS = 10  #number of cities

MAX_WRAPS = 10

# evaluation function constants
MAX_EVAL_FUN = 1e6
FUN_OPTION = 1
X_LEFT = -2
X_RIGHT = 2
U = 0.1
K0 = 1
K1 = 10
N = 10 # subintervals in 1 unit
h = 1e-5 # derivation constant

# Initialization
POPULATION_SIZE = 16 # population size (select an even number of permutations to avoid errors)

# parent selection
N_TOURNAMENTS = POPULATION_SIZE  # number of tournaments, lambda in the literature
N_INDIVIDUALS = 2  # number of individuals participating in the tournament (do not change this value)

# crossover
PC = 1 # crossover probability

# mutation
PM = 0.1 # probability of mutation

# termination condition
N_GENERATIONS = 20000 #number of generations
END_CONDITION = 1000 # max number of generations without improvement

# Success rate
delta = 0.01