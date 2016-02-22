################################################################################
# thegame.massfunction.py                                                      #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@cit.ie                                          #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module contains all the classes to work with belief functions. It uses  #
# as focal elements, the elements implemented in element.py. Implementing new  #
# mass function types working on different types of elements should be minimal.#
# ---------------------------------------------------------------------------- #
# Main classes:                                                                #
#   - MassFunction: A class providing all the usual operations on mass func-   #
#     tions, from combination rules to decision making methods and characteri- #
#     sations (specificity, discrepancy, etc).                                 #
################################################################################

from enum import Enum

import math
import copy
import functools
import operator
import itertools

import thegame.element as element

##############
# DECORATORS #
##############

def check_focal_elements_validity(function):
    """
    Decorator that checks that all the given focal elements provided to 'function'
    can be accessed via indices and contains an ``element.Element`` at index 0 and
    a numerical value at index 1.

    Args:
        function (func.): A mass function method that takes focal elements as
            arguments.
    Returns:
        function result -- The result of the provided function.
    Raises:
        ValueError: If the provided focal elements are not formatted as requested.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        for i in range(len(args)-1):
            try:
                #if (not isinstance(args[i+1][0], element.Element) or
                if  not (isinstance(args[i+1][1], int) or isinstance(args[i+1][1], float)):
                    raise ValueError(
                        "focal_element: " + str(args[i+1]) + "\n" +
                        "It should have contained an Element at index 0 and a numerical " +
                        "value at index 1 (e.g. a tuple (element, 0.8) or a list [element, 0.5] " +
                        "would have been valid)."
                    )
            except TypeError:
                raise ValueError(
                    "focal_element: " + str(args[i+1]) + "\n" +
                    "It should have supported indexing and contained an Element at index 0 and "
                    "a numerical value at index 1 (e.g. a tuple (element, 0.8) or a list " +
                    "[element, 0.5] would have been valid)."
                )
        return function(*args)
    return wrapped_function
            

def check_focal_elements_compatibility(function):
    """
    Decorator that checks that all the elements provided to 'function' are
    compatible with each others.

    Args:
        function (func.): A mass function method that takes focal elements as
            arguments.
    Returns:
        function result -- The result of the provided function.
    Raises:
        IncompatibleElementsInAMassFunctionError: If the elements provided to the
        decorated function are not compatible with each others.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        for i in range(len(args)-1):
            for j in range(len(args)-1):
                if not args[i+1][0].is_compatible(args[j+1][0]):
                    raise IncompatibleElementsInAMassFunctionError(args[i+1][0], args[j+1][0])
        return function(*args)
    return wrapped_function


def check_focal_elements_compatibility_with_mass_function(function):
    """
    Decorator that checks that all the focal elements provided to a
    mass function method are compatible with the elements already present
    in the mass function.

    Remark: It does not check if the provided focal elements are compatible
    with each others. Use ``@check_focal_elements_compatiblity``for that.

    Args:
        function (func.): A mass function method that takes focal elements as
            arguments.
    Returns:
        function result -- The result of the provided function.
    Raises:
        IncompatibleElementsInAMassFunctionError: If the elements provided to the
        decorated function are not compatible with the mass function.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        for i in range(len(args)-1):
            for element in args[0].focals:
                if not element.is_compatible(args[i+1][0]):
                    raise IncompatibleElementsInAMassFunctionError(element, args[i+1][0])
        return function(*args)
    return wrapped_function


def check_mass_function_is_not_empty(function):
    """
    Decorator that checks that the first argument (which should be a mass function)
    is not empty.

    Args:
        function (func.): A mass function method that takes a mass function
            as a first argument.
    Returns:
        function result -- The result of the provided function.
    Raises:
        EmptyMassFunctionError: If the mass function provided as first argument
        is empty.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        if args[0].is_empty():
            raise EmptyMassFunctionError()
        return function(*args)
    return wrapped_function


def check_mass_function_are_not_empty(function):
    """
    Decorator that checks that the mass functions passed as arguments to
    the provided function are not empty.

    Args:
        function (func.): A mass function method that takes mass functions
            as arguments.
    Returns:
        function result -- The result of the provided function.
    Raises:
        EmptyMassFunctionError: If at least one mass function is empty.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        for arg in args:
            if arg.is_empty():
                raise EmptyMassFunctionError()
        return function(*args)
    return wrapped_function


def check_mass_functions_compatibility(function):
    """
    Decorator that checks that all the mass functions given as arguments are
    compatible with each others.

    Args:
        function (func.): A method taking only mass functions as arguments.
    Returns:
        function result -- The result of the provided function.
    Raises:
        IncompatibleMassFunctionsError: If at least two mass functions are
        incompatible with each others.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        for i in range(len(args)):
            for j in range(len(args)):
                if i != j and not args[i].is_compatible(args[j]):
                    raise IncompatibleMassFunctionsError(args[i], args[j])
        return function(*args)
    return wrapped_function


def check_arguments_are_mass_functions(function):
    """
    Decorator that checks that there is at least one parameter provided and that
    the ones provided are MassFunctions.

    Args:
        function (func.): A method taking only mass functions as arguments.
    Returns:
        function result -- The result of the provided function.
    Raises:
        TypeError: If there is not enough parameters or if at least one of them
        is not of the proper type.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        if len(args) < 2:
            raise TypeError(
                "Not enough mass functions provided, it should receive at least one!"
            )
        for i in range(len(args)):
            if not isinstance(args[i], MassFunction):
                raise TypeError(
                    "This method accept only mass functions as arguments!"
                )
        return function(*args)
    return wrapped_function


################################################################################
################################################################################
################################################################################


##############
# EXCEPTIONS #
##############

class MassFunctionError(Exception):
    """Raised when an error occurs in this module."""
    pass


class IncompatibleElementsInAMassFunctionError(MassFunctionError):
    """
    Raised when a mass function is tried to be built with incompatible elements.

    Attributes:
        e1: The first element of the incompatibility.
        e2: The second element of the incompatibility.
    """
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return (
            "A mass function cannot contain incompatible elements.\n" +
            " - First element : " + str(self.e1) + "\n" +
            " - Second element: " + str(self.e2)
        )


class IncompatibleMassFunctionsError(MassFunctionError):
    """
    Raised when an operation on mass function is attempted on two or
    more incompatible mass functions.

    Attributes:
        m1: The first mass function of the incompatibility.
        m2: The second mass function of the incompatibility.
    """
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

    def __str__(self):
        return (
            "An operation on two incompatible mass functions has been attempted:\n" +
            " - First mass function : " + str(self.m1) + "\n" +
            " - Second mass function: " + str(self.m2)
        )


class EmptyMassFunctionError(MassFunctionError):
    """
    Raised when a method requiring focal elements is called on an empty
    mass function.
    """
    def __init__(self):
        pass

    def __str__(self):
        return "Certain methods cannot be called on an empty mass function!"
    

class DuplicateElementError(MassFunctionError):
    """
    Raised when a mass function is tried to be constructed from a set of elements
    containing duplicates.
    """

    def __init__(self):
        pass

    def __str__(self):
        return ("The given set of elements given to construct a mass function " +
               "contains duplicates!")


################################################################################
################################################################################
################################################################################



#########################
# GENERIC MASS FUNCTION #
#########################

class MassFunction():
    """
    A generic class for mass functions. All the operations that
    can be implemented in without knowing the real type of elements
    it uses are implemented. It thus make it as generic as possible,
    not really considering the elements themselves.

    Remark 0: This object is iterable and can thus be used within
        for statements; it thus provides elements.
    Remark 1: It also provides an ``items()`` method iterating over
        (element, mass) then.
    Remark 2: It also acts like a dictionary, providing a way to set
        and get items with elements as keys. 

    Attributes:
        self.focals: A dictionary with elements as keys and masses
            as values. Should not be used as it is interfaced directly
            through method overrides.
    """

    """
    The precision required for the masses. Everything under should be
    cleaned up. This prevents artifact masses to stay within mass
    functions (saves computation time and readability).
    """
    precision = 0.000001

    class Combination(Enum):
        """
        The enumeration of the combination rules implemented
        in this library.
        """

        """The classic Dempster's rule of combination."""
        Dempster    = 1
        """The unnormlised Dempster's rule, also called conjunctive.
        For a definition, refer to "P. Smets: The transferable belief
        model, 1994"."""
        Smets       = 2
        """The disjunctive rule of combination. "P. Smets, Belief functions:
        The disjunctive rule of combination and the generalized bayesian
        theorem, 1993"."""
        Disjunctive = 3
        """The Yager's rule of combination, the conflict is put on the
        whole set. For a definition, refer to "R. Yager: On the Dempster-Shafer
        framework and new combination rules, 1987"."""
        Yager       = 4
        """The Dubois & Prade's combination rule performing the normal
        conjunctive combination when there is no conflict between elements
        and putting the conflict result on the union of conflicting elements.
        For a definition, refer to "D. Dubois and H. Prade: Representation and
        Combination of Uncertainty with Belief Functions and Possibility
        Measures, 1988"."""
        DuboisPrade = 5
        """The simple average combination rule."""
        Average     = 6
        """The Murphy's combination rule, consisting of an average and X-1
        Dempster's rule of the result with itself where X is the number of
        mass functions that were combined within the average. For a definition,
        refer to "C. K. Murphy: Combining belief functions when evidence
        conflicts, 2000"."""
        Murphy      = 7
        """The Chen's combination rule based on distance between the mass
        functions. For a definition, refer to "L.-Z. Chen: A new fusion approach
        based on distance of evidences, 2005"."""
        Chen        = 8

    # *************
    # Constructors:
    # *************

    @check_focal_elements_validity
    @check_focal_elements_compatibility
    def __init__(self, *focal_elements):
        """
        Constructs a mass function given a list of focal elements.
        They should be provided as something accepting index operations
        with an ``element.Element`` at index 0 and the value at index 1 (e.g.
        tuples (DiscreteElement(3, 1), 1) or lists [DiscreteElement(2, 1), 0.5]).

        Remark: It doesn't have to form a valid mass function. If you
        want to check that, use ``check_sum(self)``.

        Warning: This can be rather slow for huge number of focal elements.
        If this is too slow, use MassFunction.factory_constructor_unsafe(*focals)
        instead.

        Args:
            *focal_elements (*Element): A list of focal elements to initialise
                the mass function with.
        Raises:
            ValueError: If the provided focal elements are not formatted as requested.
            IncompatibleElementsInAMassFunctionError: If the elements provided to the
                decorated function are not compatible with each others.
            DuplicateElementsError: If the same element is given multiple times.
        """
        #Check for duplicates:
        l = [focal[0] for focal in focal_elements]
        if len(list(set(l))) == len(l): # Duplicates <=> len(set) < list
            self.focals = {}
            for focal in focal_elements:
                 self.focals[focal[0]] = focal[1]
        else:
            raise DuplicateElementError()

    ################################################################################
            
    @classmethod
    def factory_constructor_unsafe(cls, *focal_elements):
        """
        Constructs a mass function given a list of focal elements.
        They should be provided as something accepting index operations
        with an ``element.Element`` at index 0 and the value at index 1 (e.g.
        tuples (DiscreteElement(3, 1), 1) or lists [DiscreteElement(2, 1), 0.5]).

        Remark 0: It doesn't have to form a valid mass function. If you
            want to check that, use ``check_sum(self)``.
        Remark 1: This does not check that the given elements are compatible.

        Args:
            *focal_elements (*Element): A list of focal elements to initialise
                the mass function with.
        """
        result = cls()
        for focal in focal_elements:
            result[focal[0]] = focal[1]
        return result

    ################################################################################
    ################################################################################
    ################################################################################

    # **********************************************
    # Utility methods that modify the mass function:
    # **********************************************

    @check_focal_elements_validity
    @check_focal_elements_compatibility
    @check_focal_elements_compatibility_with_mass_function
    def add_mass(self, *focal_elements):
        """
        Adds mass to the current mass function given the focal elements
        provided. They should be provided as something accepting index operations
        with an ``element.Element`` at index 0 and the value at index 1 (e.g.
        tuples (DiscreteElement(3, 1), 1) or lists [DiscreteElement(2, 1), 0.5]).

        Remark 0: If an element was already present, it adds the given mass
            to the current one.
        Remark 1: This does not care about the validity of the resulting mass
            function.
        Remark 2: It does modify the current mass function.
        Remark 3: It is possible to add negative masses, that's your problem.

        Args:
            *focal_elements (*(Element, float)): A list of focal elements to add to the
                mass function.
        Raises:
            ValueError: If the provided focal elements are not formatted as requested.
            IncompatibleElementsInAMassFunctionError: If the elements provided to the
                decorated function are not compatible with each others or if they are
                not compatible with the elements already present in the mass function.
        """
        for focal in focal_elements:
            if focal[0] not in self.focals:
                self.focals[focal[0]] = focal[1]
            else:
                self.focals[focal[0]] += focal[1]

    ################################################################################

    def add_mass_unsafe(self, *focal_elements):
        """
        Adds mass to the current mass function given the focal elements
        provided. They should be provided as something accepting index operations
        with an ``element.Element`` at index 0 and the value at index 1 (e.g.
        tuples (DiscreteElement(3, 1), 1) or lists [DiscreteElement(2, 1), 0.5]).

        Remark 0: If an element was already present, it adds the given mass
            to the current one.
        Remark 1: This does not care about the validity of the resulting mass
            function.
        Remark 2: It does modify the current mass function.
        Remark 3: It is possible to add negative masses, that's your problem.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            *focal_elements (*(Element, float)): A list of focal elements to add to the
                mass function.
        """
        for focal in focal_elements:
            if focal[0] not in self.focals:
                self.focals[focal[0]] = focal[1]
            else:
                self.focals[focal[0]] += focal[1]

    ################################################################################

    @check_focal_elements_validity
    @check_focal_elements_compatibility
    @check_focal_elements_compatibility_with_mass_function
    def remove_mass(self, *focal_elements):
        """
        Removes mass to the current mass function given the focal elements provided.
        They should be provided as something accepting index operations
        with an ``element.Element`` at index 0 and the value at index 1 (e.g.
        tuples (DiscreteElement(3, 1), 1) or lists [DiscreteElement(2, 1), 0.5]).

        Remark 0: If an element wasn't present in the mass function, it removes the
            mass anyway.
        Remark 1: This does not care about the validity of the resulting mass function.
        Remark 2: It does modify the current mass function.
        Remark 3: It is possible to remove negative masses (thus adding mass), that's
            your problem.

        Args:
            *focal_elements (*(Element, float)): A list of focal elements to remove 
                from the mass function.
        Raises:
            ValueError: If the provided focal elements are not formatted as requested.
            IncompatibleElementsInAMassFunctionError: If the elements provided to the
                decorated function are not compatible with each others or if they are
                not compatible with the elements already present in the mass function.
        """
        for focal in focal_elements:
            if focal[0] in self.focals:
                self.focals[focal[0]] -= focal[1]
            else:
                self.focals[focal[0]] = -focal[1]

    ################################################################################

    def remove_mass_unsafe(self, *focal_elements):
        """
        Removes mass to the current mass function given the focal elements provided.
        They should be provided as something accepting index operations
        with an ``element.Element`` at index 0 and the value at index 1 (e.g.
        tuples (DiscreteElement(3, 1), 1) or lists [DiscreteElement(2, 1), 0.5]).

        Remark 0: If an element wasn't present in the mass function, it removes the
            mass anyway.
        Remark 1: This does not care about the validity of the resulting mass function.
        Remark 2: It does modify the current mass function.
        Remark 3: It is possible to remove negative masses (thus adding mass), that's
            your problem.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            *focal_elements (*(Element, float)): A list of focal elements to remove 
                from the mass function.
        """
        for focal in focal_elements:
            if focal[0] in self.focals:
                self.focals[focal[0]] -= focal[1]
            else:
                self.focals[focal[0]] = -focal[1]
                
    ################################################################################
    
    def clean(self):
        """
        Cleans the current mass function from all the focal elements with a value
        lower than the precision given by ``MassFunction.precision``.

        Remark: It does modify the current mass function.
        """
        newDict = {}
        for element, value in self.focals.items():
            if value >= MassFunction.precision:
                newDict[element] = value
        self.focals = newDict

    ################################################################################

    def normalise(self):
        """
        Normalises the current mass function.

        Remark: It does modify the current mass function.
        """
        s = self._sum()
        if s != 0:
            for element, value in self.focals.items():
                self.focals[element] /= s

    ################################################################################
    ################################################################################
    ################################################################################

    # *******************
    # Validation methods:
    # *******************

    def is_compatible(self, mass_function):
        """
        Checks that the given mass function is compatible with the current one
        (it basically checks if their focal elements are compatible). This assumes
        that the mass functions are already consistent in themselves.

        Args:
            mass_function: The mass function to check compatibility with.
        Returns:
            bool -- ``True`` if both mass functions are compatible, ``False``
            otherwise.
        """
        if self.is_empty() or mass_function.is_empty():
            return True

        #Check that any element of self is compatible with any element of massfunction:
        anyFocal1 = next(iter(self.focals))
        anyFocal2 = next(iter(mass_function.focals))
        return anyFocal1.is_compatible(anyFocal2)
    
    ################################################################################

    def is_empty(self):
        """
        Checks if the current mass function is empty or not. It more exactly checks
        if the sum of its focal elements is null or not.

        Returns:
            bool -- ``True`` if there is no mass, ``False`` otherwise.
        """
        return self._sum() == 0

    ################################################################################

    def has_valid_values(self):
        """
        Checks that all the values stored in the current mass function are valid
        (0 <= value <= 1).

        Returns:
            bool -- ``True``if all the masses are valid, ``False`` otherwise.
        """
        for element, value in self.items():
            if not (0 <= value <= 1):
                return False
        return True

    ################################################################################

    def has_valid_sum(self):
        """
        Checks that the current mass function has a valid sum.

        Returns:
            bool -- ``True`` if the sum is valid, ``False`` otherwise.
        """
        return 1 - MassFunction.precision <= self._sum() <= 1 + MassFunction.precision

    ################################################################################

    def is_valid(self):
        """
        Checks that the current mass function is valid (valid sum + valid values).

        Returns:
            bool -- ``True`` if the mass function is valid, ``False`` otherwise.
        """
        return self.has_valid_values() and self.has_valid_sum()

    ################################################################################

    def _sum(self):
        """
        Gives the sum of the masses stored in the mass function.

        Returns:
            float -- The sum of all the masses.
        """
        s = 0
        for element, value in self.items():
            s += value
        return s

    ################################################################################
    ################################################################################
    ################################################################################

    # *************************************
    # Decision making criteria and methods:
    # *************************************

    def m(self, element):
        """
        Gets the mass of the given element in the current mass function.
        Equivalent to ``self.mass(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The mass for the given element in the current mass function.
        """
        if element in self.focals:
            return self.focals[element]
        return 0

    ################################################################################

    def mass(self, element):
        """
        Gets the mass of the given element in the current mass function.
        Equivalent to ``self.m(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The mass for the given element in the current mass function.
        """
        return self.m(element)

    ################################################################################

    def bel(self, element):
        """
        Gets the belief/credibility of the given element in the current mass function.
        Equivalent to ``self.belief(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The belief for the given element in the current mass function.
        """
        if element.is_empty():
            return 0

        if self.is_empty():
            return 0

        if not element.is_compatible(next(iter(self.focals))):
            return 0
        
        result = 0
        for focal, value in self.items():
            if not focal.is_empty() and focal.is_subset(element):
                result += value
        return round(result, 6)

    ################################################################################

    def belief(self, element):
        """
        Gets the belief of the given element in the current mass function.
        Equivalent to ``self.bel(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The belief for the given element in the current mass function.
        """
        return self.bel(element)

    ################################################################################

    def betP(self, element):
        """
        Gets the pignistic transformation value of the given element in the current
        mass function. Equivalent to ``self.pignistic_transformation(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The pignistic transformation value for the given element in the
            current mass function.
        """
        if element.is_empty():
            return 0

        if self.is_empty():
            return 0

        if not element.is_compatible(next(iter(self.focals))):
            return 0

        result = 0
        for focal, value in self.items():
            if not focal.is_empty():
                result += value * focal.conjunction_unsafe(element).cardinal / focal.cardinal
        return round(result, 6)

    ################################################################################

    def pignistic_transformation(self, element):
        """
        Gets the pignistic transformation value of the given element in the current
        mass function. Equivalent to ``self.betP(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The pignistic transformation value for the given element in the
            current mass function.
        """
        return self.betP(element)

    ################################################################################

    def pl(self, element):
        """
        Gets the plausibility of the given element in the current mass function.
        Equivalent to ``self.plausibility(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The plausibility of the given element in the current mass function.
        """
        
        if self.is_empty():
            return 0

        if element.is_empty():
            return self._sum()

        if not element.is_compatible(next(iter(self.focals))):
            return 0
        
        result = 0
        for focal, value in self.items():
            if not element.conjunction_unsafe(focal).is_empty():
                result += value
        return round(result, 6)
    
    ################################################################################

    def plausibility(self, element):
        """
        Gets the plausibility of the given element in the current mass function.
        Equivalent to ``self.pl(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The plausibility of the given element in the current mass function.
        """
        return self.pl(element)

    ################################################################################

    def q(self, element):
        """
        Gets the commonality of the given element in the current mass function.
        Equivalent to ``self.commonality(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The commonality of the given element in the current mass function.
        """
        
        if self.is_empty():
            return 0

        if element.is_empty():
            return self._sum()

        if not element.is_compatible(next(iter(self.focals))):
            return 0

        result = 0
        for focal, value in self.items():
            if element.is_subset(focal):
                result += value
        return round(result, 6)

    ################################################################################

    def commonality(self, element):
        """
        Gets the commonality of the given element in the current mass function.
        Equivalent to ``self.q(element)``.

        Args:
            element (Element): The element to look for.
        Returns:
            float -- The commonality of the given element in the current mass function.
        """
        return self.q(element)

    ################################################################################

    @staticmethod
    def get_min(criterion, max_card, elements):
        """
        Gets the minima for the given criteria (in the form my_instance.my_function), maximum
        cardinal and an iterable of elements. This method can be called for discrete elements
        using for instance ``DiscreteElement.iterator_powerset(size)`` as a list of elements.
        
        Remark 0: This is not checking for elements compatibility, so it might return
            a lot of zeros if the elements are incompatible with the mass function.
        Remark 1: Does not consider the empty set as a valid answer.
        Remark 2: Good candidates for criteria are ``m.mass``, ``m.bel``,
            ``m.betP``, ``m.pl`` or ``m.q`` applied to an instance.

        Args:
            criterion (func.): A method on MassFunctions that takes exactly one element
                as argument.
            max_card (int): The maximum cardinal requested for the elements found as minima.
            elements (iter. Elements): An iterable containing the list of Elements to
                look into.
        Returns:
            list[tuple(Element, value), ...] -- A list of couples corresponding to the found
            minima for the current mass function given the criteria, the maximum cardinal and
            a set of elements to look into.
        Raises:
            ValueError: If max_card is null or negative.
        """
        if max_card <= 0:
            raise ValueError(
                "max_card: " + str(max_card) + "\n" +
                "The maximum cardinal cannot be null nor negative!"
            )

        minima = []
        currentMin = 1000000000
        for e in elements:
            if 0 < e.cardinal <= max_card:
                if len(minima) == 0:
                    currentMin = criterion(e)
                    minima.append((e, currentMin))
                else:
                    newCandidate = criterion(e)
                    if newCandidate == currentMin:
                        minima.append((e, currentMin))
                    elif newCandidate < currentMin:
                        minima = []
                        currentMin = newCandidate
                        minima.append((e, currentMin))
        return minima

    ################################################################################

    @staticmethod
    def get_max(criterion, max_card, elements):
        """
        Gets the maxima for the given criteria (in the form my_instance.my_function), maximum
        cardinal and an iterable of elements. This method can be called for discrete elements
        using for instance ``DiscreteElement.iterator_powerset(size)`` as a list of elements.

        Remark 0: This is not checking for elements compatibility, so it might return
            a lot of zeros if the elements are incompatible with the mass function.
        Remark 1: Does not consider the empty set as a valid answer.
        Remark 2: Good candidates for criterion are ``m.mass``, ``m.bel``,
            ``m.betP``, ``m.pl`` or ``m.q`` applied to an instance.
            
        Args:
            criterion (func.): A method on MassFunctions that takes exactly one element
                as argument.
            max_card (int): The maximum cardinal requested for the elements found as minima.
            elements (iter. Elements): An iterable containing the list of Elements to
                look into.
        Returns:
            list[tuple(Element, value), ...] -- A list of couples corresponding to the found
            maxima for the current mass function given the criteria, the maximum cardinal and
            a set of elements to look into.
        Raises:
            ValueError: If max_card is null or negative.
        """
        if max_card <= 0:
            raise ValueError(
                "max_card: " + str(max_card) + "\n" +
                "The maximum cardinal cannot be null nor negative!"
            )

        maxima = []
        currentMax = 0
        for e in elements:
            if 0 < e.cardinal <= max_card:
                if len(maxima) == 0:
                    currentMax = criterion(e)
                    maxima.append((e, currentMax))
                else:
                    newCandidate = criterion(e)
                    if newCandidate == currentMax:
                        maxima.append((e, currentMax))
                    elif newCandidate > currentMax:
                        maxima = []
                        currentMax = newCandidate
                        maxima.append((e, currentMax))
        return maxima

    ################################################################################

    @staticmethod
    def format_extrema_result(result):
        """
        Gives a nicely formatted string ready to print for the get_min()/get_max()
        results.

        Args:
            result (list[tuple(Element, value), ...]): The results provided by either
                get_min() or get_max().
        Returns:
            string -- A nicely formatted string in the form [(element1, value1), ...].
        """
        s = ""
        for t in result:
            s += "(" + str(t[0]) + ", " + "{:.4f}".format(t[1]) + "), "
        return "[" + s[:-2] + "]"
    
    ################################################################################
    ################################################################################
    ################################################################################

    # ***********************************
    # Characterisation of mass functions:
    # ***********************************

    def specificity(self):
        """
        Gets the specificity of the current mass function. For a definition, refer
        to "Yager, R.: Entropy and specificity in a mathematical theory of evidence, 1983".

        Returns:
            float -- The specificity of the current mass function.
        """
        result = 0
        for focal, value in self.items():
            if focal.cardinal > 0:
                result += value / focal.cardinal
        return round(result, 6)

    ################################################################################

    def non_specificity(self):
        """
        Gets the non-specificity of the current mass function. For a definition, refer
        to "Yager, R.: Entropy and specificity in a mathematical theory of evidence, 1983".

        Returns:
            float -- The non-specificity of the current mass function.
        """
        result = 0
        for focal, value in self.items():
            if focal.cardinal > 0:
                result += value * math.log(focal.cardinal, 2)
        return round(result, 6)

    ################################################################################

    def discrepancy(self):
        """
        Gets the discrepancy of the current mass function. For a definition, refer
        to "J. Abellan and S. Moral, Completing a total uncertainty measure in
        Dempster-Shafer theory, 1999".

        Returns:
            float -- The discrepancy of the current mass function.
        """
        result = 0
        for focal, value in self.items():
            if focal.cardinal > 0:
                result -= value * math.log(self.betP(focal), 2)
        return round(result, 6)

    ################################################################################
    ################################################################################
    ################################################################################

    # *********************************
    # Discounting/Conditioning methods:
    # *********************************

    @check_mass_function_is_not_empty
    def weakening(self, alpha):
        """
        Gives a new mass function that is the weakened version of the current one.
        This operation is close to discounting but instead of transfering mass to
        the complete set, transfers it to the empty set.

        Remark: Does not modify the current mass function.

        Args:
            alpha (float): The proportion of mass that will be lost by all focal
                elements (should respect 0 <= alpha <= 1).
        Returns:
            MassFunction -- A new mass function that corresponds to the weakened
            version of the current one.
        Raises:
            EmptyMassFunctionError: If it is applied to an empty mass function.
            ValueError: If 0 <= alpha <= 1 is not true.
        """
        if not (0 <= alpha <= 1):
            raise ValueError(
                "alpha: " + str(alpha) + "\n" +
                "0 <= alpha <= 1 should be true!"
            )

        result = MassFunction()
        for focal, value in self.items():
            weakened = value * (1 - alpha)
            result.add_mass((focal, round(value * (1 - alpha), 6)))
        result.add_mass((focal.get_compatible_empty_element(), alpha))
        return result

    ################################################################################

    @check_mass_function_is_not_empty
    def discounting(self, alpha):
        """
        Gives a new mass function that is the discounted version of the current one.
        This operation transfers a part of the mass of all the focal elements to
        the complete set (the "I don't know" state, i.e. m(Omega)).

        Remark: Does not modify the current mass function.

        Args:
            alpha (float): The proportion of mass that will be lost by all focal
                elements (should respect 0 <= alpha <= 1).
        Returns:
            MassFunction -- A new mass function that corresponds to the discounted
            version of the current one.
        Raises:
            EmptyMassFunctionError: If it is applied to an empty mass function.
            ValueError: If 0 <= alpha <= 1 is not true.
        """
        if not (0 <= alpha <= 1):
            raise ValueError(
                "alpha: " + str(alpha) + "\n" +
                "0 <= alpha <= 1 should be true!"
            )

        result = MassFunction()
        for focal, value in self.items():
            result.add_mass((focal, round(value * (1 - alpha), 6)))
        result.add_mass((focal.get_compatible_complete_element(), alpha))
        return result

    ################################################################################

    @check_mass_function_is_not_empty
    def conditioning(self, element):
        """
        Gets a new mass function that is the conditioned version of the current one.
        For a definition, refer to "P. Smets, The transferable belief model for belief
        representation, 1999".

        Remark: Does not modify the current mass function.

        Args:
            element (Element): The element to condition by, doesn't have to be atomic.
        Returns:
            MassFunction -- A new mass function that is the conditioned version of
            the current one.
        Raises:
            EmptyMassFunctionError: If if is applied to an empty mass function.
            IncompatibleElementsInAMassFunctionError: If the given element is incompatible
                with the current mass function.
        """
        if not next(iter(self)).is_compatible(element):
            raise IncompatibleElementsInAMassFunctionError(next(iter(self)), element)
        
        condition = MassFunction((element, 1))
        return self.combination_smets(condition)

    ################################################################################
    ################################################################################
    ################################################################################

    # *******************
    # Comparison methods:
    # *******************

    @check_arguments_are_mass_functions
    @check_mass_functions_compatibility
    def difference(self, mass_function):
        """
        Does the difference between the current mass function and the given one.
        Used only to compute the distance.

        Remark 0: Does not give a proper mass function!
        Remark 1: Does not modify the current mass function.

        Args:
            mass_function (MassFunction): The mass function to do the difference with.
        Returns:
            MassFunction -- A new mass function corresponding to the difference
            between the current one and the given one.
        Raises:
            TypeError: If the provided argument is not a mass function.
            IncompatibleMassFunctionsError: If the current mass function and the
                given one are incompatible (they are if their focal elements are
                incompatible).
        """
        result = copy.deepcopy(self)
        for focal, value in mass_function.items():
            result.remove_mass((focal, value))

        newFocals = {}
        for focal, value in result.items():
            if value != 0:
                newFocals[focal] = value
        result.focals = newFocals
        return result

    ################################################################################

    def difference_unsafe(self, mass_function):
        """
        Does the difference between the current mass function and the given one.
        Used only to compute the distance.

        Remark 0: Does not give a proper mass function!
        Remark 1: Does not modify the current mass function.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_function (MassFunction): The mass function to do the difference with.
        Returns:
            MassFunction -- A new mass function corresponding to the difference
            between the current one and the given one.
        """
        result = copy.deepcopy(self)
        for focal, value in mass_function.items():
            result.remove_mass_unsafe((focal, value))

        newFocals = {}
        for focal, value in result.items():
            if value != 0:
                newFocals[focal] = value
        result.focals = newFocals
        return result

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def distance(self, *mass_functions):
        """
        Gets the classic distance between the current mass function and the given ones.
        For a definition, refer to "A. Jousselme et al, A new distance between two
        bodies of evidence, 2001".
        
        Args:
            mass_functions (*MassFunction): The mass functions to compute the
                distance with.
        Returns:
            float -- The distance between the current mass function and the given ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        #Submethod to get distance between self and one mass function:
        def distance_one_mass(mass_function):
            #Get the jaccard index matrix:
            difference = self.difference(mass_function)
            matrix = {}
            for e1 in difference:
                matrix[e1] = {}
                for e2 in difference:
                    if (not e1.is_empty()) or (not e2.is_empty()):
                        matrix[e1][e2] = e1.conjunction(e2).cardinal / e1.disjunction(e2).cardinal
                    else:
                        matrix[e1][e2] = 1
            
            #Compute the distance as sqtr(0.5 * diffT * matrix * diff):
            distance = 0
            temp = {}
            for e1 in difference:
                temp[e1] = 0
                for e2 in difference:
                    temp[e1] += difference[e2] * matrix[e1][e2]
            for e1 in difference:
                distance += temp[e1] * difference[e1]
            return math.sqrt(0.5 * distance)

        #Get the distance between self and the provided set of mass functions:
        distance = 0
        for mass_function in mass_functions:
            distance += distance_one_mass(mass_function)
        return round(distance / len(mass_functions), 6)

    ################################################################################

    def distance_unsafe(self, *mass_functions):
        """
        Gets the classic distance between the current mass function and the given ones.
        For a definition, refer to "A. Jousselme et al, A new distance between two
        bodies of evidence, 2001".
        
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to compute the
                distance with.
        Returns:
            float -- The distance between the current mass function and the given ones.

        """
        #Submethod to get distance between self and one mass function:
        def distance_one_mass(mass_function):
            #Get the jaccard index matrix:
            difference = self.difference_unsafe(mass_function)
            matrix = {}
            for e1 in difference:
                matrix[e1] = {}
                for e2 in difference:
                    if (not e1.is_empty()) or (not e2.is_empty()):
                        matrix[e1][e2] = e1.conjunction_unsafe(e2).cardinal / e1.disjunction_unsafe(e2).cardinal
                    else:
                        matrix[e1][e2] = 1
            
            #Compute the distance as sqtr(0.5 * diffT * matrix * diff):
            distance = 0
            temp = {}
            for e1 in difference:
                temp[e1] = 0
                for e2 in difference:
                    temp[e1] += difference[e2] * matrix[e1][e2]
            for e1 in difference:
                distance += temp[e1] * difference[e1]
            return math.sqrt(0.5 * distance)

        #Get the distance between self and the provided set of mass functions:
        distance = 0
        for mass_function in mass_functions:
            distance += distance_one_mass(mass_function)
        return round(distance / len(mass_functions), 6)

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def similarity(self, mass_function):
        """
        Gets the similarity between the current mass function and the given one.
        For a definition, please refer to "L.-Z. Chen: A new fusion approach based on distance
        of evidences, 2005".

        Args:
            mass_function (MassFunction): The mass function to compute the similarity with.
        Returns:
            float -- The similarity between the current mass function and the given one.
        Raises:
            TypeError: If the provided argument is not a mass function.
            EmptyMassFunctionError: If the current mass function or the provided one
                mass functions is empty.
            IncompatibleMassFunctionsError: If the current mass function and the provided
                one are incompatible.
        """
        return round(0.5 * (math.cos(math.pi * self.distance(mass_function)) + 1), 6)
    
    ################################################################################

    def similarity_unsafe(self, mass_function):
        """
        Gets the similarity between the current mass function and the given one.
        For a definition, please refer to "L.-Z. Chen: A new fusion approach based on distance
        of evidences, 2005".

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_function (MassFunction): The mass function to compute the similarity with.
        Returns:
            float -- The similarity between the current mass function and the given one.
        """
        return round(0.5 * (math.cos(math.pi * self.distance_unsafe(mass_function)) + 1), 6)

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def support(self, *mass_functions):
        """
        Gets the support of the current mass function given a set of mass functions,
        i.e. the sum of the similarities of the current mass function with the given
        ones. For a definition, please refer to "L.-Z. Chen: A new fusion approach based
        on distance of evidences, 2005".

        Args:
            mass_functions (*MassFunction): The mass functions to compute the support with.
        Returns:
            float -- The support given by the provided mass functions to the current one.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        result = 0
        for mass_function in mass_functions:
            result += self.similarity(mass_function)
        return round(result, 6)
    
    ################################################################################

    def support_unsafe(self, *mass_functions):
        """
        Gets the support of the current mass function given a set of mass functions,
        i.e. the sum of the similarities of the current mass function with the given
        ones. For a definition, please refer to "L.-Z. Chen: A new fusion approach based
        on distance of evidences, 2005".

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to compute the support with.
        Returns:
            float -- The support given by the provided mass functions to the current one.
        """
        result = 0
        for mass_function in mass_functions:
            result += self.similarity_unsafe(mass_function)
        return round(result, 6)

    ################################################################################

    @staticmethod
    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def credibility(*mass_functions):
        """
        Gets the vector of credibility of the given mass functions compared to each
        others. For a definition, please refer to "L.-Z. Chen: A new fusion approach
        based on distance of evidences, 2005".

        Args:
            mass_functions (*MassFunction): The mass functions to compute the credibility for.
        Returns:
            list[floats] -- The credibility of the provided mass functions given each others.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        #Get the supports of each mass function:
        supports = []
        for mass_function in mass_functions:
            supports.append(mass_function.support(*[x for x in mass_functions if x != mass_function]))
            
        #Compute the credibility of each mass function:
        cred = []
        supportSum = sum(supports)
        for i in range(len(mass_functions)):
            cred.append(round(supports[i]/supportSum, 6))
        return cred
    
    ################################################################################

    @staticmethod
    def credibility_unsafe(*mass_functions):
        """
        Gets the vector of credibility of the given mass functions compared to each
        others. For a definition, please refer to "L.-Z. Chen: A new fusion approach
        based on distance of evidences, 2005".

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to compute the credibility for.
        Returns:
            list[floats] -- The credibility of the provided mass functions given each others.
        """
        #Get the supports of each mass function:
        supports = []
        for mass_function in mass_functions:
            supports.append(mass_function.support_unsafe(*[x for x in mass_functions if x != mass_function]))
            
        #Compute the credibility of each mass function:
        cred = []
        supportSum = sum(supports)
        for i in range(len(mass_functions)):
            cred.append(round(supports[i]/supportSum, 6))
        return cred
    
    ################################################################################
    ################################################################################
    ################################################################################

    # ******************
    # Combination rules:
    # ******************

    def combination(self, combination_rule, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the combination rule selected
        (see ``MassFunction.Combination`` for details on which ones are available).

        Remark: Does not modify the current mass function.
        
        Args:
            combination_rule (MassFunction.Combination): The combination rule to use.
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            ValueError: If the combination rule requested is not recognised.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        if combination_rule == MassFunction.Combination.Dempster:
            return self.combination_dempster(*mass_functions)
        elif combination_rule == MassFunction.Combination.Smets:
            return self.combination_smets(*mass_functions)
        elif combination_rule == MassFunction.Combination.Disjunctive:
            return self.combination_disjunctive(*mass_functions)
        elif combination_rule == MassFunction.Combination.Yager:
            return self.combination_yager(*mass_functions)
        elif combination_rule == MassFunction.Combination.DuboisPrade:
            return self.combination_dubois_prade(*mass_functions)
        elif combination_rule == MassFunction.Combination.Average:
            return self.combination_average(*mass_functions)
        elif combination_rule == MassFunction.Combination.Murphy:
            return self.combination_murphy(*mass_functions)
        elif combination_rule == MassFunction.Combination.Chen:
            return self.combination_chen(*mass_functions)
        else:
            raise ValueError(
                "combination_rule:" + str(combination_rule) + "\n" +
                "The provided combination rule was not recognised, see the enumeration " +
                "MassFunction.Combination for more information!"
            )
    
    ################################################################################

    def combination_unsafe(self, combination_rule, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the combination rule selected
        (see ``MassFunction.Combination`` for details on which ones are available).

        Remark: Does not modify the current mass function.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            combination_rule (MassFunction.Combination): The combination rule to use.
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            ValueError: If the combination rule requested is not recognised.
        """
        if combination_rule == MassFunction.Combination.Dempster:
            return self.combination_dempster_unsafe(*mass_functions)
        elif combination_rule == MassFunction.Combination.Smets:
            return self.combination_smets_unsafe(*mass_functions)
        elif combination_rule == MassFunction.Combination.Disjunctive:
            return self.combination_disjunctive_unsafe(*mass_functions)
        elif combination_rule == MassFunction.Combination.Yager:
            return self.combination_yager_unsafe(*mass_functions)
        elif combination_rule == MassFunction.Combination.DuboisPrade:
            return self.combination_dubois_prade_unsafe(*mass_functions)
        elif combination_rule == MassFunction.Combination.Average:
            return self.combination_average_unsafe(*mass_functions)
        elif combination_rule == MassFunction.Combination.Murphy:
            return self.combination_murphy_unsafe(*mass_functions)
        elif combination_rule == MassFunction.Combination.Chen:
            return self.combination_chen_unsafe(*mass_functions)
        else:
            raise ValueError(
                "combination_rule:" + str(combination_rule) + "\n" +
                "The provided combination rule was not recognised, see the enumeration " +
                "MassFunction.Combination for more information!"
            )
        
    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_dempster(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using Dempster's rule of combination.
        If you need details on this rule, maybe you shouldn't be using this library.

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        #Define the combination for only two mass functions:
        def combination_two(m1, m2):
            combination = m1.combination_smets(m2)
            combination.focals.pop(next(iter(combination)).get_compatible_empty_element(), None)
            combination.clean()
            combination.normalise()
            return combination

        #Combine all the mass functions:
        combination = combination_two(self, mass_functions[0])
        for mass_function in mass_functions[1:]:
            combination = combination_two(combination, mass_function)
        return combination
        
    ################################################################################

    def combination_dempster_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using Dempster's rule of combination.
        If you need details on this rule, maybe you shouldn't be using this library.

        Remark: Does not modify the current mass function.
        
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        #Define the combination for only two mass functions:
        def combination_two(m1, m2):
            combination = m1.combination_smets_unsafe(m2)
            combination.focals.pop(next(iter(combination)).get_compatible_empty_element(), None)
            combination.clean()
            combination.normalise()
            return combination

        #Combine all the mass functions:
        combination = combination_two(self, mass_functions[0])
        for mass_function in mass_functions[1:]:
            combination = combination_two(combination, mass_function)
        return combination
    
    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_smets(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using Smets' rule of combination (
        a.k.a. the unnormalised Dempster's rule of combination).
        For a definition, refer to "P. Smets, Belief functions: The disjunctive rule of
        combination and the generalized bayesian theorem, 1993".

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        #Define the combination for only two mass functions:
        def combination_two(m1, m2):
            combination = MassFunction()
            for e1, mass1 in m1.items():
                for e2, mass2 in m2.items():
                    combination.add_mass((e1.conjunction(e2), mass1*mass2))
            combination.clean()
            return combination

        #Combine all the mass functions:
        combination = combination_two(self, mass_functions[0])
        for mass_function in mass_functions[1:]:
            combination = combination_two(combination, mass_function)
        return combination
    
    ################################################################################

    def combination_smets_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using Smets' rule of combination (
        a.k.a. the unnormalised Dempster's rule of combination).
        For a definition, refer to "P. Smets, Belief functions: The disjunctive rule of
        combination and the generalized bayesian theorem, 1993".

        Remark: Does not modify the current mass function.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        #Define the combination for only two mass functions:
        def combination_two(m1, m2):
            combination = MassFunction()
            for e1, mass1 in m1.items():
                for e2, mass2 in m2.items():
                    combination.add_mass_unsafe((e1.conjunction_unsafe(e2), mass1*mass2))
            combination.clean()
            return combination

        #Combine all the mass functions:
        combination = combination_two(self, mass_functions[0])
        for mass_function in mass_functions[1:]:
            combination = combination_two(combination, mass_function)
        return combination

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_disjunctive(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the disjunctive rule of combination.
        For a definition, refer to "P. Smets, Belief functions: The disjunctive rule of
        combination and the generalized bayesian theorem, 1993".

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        #Define the combination for only two mass functions:
        def combination_two(m1, m2):
            combination = MassFunction()
            for e1, mass1 in m1.items():
                for e2, mass2 in m2.items():
                    combination.add_mass((e1.disjunction(e2), mass1*mass2))
            combination.clean()
            return combination

        #Combine all the mass functions:
        combination = combination_two(self, mass_functions[0])
        for mass_function in mass_functions[1:]:
            combination = combination_two(combination, mass_function)
        return combination

    ################################################################################

    def combination_disjunctive_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the disjunctive rule of combination.
        For a definition, refer to "P. Smets, Belief functions: The disjunctive rule of
        combination and the generalized bayesian theorem, 1993".

        Remark: Does not modify the current mass function.
        
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        #Define the combination for only two mass functions:
        def combination_two(m1, m2):
            combination = MassFunction()
            for e1, mass1 in m1.items():
                for e2, mass2 in m2.items():
                    combination.add_mass_unsafe((e1.disjunction_unsafe(e2), mass1*mass2))
            combination.clean()
            return combination

        #Combine all the mass functions:
        combination = combination_two(self, mass_functions[0])
        for mass_function in mass_functions[1:]:
            combination = combination_two(combination, mass_function)
        return combination

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_yager(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Yager's rule of combination.
        For a definition, refer to "R. Yager: On the Dempster-Shafer framework and new
        combination rules, 1987".

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        combination = self.combination_smets(*mass_functions)
        empty = next(iter(combination)).get_compatible_empty_element()
        complete = next(iter(combination)).get_compatible_complete_element()
        combination[complete] = combination.mass(empty)
        combination.focals.pop(empty, None)
        return combination

    ################################################################################

    def combination_yager_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Yager's rule of combination.
        For a definition, refer to "R. Yager: On the Dempster-Shafer framework and new
        combination rules, 1987".

        Remark: Does not modify the current mass function.
        
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        combination = self.combination_smets_unsafe(*mass_functions)
        empty = next(iter(combination)).get_compatible_empty_element()
        complete = next(iter(combination)).get_compatible_complete_element()
        combination[complete] = combination.mass(empty)
        combination.focals.pop(empty, None)
        return combination

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_dubois_prade(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Dubois and Prade's rule
        of combination.
        For a definition, refer to "D. Dubois and H. Prade: Representation and Combination 
        of Uncertainty with Belief Functions and Possibility Measures, 1988".

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        functions = [self]
        functions.extend(list(mass_functions))

        combination = MassFunction()
        for c in itertools.product(*functions):
            masses = []
            for e, m in zip(c, functions):
                masses.append(m.m(e))
            massToAdd = functools.reduce(operator.mul, masses, 1) #Replaces a lacking product() built-in function
            resultElement = element.Element.static_conjunction(*c)
            
            if resultElement.is_empty():
                resultElement = element.Element.static_disjunction(*c)
            combination.add_mass((resultElement, massToAdd))
        combination.clean()
        return combination

    ################################################################################

    def combination_dubois_prade_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Dubois and Prade's rule
        of combination.
        For a definition, refer to "D. Dubois and H. Prade: Representation and Combination 
        of Uncertainty with Belief Functions and Possibility Measures, 1988".

        Remark: Does not modify the current mass function.
        
        WARNING: IT CAN HARM YOUR POOR COMPUTER IF USED WITH AN UNREASONABLY BIG NUMBER
        OF MASS FUNCTIONS ALL CONTAINING A LOT OF FOCAL ELEMENTS.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        functions = [self]
        functions.extend(list(mass_functions))

        combination = MassFunction()
        for c in itertools.product(*functions):
            masses = []
            for e, m in zip(c, functions):
                masses.append(m.m(e))
            massToAdd = functools.reduce(operator.mul, masses, 1) #Replaces a lacking product() built-in function
            resultElement = element.Element.static_conjunction_unsafe(*c)
            
            if resultElement.is_empty():
                resultElement = element.Element.static_disjunction_unsafe(*c)
            combination.add_mass_unsafe((resultElement, massToAdd))
        combination.clean()
        return combination

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_average(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the average rule of combination.
        As its name suggests, this is a simple average.

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        combination = copy.deepcopy(self)
        for mass_function in mass_functions:
            for element, mass in mass_function.items():
                combination.add_mass((element, mass))
        for element, mass in combination.items():
            combination[element] /= len(mass_functions) + 1
        return combination

    ################################################################################

    def combination_average_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the average rule of combination.
        As its name suggests, this is a simple average.

        Remark: Does not modify the current mass function.
        
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        combination = copy.deepcopy(self)
        for mass_function in mass_functions:
            for element, mass in mass_function.items():
                combination.add_mass_unsafe((element, mass))
        for element, mass in combination.items():
            combination[element] /= len(mass_functions) + 1
        return combination

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_murphy(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Murphy's rule of combination.
        For a definition, refer to "C. K. Murphy: Combining belief functions when evidence
        conflicts, 2000".

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        average = self.combination_average(*mass_functions)
        return average.combination_dempster(*([average]*len(mass_functions)))

    ################################################################################

    def combination_murphy_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Murphy's rule of combination.
        For a definition, refer to "C. K. Murphy: Combining belief functions when evidence
        conflicts, 2000".

        Remark: Does not modify the current mass function.
        
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        average = self.combination_average_unsafe(*mass_functions)
        return average.combination_dempster_unsafe(*([average]*len(mass_functions)))

    ################################################################################

    @check_arguments_are_mass_functions
    @check_mass_function_are_not_empty
    @check_mass_functions_compatibility
    def combination_chen(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Chen's rule of combination.
        For a definition, please refer to "L.-Z. Chen: A new fusion approach based on distance
        of evidences, 2005".

        Remark: Does not modify the current mass function.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        Raises:
            TypeError: If at least one of the provided arguments is not a mass function.
            EmptyMassFunctionError: If the current mass function or one of the provided
                mass functions is empty.
            IncompatibleMassFunctionsError: If at least two of the mass functions are
                incompatible with each others.
        """
        #Get the credibility:
        masses = [self]
        masses.extend(list(mass_functions))
        credibility = MassFunction.credibility(*masses)

        #Add the masses:
        beforeDempster = MassFunction()
        for cred, mass in zip(credibility, masses):
            for focal, value in mass.items():
                beforeDempster.add_mass((focal, value*cred))
        
        #N-1 Dempster combinations:
        return beforeDempster.combination_dempster(*([beforeDempster]*len(mass_functions)))

    ################################################################################

    def combination_chen_unsafe(self, *mass_functions):
        """
        Gets a new mass function corresponding to the result of the combination of the
        current mass function with the provided ones using the Chen's rule of combination.
        For a definition, please refer to "L.-Z. Chen: A new fusion approach based on distance
        of evidences, 2005".

        Remark: Does not modify the current mass function.
        
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            mass_functions (*MassFunction): The mass functions to combine with the current
                one.
        Returns:
            MassFunction -- A new mass function that is the combination of the current one
            with the provided ones.
        """
        #Get the credibility:
        masses = [self]
        masses.extend(list(mass_functions))
        credibility = MassFunction.credibility_unsafe(*masses)

        #Add the masses:
        beforeDempster = MassFunction()
        for cred, mass in zip(credibility, masses):
            for focal, value in mass.items():
                beforeDempster.add_mass_unsafe((focal, value*cred))
        
        #N-1 Dempster combinations:
        return beforeDempster.combination_dempster_unsafe(*([beforeDempster]*len(mass_functions)))

    ################################################################################
    
    def auto_conflict(self, degree):
        """
        Gets the auto-conflict up to ``degree`` degree as a list of values.
        For a complete definition, refer to "A. Martin et al.: Conflict measure for the
        discounting operation on belief functions, 2008".
        To easily access the the highest degree of auto-conflict requested, you can use
        ``mass_function.auto_conflict(degree)[-1]``.

        Args:
            degree (int): The degree up to which the auto-conflict should be computed.
        Returns:
            list[float] -- The auto-conflicts value, in order from degree 1 to the
            requested degree.
        Raises:
            EmptyMassFunctionError: If the current mass function is empty.
            ValueError: If the requested degree is null or negative.
        """
        if self.is_empty():
            raise EmptyMassFunctionError()
        
        if degree < 1:
            raise ValueError(
                "degree: " + str(degree) + "\n" +
                "The degree of auto-conflict cannot be null or negative, it does " +
                "not make sense!"
            )

        result = []
        empty_element = next(iter(self)).get_compatible_empty_element()
        
        combination = self.combination_smets(self)
        result.append(combination.mass(empty_element))
        for i in range(degree-1):
            combination = combination.combination_smets(self)
            result.append(combination.mass(empty_element))

        return result
    
    ################################################################################
    ################################################################################
    ################################################################################

    # *************************************************
    # Temporisation methods for dynamic mass functions:
    # *************************************************

    def temporisation_specificity(self, old_time, new_time, max_time, new_mass_function, got_data=True):
        """
        Gets a new mass function which corresponds to the temporisation with discrimination
        based on specificity. This is to be used with a continuous flow of mass functions
        (obtained for instance from sensor measurements), to stabilise the belief over time.
        For more details, refer to "B. Pietropaoli et al., Belief Inference with Timed
        Evidence, 2012".

        Remark 0: This should be applied to an old mass function.
        Remark 1: This does not check anything, so be careful.
        Remark 2: This does not modify the current mass function.

        Args:
            old_time (float): The time at which the current mass function was acquired
                (if set to -1, then it considers that this is the first time this is
                applied and it won't do much).
            new_time (float): The time at which the new mass function was acquired.
            max_time (float): The maximum time before beliefs get totally forgotten
                (i.e. the time before the mass function get discounted with alpha = 1).
            new_mass_function (MassFunction): The new mass function that was obtained.
            got_data (bool): If the new mass function was obtained with data or not
                (this enables to differenciate vacuous mass functions induced by data
                from vacuous mass functions induced by loss of data).
        Returns:
            temporised (MassFunction): The result of the temporisation.
            new_old_time (float): The new old_time to consider in the next call of
                temporisation_specificity().
            new_old_mass_function (MassFunction): A new mass function which corresponds
                to the old one (to which the next call of temporisation_specificity()
                will be applied).
        """
        #First time this is applied:
        if old_time == -1:
            return copy.deepcopy(new_mass_function), new_time, copy.deepcopy(new_mass_function)

        elapsed = new_time - old_time
        #The new mass function is always considered if the old one would become vacuous:
        if elapsed > max_time:
            return copy.deepcopy(new_mass_function), new_time, copy.deepcopy(new_mass_function)
        #Apply temporisation:
        else:
            alpha = elapsed / max_time
            discounted = self.discounting(alpha)
            if not got_data:                                                                       #No data was received
                return discounted, old_time, copy.deepcopy(self)
            elif new_mass_function.specificity() >= discounted.specificity():                      #The new mass function is more specific
                return copy.deepcopy(new_mass_function), new_time, copy.deepcopy(new_mass_function)
            else:                                                                                  #The discounted one is more specific
                return discounted, old_time, copy.deepcopy(self)

    ################################################################################

    def temporisation_fusion(self, old_time, new_time, max_time, new_mass_function, got_data=True,
                             combination_rule=Combination.DuboisPrade):
        """
        Gets a new mass function which corresponds to the temporisation with fusion. This is
        to be used with a continuous flow of mass functions (obtained for instance from sensor
        measurements), to stabilise the belief over time.

        What it does quickly:
            - Discounts the current mass function depending on the time that has passed.
            - Fuse the discounted mass function with the new one.
            - If the new one wasn't inferred from data, then it returns the discounted one.
              This changes the way the belief with decrease with time. A sequence of vacuous
              mass functions obtained from data will create a smooth discounting in the form
              of something like (1 - e^X) while a sequence of data losses will create a linear
              discounting over time (equivalent to temporisation_specificity() to that regard).
        For more details, refer to "B. Pietropaoli, Stable context recognition in smart home,
        2013" (French)

        Remark 0: This should be applied to an old mass function.
        Remark 1: This does not check anything, so be careful.
        Remark 2: This does not modify the current mass function.

        Args:
            old_time (float): The time at which the current mass function was acquired
                (if set to -1, then it considers that this is the first time this is
                applied and it won't do much).
            new_time (float): The time at which the new mass function was acquired.
            max_time (float): The maximum time before beliefs get totally forgotten
                (i.e. the time before the mass function get discounted with alpha = 1).
            new_mass_function (MassFunction): The new mass function that was obtained.
            got_data (bool): If the new mass function was obtained with data or not
                (this enables to differenciate vacuous mass functions induced by data
                from vacuous mass functions induced by loss of data).
            combination_rule (MassFunction.Combination): The combination rule to use
                for the fusion of the discounted mass function with the new one.
        Returns:
            temporised (MassFunction): The result of the temporisation.
            new_old_time (float): The new old_time to consider in the next call of
                temporisation_fusion().
            new_old_mass_function (MassFunction): A new "old" mass function to store,
                the one on which the next call of temporisation_fusion() will be done.
        """
        #First time this is applied:
        if old_time == -1:
            return copy.deepcopy(new_mass_function), new_time, copy.deepcopy(new_mass_function)

        elapsed = new_time - old_time
        alpha = elapsed / max_time if elapsed < max_time else 1
        discounted = self.discounting(alpha)
        if not got_data:
            return discounted, old_time, copy.deepcopy(self)
        else:
            temporised = discounted.combination(combination_rule, new_mass_function)
            return temporised, new_time, copy.deepcopy(temporised)
        
    
    ################################################################################
    ################################################################################
    ################################################################################

    # *****************************
    # Making MassFunction iterable:
    # *****************************

    def __iter__(self):
        """
        Iterates over the focal elements. To be used with ``for`` statetements,
        e.g. ``for element in my_mass_function:``.

        Returns:
            element (Element): A focal element.
        """
        for element in self.focals:
            yield element
    
    ################################################################################
    
    def items(self):
        """
        Iterates over the focal elements and masses. To be used with ``for`` statements,
        e.g. ``for element, value in my_mass_function.items():``.

        Returns:
            element (Element): A focal element.
            value (float): The mass associated to the focal element.
        """
        for element, value in self.focals.items():
            yield (element, value)
    
    ################################################################################
    ################################################################################
    ################################################################################

    # ******************************
    # Overriding built-in functions:
    # ******************************

    def __str__(self):
        """
        Gives a string representation of the current mass function. The resulting
        string should be in the form ``{element1:value1, element2:value2, ...}``.
        Note that each value is limited to 4 digits after the period to improve
        readability.

        Returns:
            str -- Returns a string representing the current mass function.
        """
        #Get an ordered list of the elements strings so it outputs always the same
        #string given a mass function.
        elements = []
        for element in self.focals:
            elements.append((element, str(element)))
        sortedList = sorted(elements, key=lambda x:x[1])
        
        result = ""
        first = True
        for t in sortedList:
            if first:
                result += t[1] + ":" + "{:.4f}".format(self.focals[t[0]])
                first = False
            else:
                result += ", " + t[1] + ":" + "{:.4f}".format(self.focals[t[0]])
        return "{" + result + "}"
    
    ################################################################################

    def __eq__(self, m):
        """
        Overrides ``==``.
        Checks that the given mass function is equal to the current one. Two mass
        functions are equal if they have the same focal set and the same masses over
        their focal set.

        Args:
            m (MassFunction): The mass function to compare to.
        Returns:
            bool -- ``True``if the current mass function and the given one are equal,
            ``False`` otherwise.
        """
        #Check one way:
        for focal, value in self.items():
            if not focal in m:
                if value != 0 :
                    return False
            if round(m[focal], 6) != round(value, 6):
                return False
            
        #Check the other way:
        for focal, value in m.items():
            if not focal in self:
                if value != 0:
                    return False
            if round(self[focal], 6) != round(value, 6):
                return False
        return True

    ################################################################################

    def __getitem__(self, element):
        """
        Overrides access through ``[]``. Gets the mass for the given element.

        Args:
            element (Element): The element for which the mass is requested.
        Returns:
            float -- The mass for the given element.
        """
        if element not in self.focals:
            return 0
        return self.focals[element]

    ################################################################################

    def __setitem__(self, element, mass):
        """
        Overrides item setting through ``[]``. Sets the mass for the given element.

        Args:
            element (Element): The element to assign mass to.
            mass (float): The mass to assign to the given element.
        """
        self.focals[element] = mass

    ################################################################################

    def __len__(self):
        """
        Overrides ``len()``, gets the number of focal elements in the mass function.

        WARNING: That would count the focals with mass equal to 0, use ``self.clean()``
        first if you want to make sure to get the real number of focal elements.

        Returns:
            int -- The number of focal elements in the mass function.
        """
        return len(self.focals)

################################################################################
################################################################################
################################################################################


