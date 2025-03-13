from PIL.ImageChops import constant

import constants
import numpy as np


def function(x):
    """
    function to be integrated
    :param x: independent variable
    :return: function value
    """
    fun = 1/4*(3*x**2 - 2*x + 1)

    return fun

def eval_function(x):
    """
    evaluation function
    :param x: independent variable
    :return: function value
    """


    fun_eval = 0
    for i in range((constants.X_RIGHT - constants.X_LEFT) * constants.N):

        x = constants.X_LEFT + i


        fun_eval = 1 / (constants.N + 1) * (fun_eval + )

    return fun_eval