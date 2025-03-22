import constants
import numpy as np
import math

import warnings


def function(x):
    """
    function to be integrated
    :param x: independent variable
    :return: function value
    """

    fun = np.nan
    if constants.FUN_OPTION == 1:
        fun = 1/4 * (3*x**2 - 2*x + 1)
    elif constants.FUN_OPTION == 2:
        fun = math.log(1 + x) + x / (1 + x)
    elif constants.FUN_OPTION == 3:
        fun = math.exp(x) * (math.sin(x) + math.cos(x))

    return fun


def eval_function(integral, penalty_weight=0):
    """
    evaluation function
    :param integral: string with potential integral function which has to be evaluated
    :return: fitness value
    """
    warnings.simplefilter('error')

    # if the element is incomplete after wrapping process return the maximum fitness value
    if integral is None:
        return constants.MAX_EVAL_FUN

    n_points = (constants.X_RIGHT - constants.X_LEFT) * constants.N
    vector = np.linspace(constants.X_LEFT, constants.X_RIGHT, n_points)
    sum = 0

    # compute first derivative of the potential solution
    for i in range(n_points):

        x = vector[i] + constants.h
        try:
            F1 = eval(integral)

        # if error sum=nan
        except (ZeroDivisionError, OverflowError, ValueError, RuntimeWarning, TypeError):
            sum = np.nan
            break

        x = vector[i]
        try:
            F2 = eval(integral)

        # if error sum=nan
        except (ZeroDivisionError, OverflowError, ValueError, RuntimeWarning, TypeError):
            sum = np.nan
            break

        # if constant function. break and return nan to repeat iteration
        if F1 == F2:
            sum = np.nan
            break

        F_prim = (F1 - F2) / constants.h

        # compute fitness
        if abs(F_prim - function(x)) <= constants.U:
            sum = sum + constants.K0 * abs(F_prim - function(x))
        else:
            sum = sum + constants.K1 * abs(F_prim - function(x))

    # invalid function
    if sum is np.nan:
        fun_eval = constants.MAX_EVAL_FUN
    #valid function
    else:
        #compute penalty
        x = constants.X_CONSTRAINT
        try:
            penalty = abs(eval(integral) - constants.F0)
        # if error sum=nan
        except (ZeroDivisionError, OverflowError, ValueError, RuntimeWarning, TypeError):
            fun_eval = constants.MAX_EVAL_FUN
            return fun_eval

        #compute fitness considering the penalty
        fun_eval = 1 / (n_points + 1) * sum + penalty_weight * penalty

    return fun_eval

def integral_function(x):
    """
    integral function
    :param x: independent variable
    :return: function value
    """

    F = np.nan
    if constants.FUN_OPTION == 1:
        F = 1/4 * (x**2 + 1) * (x - 1)
    elif constants.FUN_OPTION == 2:
        F = x * math.log(1 + x)
    elif constants.FUN_OPTION == 3:
        F = math.exp(x) * math.sin(x)

    return F


