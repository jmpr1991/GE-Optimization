import constants
import numpy as np


def function(x):
    """
    function to be integrated
    :param x: independent variable
    :return: function value
    """

    fun = np.nan
    if constants.FUN_OPTION == 1:
        fun = 1/4*(3*x**2 - 2*x + 1)
    elif constants.FUN_OPTION == 2:
        fun = np.log(1 + x) + x / (1 + x)
    elif constants.FUN_OPTION == 3:
        fun = np.exp(x) * (np.sin(x) + np.cos(x))

    return fun

def eval_function(integral):
    """
    evaluation function
    :param integral: string with potential integral function whihc has to be evaluated
    :return: function value
    """

    # if the element is incomplete after wrapping process return the maximum fitness value
    if integral is None:
        return constants.MAX_EVAL_FUN

    sum = 0
    for i in range((constants.X_RIGHT - constants.X_LEFT) * constants.N):

        x = constants.X_LEFT + i + constants.h
        F1 = eval(integral)

        x = constants.X_LEFT + i
        F2 = eval(integral)

        F_prim = (F1 - F2) / constants.h

        if np.abs(F_prim - function(x)) <= constants.U:
            sum = sum + constants.K0 * np.abs(F_prim - function(x))
        else:
            sum = sum + constants.K1 * np.abs(F_prim - function(x))

    fun_eval = 1 / (constants.N + 1) * sum

    return fun_eval




