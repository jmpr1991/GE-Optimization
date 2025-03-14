import numpy as np
import matplotlib.pyplot as plt

import constants

def statistics(distances_vector, generation_vector, success_rate, pex):
    """
    This function print the statistics of the genetic algorithm
    :param distances_vector: vector compiling the last generation distances of each execution
    :param generation_vector: vector compiling the number of generations of each execution
    :param success_rate: number of successful executions
    :param pex: number of generations to succeed
    """
    # Success rate computation
    print("\n Statistics:")

    # VAMM computation
    vam = np.zeros(constants.N_EXECUTIONS)
    for i in range(constants.N_EXECUTIONS):
        vam[i] = float(min(np.array(distances_vector[i])))

    vamm = sum(vam) / constants.N_EXECUTIONS
    vamm_std = np.std(vam)
    print('VAMM = ', vamm, '+/-', vamm_std)
    print('Execution mean number to converge = ', np.mean(generation_vector), '+/-', np.std(generation_vector))

def graphics(min_distance_vector, mean_distance_vector, std_distance_vector):
    """
    This function creates  the progress curve of the first execution of the algorithm
    :param min_distance_vector: vector compiling the min distance of the population of each generation
    :param mean_distance_vector: vector compiling the mean distance of the population of each generation
    :param std_distance_vector: vector compiling the standard deviation of the distances of each generation
    :param last_parent_vector: solution vector
    """

    # print the convergence of the best individual
    plt.plot(np.array(min_distance_vector[0]), linewidth=0.6)
    plt.plot(np.array(mean_distance_vector[0]), linewidth=0.6, color='darkred')
    plt.errorbar(y=np.array(mean_distance_vector[0]), x=[i for i in range(len(np.array(mean_distance_vector[0])))],
                 yerr=np.array(std_distance_vector[0]), errorevery=int(len(np.array(mean_distance_vector[0]))/10),
                 fmt='none', elinewidth=0.3, ecolor='darkred',capsize=5, ls='-.', label='error bar')
    plt.title('{} individuals progress curve '
              '\n Best individual and population mean for each generation'.format(constants.N_CODONS))
    plt.xlabel('Generation')
    plt.ylabel('Adaptation function (distance)')
    plt.legend(['best individual', 'population mean', 'error band'])
    plt.show()