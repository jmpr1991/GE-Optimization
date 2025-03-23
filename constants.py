"""
This file contain the constants of the problem
"""

#  randon_vector_generator constants
CODON_BITS = 8 #number of bits of the codons
N_EXECUTIONS = 1  #number of executions
N_CODONS = 16  #number of codons
MAX_WRAPS = 10

# evaluation function constants
MAX_EVAL_FUN = 50
FUN_OPTION = 2
X_CONSTRAINT = 0
F0 = 0
X_LEFT = 0
X_RIGHT = 5
U = 0.1
K0 = 1
K1 = 10
N = 10 # subintervals in 1 unit
h = 1e-5 # derivation constant

# restrictions
PENALTY = True
INITIAL_PENALTY = 3e-3
NF = 4
BETA1 = 4
BETA2 = 2.8

# local search
LOCAL_SEARCH = False
CODON_CONSTRAINT = 8
N_CODONS_2_USE = CODON_CONSTRAINT

# crossover and mutation
ADAPTATIVE_VARIATION = True
PC_K1 = 1.0
PM_K2 = 0.5
PC_K3 = 1.0
PM_K4 = 0.5

PC = 0.9 # crossover probability
PM = 0.2 # probability of mutation

# Initialization
POPULATION_SIZE = 100 # population size (select an even number of permutations to avoid errors)

# parent selection
N_TOURNAMENTS = POPULATION_SIZE  # number of tournaments, lambda in the literature
N_INDIVIDUALS = 2  # number of individuals participating in the tournament (do not change this value)

# termination condition
N_GENERATIONS = 2000 #number of generations
END_CONDITION = 50 # max number of generations without improvement
DELTA = 0.2