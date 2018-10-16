################################################################################
# thegame.construction.fromrandomness.py                                       #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@insight-centre.org                              #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module contains the classes to build random mass functions.             #
# ---------------------------------------------------------------------------- #
# Main classes:                                                                #
#   - RandomDiscreteMassFunctionsGenerator: A generator of random mass         #
#     functions.                                                               #
################################################################################

import thegame.element as element
import thegame.massfunction as massfunction

import random

class RandomDiscreteMassFunctionsGenerator:
    """
    A generator of random discrete mass functions. You can customise the
    size of the frame of discernment and the number of focals you would like.

    Attributes:
        self.cache: If the elements should be cached or not (this can greatly
            accelerates the speed of generation but it might also take too much
            memory or be simply impossible to store (2^10000 elements should not
            be cached for instance!)).
        self.nb_states: The number of states in the frame of discernment.
        self.__cache: The cache containing all the elements in the powerset.
        self.__max: The maximum value for the elements which is also the max number
            of focal elements that can be requested.
    """

    def __init__(self, nb_states, cache=True):
        """
        Constructor of the generator. If cache is set to True, then all the possible
        elements are stored within the cache. This might saturate your memory if you
        ask for too many states.

        Args:
            nb_states (int): The number of states in the frame of discernment.
            cache (bool): If the elements should be cached or not.
        Raises:
            ValueError: If the number of states given is null or negative.
        """
        if nb_states <= 0:
            raise ValueError(
                "nb_states: " + str(nb_states) + "\n" +
                "The number of states in your frame of discernment cannot " +
                "be null or negative!"
            )
        
        self.cache = cache
        self.nb_states = nb_states
        self.__cache = []
        self.__max = 2**nb_states

        if self.cache:
            for e in element.DiscreteElement.iterator_powerset(nb_states):
                self.__cache.append(e)


    def build_evidence(self, nb_focals):
        """
        Builds a random mass function with the given number of focal elements.

        Args:
            nb_focals (int): The number of focal elements for the random mass function.
        Returns:
            MassFunction -- A new random discrete mass function.
        Raises:
            ValueError: if the number of focal elements requested does not make sense.
        """
        if not 0 < nb_focals <= self.__max:
            raise ValueError(
                "nb_focals: " + str(nb_focals) + "\n" +
                "The number of focals cannot exceed the number of possible " +
                "different elements in your frame of discernment. It also can't be " +
                "null or negative."
            )
        
        if self.cache:
            elements = random.sample(self.__cache, nb_focals)
        else:
            elements = []
            for i in range(nb_focals):
                e = element.DiscreteElement(self.nb_states, random.randint(0, self.__max - 1))
                while e in elements:
                    e = element.DiscreteElement(self.nb_states, random.randint(0, self.__max - 1))
                elements.append(e)

        numbers = range(100)
        values = [random.choice(numbers) for _ in range(nb_focals)]
        focals = [(focal, value) for focal, value in zip(elements, values)]

        result = massfunction.MassFunction(*focals)
        result.normalise()
        return result


