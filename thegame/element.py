################################################################################
# thegame.element.py                                                           #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@cit.ie                                          #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module contains all the classes to manage focal elements within the     #
# belief functions theory. It provides the set-theoretic operations needed for #
# the theory of evidence to be applied.                                        #
# As a reminder, focal elements are sets of possible states defined within a   #
# frame of discernment. That's why the operations provided here are in fact    #
# set-theoretic operations.                                                    #
# ---------------------------------------------------------------------------- #
# Main classes:                                                                #
#   - Element: Abstract class providing the API for elements to use within the #
#     belief functions theory.                                                 #
#   - DiscreteElement: A class providing elements defined on finite and dis-   #
#     crete frames of discernment; this is the classic belief functions theory.#
################################################################################

import re
import math
import functools
from abc import ABCMeta, abstractmethod

##############
# DECORATORS #
##############

def check_elements_compatibility(function):
    """
    Decorator that checks that all the elements provided to 'function' are
    compatible with each others.

    Args:
        function (func.): A set-theoretic function that takes elements as
            arguments.
    Returns:
        function result -- The result of the provided function.
    Raises:
        IncompatibleElementsError: If the elements provided to decorated
        function are not compatible with each others.
    """
    @functools.wraps(function)
    def wrapped_function(*args):
        for i in range(len(args)):
            for j in range(len(args)):
                if not args[i].is_compatible(args[j]):
                    raise IncompatibleElementsError(args[i], args[j])
        return function(*args)
    return wrapped_function


################################################################################
################################################################################
################################################################################


##############
# EXCEPTIONS #
##############

class ElementError(Exception):
    """Raised when an error occurs in this module."""
    pass


class IncompatibleElementsError(ElementError):
    """
    Raised when trying to perform an operation on elements that requires
    them to be compatible such as disjunction/conjunction.

    Attributes:
        e1: The first element of the incompatibility.
        e2: The second element of the incompatibility.
    """
    
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return (
            "An operation on two incompatible elements has been attempted:\n" +
            " - First element : " + str(self.e1) + "\n" +
            " - Second element: " + str(self.e2)
        )


class IncompatibleSizeAndNumberError(ElementError):
    """
    Raised when trying to construct a discrete element and the given
    encoding number and the size of the frame of discernment are incompatible.
    
    Typical cases:
        number < 0: This is a non-sense.
        number > 2^size - 1: The given number is too big for the given size.

    Attributes:
        size: The size of the frame of discernment that was provided.
        number: The number encoding the element that caused an error.
    """
    
    def __init__(self, size, number):
        self.size = size
        self.number = number

    def __str__(self):
        return (
            "An element with incompatible size and number encoding was tried to be constructed.\n" +
            " - size = " + str(self.size) + "\n" +
            " - number = " + str(self.number) + "\n" +
            "The following inequality should be respected: 0 <= number < 2^size - 1."
        )


class IncompatibleReferencesError(ElementError):
    """
    Raised when trying to use DiscreteElement.format_str() with a list of
    references that does not seem to correspond to the element to which it
    is applied.

    Attributes:
        element: The element for which format was called.
        references: The list of strings to use as references.
    """

    def __init__(self, element, references):
        self.element = element
        self.references = references

    def __str__(self):
        return (
            "Impossible to format a string to represent the element with the given references list.\n" +
            " - Element = " + str(self.element) + " (size: " + str(self.element._size) + ")\n" +
            " - References = " + str(self.references) + " (size: " + str(len(self.references)) + ")\n" +
            "Both, the element and the references list, should be of the same size."
        )

################################################################################
################################################################################
################################################################################


####################
# ABSTRACT ELEMENT #
####################

class Element(metaclass=ABCMeta):
    """
    Abstract class to represent elements used in focal elements.

    Provides the API to implement elements that can be used into mass functions.
    The idea here is to never modify an existing element. Thus, every method
    returns a new element without modifying the one on which methods are called.
    You should respect this as the elements are used as keys in a dictionary in
    the module massfunction. If you modify them, it will thus mess up the hashes.

    I know having an abstract class is not very Pythonic as duck typing is often
    preferred. In fact, you can use duck typing in THEGAME without getting into
    any trouble. It is just that here, this abstract class provides the complete
    API and also operator overrides, etc. So, if you use it, you're sure that all
    the mass functions methods will work.

    Properties:
        cardinal (int): The cardinal of the element. For consistency, this should
            not implement a setter.
    """

    @property
    @abstractmethod
    def cardinal(self):
        """
        Gets the cardinal of the current element (the number
        of possible states it is composed of).

        Returns:
            int -- The cardinal of the element.
        """
        pass

    @abstractmethod
    def opposite(self):
        """
        Gets the opposite of the current element.

        Returns:
            Element -- A new element which is the opposite
            of the current one.
        """
        pass

    def exclusion(self, element):
        """
        Gets the element resulting from the exclusion of the given one
        from the current one (i.e. self \ element).

        This is equivalent to ``self.conjunction(element.opposite())``.

        Args:
            element (Element): The element to exclude from the current one.
        Returns:
            Element -- A new element that is the result of excluding the
            given one from the current one.
        """
        return self.conjunction(element.opposite())

    def exclusion_unsafe(self, element):
        """
        Gets the element resulting from the exclusion of the given one
        from the current one (i.e. self \ element).

        This is equivalent to ``self.conjunction(element.opposite())``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            element (Element): The element to exclude from the current one.
        Returns:
            Element -- A new element that is the result of excluding the
            given one from the current one.
        """
        return self.conjunction_unsafe(element.opposite())

    @abstractmethod
    @check_elements_compatibility
    def conjunction(self, element):
        """
        Gets the conjunction/intersection of the current element with the
        given one.

        Equivalent to ``self.intersection(element)``.

        Args:
            element (Element): The element with which conjunction/intersection
                is requested.
        Returns:
            Element -- A new element which is the conjunction/intersection
            of the current element with the given one.
        Raises:
            IncompatibleElementsError: If the current element and the given
            one are not compatible.
        """
        pass

    @abstractmethod
    def conjunction_unsafe(self, element):
        """
        Gets the conjunction/intersection of the current element with the
        given one.

        Equivalent to ``self.intersection_unsafe(element)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.

        Args:
            element (Element): The element with which conjunction/intersection
                is requested.
        Returns:
            Element -- A new element which is the conjunction/intersection
            of the current element with the given one.
        """
        pass

    def intersection(self, element):
        """
        Gets the conjunction/intersection of the current element with the
        given one.

        Equivalent to ``self.conjunction(element)``.

        Args:
            element (Element): The element with which conjunction/intersection
                is requested.
        Returns:
            Element -- A new element which is the conjunction/intersection
            of the current element with the given one.
        Raises:
            IncompatibleElementsError: If the current element and the given
            one are not compatible.
        """
        return self.conjunction(element)

    def intersection_unsafe(self, element):
        """
        Gets the conjunction/intersection of the current element with the
        given one.

        Equivalent to ``self.conjunction_unsafe(element)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.

        Args:
            element (Element): The element with which conjunction/intersection
                is requested.
        Returns:
            Element -- A new element which is the conjunction/intersection
            of the current element with the given one.
        """
        return self.conjunction_unsafe(element)

    @abstractmethod
    @check_elements_compatibility
    def disjunction(self, element):
        """
        Gets the disjunction/union of the current element with the
        given one.

        Equivalent to ``self.union(element)``.

        Args:
            element (Element): The element with which disjunction/union
                is requested.
        Returns:
            Element -- A new element which is the disjunction/union
            of the current element with the given one.
        Raises:
            IncompatibleElementsError: If the current element and the given
            one are not compatible.
        """
        pass

    @abstractmethod
    def disjunction_unsafe(self, element):
        """
        Gets the disjunction/union of the current element with the
        given one.

        Equivalent to ``self.union_unsafe(element)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.

        Args:
            element (Element): The element with which disjunction/union
                is requested.
        Returns:
            Element -- A new element which is the disjunction/union
            of the current element with the given one.
        """
        pass

    def union(self, element):
        """
        Gets the disjunction/union of the current element with the
        given one.

        Equivalent to ``self.disjunction(element)``.

        Args:
            element (Element): The element with which disjunction/union
                is requested.
        Returns:
            Element -- A new element which is the disjunction/union
            of the current element with the given one.
        Raises:
            IncompatibleElementsError: If the current element and the given
            one are not compatible.
        """
        return self.disjunction(element)

    def union_unsafe(self, element):
        """
        Gets the disjunction/union of the current element with the
        given one.

        Equivalent to ``self.disjunction_unsafe(element)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.

        Args:
            element (Element): The element with which disjunction/union
                is requested.
        Returns:
            Element -- A new element which is the disjunction/union
            of the current element with the given one.
        """
        return self.disjunction_unsafe(element)

    @abstractmethod
    def get_empty_element(self):
        """
        Gets the empty element compatible with the current element.

        Returns:
            Element -- A new element, which is empty and compatible
            with the current element.
        """
        pass

    @abstractmethod
    def get_complete_element(self):
        """
        Gets the complete set as an element compatible with the current
        one.

        Returns:
            Element -- A new element, which is the complete set of stats
            and compatible with the current element.
        """
        pass

    def is_subset(self, element):
        """
        Checks if the current element is a subset of the given one.

        Args:
            element (Element): The element to check subsetness with.
        Returns:
            bool -- ``True`` if the current element is a subset of the
            given one, ``False`` otherwise.
        """
        if not self.is_compatible(element):
            return False

        return self.conjunction_unsafe(element) == self

    def is_superset(self, element):
        """
        Checks if the current element is a superset of the given one.

        Args:
            element (Element): The element to check supersetness with.
        Returns:
            bool -- ``True`` if the current element is a superset of the
            given one, ``False`` otherwise.
        """
        return element.is_subset(self)

    @abstractmethod
    def is_empty(self):
        """
        Checks if the current element is the empty set.

        Returns:
            bool -- ``True`` if the current element is empty,
            ``False`` otherwise.
        """
        pass

    @abstractmethod
    def is_complete(self):
        """
        Checks if the current element corresponds to the complete set.

        Returns:
            bool -- ``True`` if the current element corresponds to the
            complete set, ``False`` otherwise.
        """
        pass

    @abstractmethod
    def is_compatible(self, element):
        """
        Checks if the current element and the given one are compatible
        (to perform set-theoretic operations) or not.

        Args:
            element (Element): The element to check compatibility with.
        Returns:
            bool -- ``True`` if both elements are compatible, ``False``
            otherwise.
        """
        pass

    @abstractmethod
    def equals(self, element):
        """
        Checks if the current element and the given one are equal.

        Args:
            element (Element): The element to compare to.
        Returns:
            bool -- ``True`` if both elements are equal, ``False``
            otherwise.
        """
        pass

    # **********************
    # Overiding operators:
    # **********************

    @abstractmethod
    def __hash__(self):
        """
        Overrides ``hash()``, necessary to enable elements being used
        as dictionary keys.

        Returns:
            int -- The hash code of the current element.
        """
        pass

    def __eq__(self, element):
        """
        Overrides ``==``, compares self with the given element.

        Equivalent to ``self.equals(element)``.
        
        Args:
            element (Element): The element to compare to.
        Returns:
            bool -- ``True`` if both are equal, ``False`` otherwise.
        """
        return self.equals(element)

    def __add__(self, element):
        """
        Overrides ``+``, performs a disjunction of self with the given element.

        Equivalent to ``self.disjunction(element)`` and to ``self.union(element)``.
        
        Args:
            element (Element): The element to do the union with.
        Returns:
            Element -- A new ``Element`` that is the disjunction/union of
            self with the given element.
        """
        return self.disjunction(element)

    def __sub__(self, element):
        """
        Overrides ``-``, performs the exclusion of the given element from self.

        Equivalent to ``self.exclusion(element)``.

        Args:
            element (Element): The element to exclude from the current one.
        Returns:
            Element -- A new ``Element`` that is the current one excluded the
            given one.
        """
        return self.exclusion(element)

    def __mul__(self, element):
        """
        Overrides ``*``, performs a conjunction of self with the given element.

        Equivalent to ``self.conjunction(element)`` and to ``self.intersection(element)``.
        
        Args:
            element (Element): The element to do the intersection with.
        Returns:
            Element -- A new ``Element`` that is the conjunction/intersection of
            self with the given element.
        """
        return self.conjunction(element)

    def __or__(self, element):
        """
        Overrides ``|``, performs a disjunction of self with the given element.

        Equivalent to ``self.disjunction(element)`` and to ``self.union(element)``.
        
        Args:
            element (Element): The element to do the union with.
        Returns:
            Element -- A new ``Element`` that is the disjunction/union of
            self with the given element.
        """
        return self.disjunction(element)

    def __and__(self, element):
        """
        Overrides ``&``, performs a conjunction of self with the given element.

        Equivalent to ``self.conjunction(element)`` and to ``self.intersection(element)``.
        
        Args:
            element (Element): The element to do the intersection with.
        Returns:
            Element -- A new ``Element`` that is the conjunction/intersection of
            self with the given element.
        """
        return self.conjunction(element)

    def __invert__(self):
        """
        Overrides ``~``, gives the opposite of the current element.

        Equivalent to ``self.opposite()``.

        Returns:
            Element -- A new ``Element`` that is the opposite of the current
            one.
        """
        return self.opposite()

    def __len__(self):
        """
        Overrides ``len()``, gives the length of the element, or more simply
        its cardinal.

        Returns:
            int -- The cardinal of the element.
        """
        return self.cardinal

    # **************
    # Class methods:
    # **************

    @classmethod
    def compatible_elements(*elements):
        """
        Checks that all the given elements are compatible with each others.

        Args:
            *elements (Elements): An iterable of elements to check.
        Returns:
            bool -- ``True`` if all the provided elements are compatible
            with each others, ``False`` otherwise.
        """
        for e1 in elements:
            for e2 in elements:
                if not e1.is_compatible(e2):
                    return False
        return True

    @staticmethod
    @check_elements_compatibility
    def static_conjunction(*elements):
        """
        Gets the conjunction/intersection of all the provided elements.

        Equivalent to ``Element.static_intersection(*elements)``.

        Args:
            elements (*Element): Elements for which the conjunction is requested.
        Returns:
            Element -- A new element corresponding to the conjunction of all the
            provided ones.
        Raises:
            IncompatibleElementsError: If two or more of the provided elements
            are incompatible with each others.
        """
        conj = elements[0]
        for e in elements[1:]:
            conj = conj.conjunction(e)
        return conj

    @staticmethod
    def static_conjunction_unsafe(*elements):
        """
        Gets the conjunction/intersection of all the provided elements.

        Equivalent to ``Element.static_intersection_unsafe(*elements)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.

        Args:
            elements (*Element): Elements for which the conjunction is requested.
        Returns:
            Element -- A new element corresponding to the conjunction of all the
            provided ones.
        """
        conj = elements[0]
        for e in elements[1:]:
            conj = conj.conjunction_unsafe(e)
        return conj

    @staticmethod
    def static_intersection(*elements):
        """
        Gets the conjunction/intersection of all the provided elements.

        Equivalent to ``Element.static_conjunction(*elements)``.

        Args:
            elements (*Element): Elements for which the conjunction is requested.
        Returns:
            Element -- A new element corresponding to the conjunction of all the
            provided ones.
        Raises:
            IncompatibleElementsError: If two or more of the provided elements
            are incompatible with each others.
        """
        return Element.static_conjunction(*elements)

    @staticmethod
    def static_intersection_unsafe(*elements):
        """
        Gets the conjunction/intersection of all the provided elements.

        Equivalent to ``Element.static_conjunction(*elements)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            elements (*Element): Elements for which the conjunction is requested.
        Returns:
            Element -- A new element corresponding to the conjunction of all the
            provided ones.
        Raises:
            IncompatibleElementsError: If two or more of the provided elements
            are incompatible with each others.
        """
        return Element.static_conjunction_unsafe(*elements)

    @staticmethod
    @check_elements_compatibility
    def static_disjunction(*elements):
        """
        Gets the disjunction/union of all the provided elements.

        Equivalent to ``Element.static_union(*elements)``.

        Args:
            elements (*Element): Elements for which the disjunction is requested.
        Returns:
            Element -- A new element corresponding to the disjunction of all the
            provided ones.
        Raises:
            IncompatibleElementsError: If two or more of the provided elements
            are incompatible with each others.
        """
        disj = elements[0]
        for e in elements[1:]:
            disj = disj.disjunction(e)
        return disj

    @staticmethod
    def static_disjunction_unsafe(*elements):
        """
        Gets the disjunction/union of all the provided elements.

        Equivalent to ``Element.static_union_unsafe(*elements)``.
    
        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            elements (*Element): Elements for which the disjunction is requested.
        Returns:
            Element -- A new element corresponding to the disjunction of all the
            provided ones.
        Raises:
            IncompatibleElementsError: If two or more of the provided elements
            are incompatible with each others.
        """
        disj = elements[0]
        for e in elements[1:]:
            disj = disj.disjunction_unsafe(e)
        return disj

    @staticmethod
    def static_union(*elements):
        """
        Gets the disjunction/union of all the provided elements.

        Equivalent to ``Element.static_disjunction(*elements)``.

        Args:
            elements (*Element): Elements for which the disjunction is requested.
        Returns:
            Element -- A new element corresponding to the disjunction of all the
            provided ones.
        Raises:
            IncompatibleElementsError: If two or more of the provided elements
            are incompatible with each others.
        """
        return Element.static_disjunction(*elements)

    @staticmethod
    def static_union_unsafe(*elements):
        """
        Gets the disjunction/union of all the provided elements.

        Equivalent to ``Element.static_disjunction_unsafe(*elements)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.
        
        Args:
            elements (*Element): Elements for which the disjunction is requested.
        Returns:
            Element -- A new element corresponding to the disjunction of all the
            provided ones.
        Raises:
            IncompatibleElementsError: If two or more of the provided elements
            are incompatible with each others.
        """
        return Element.static_disjunction_unsafe(*elements)

################################################################################
################################################################################
################################################################################


#################################
# DISCRETE ELEMENT: CLASSIC BFT #
#################################

class DiscreteElement(Element):
    """
    Discrete elements for classical belief functions using a finite frame of
    discernment.

    The focal elements are encoded as numbers corresponding, in their binary form
    to the set they represent. This is optimised for usual set-theoretic operations
    such as conjunctions and disjunctions.
    The methods never modify the element, attributes should thus not be modified manually
    even though you're free to do it. It might create weird behaviours though.

    The class provides methods marked as "unsafe". Those methods do not check the validity
    of the created element or of the performed operations but they are generally faster than
    their safe equivalent (this is particularly noticeable for very big elements, i.e. > 1000
    possible states).

    Attributes:
        _card: An integer providing the cardinal of the focal element. It is initialised
            at -1 as it takes time to compute and is not always needed. Should be accessed
            through ``self.cardinal`` if you don't want to handle the -1 yourself.
        _size: An integer corresponding to the size of the frame of discernment on which the
            element is defined.
        _number: An integer encoding the states present in the element.

    Properties:
        cardinal (int): The cardinal of the element. For consistency, this property does not
            have a setter.
        size (int): The size of the frame of discernement on which the element is defined. This
            property does not have a setter.
    """

    # *************
    # Constructors:
    # *************
    
    def __init__(self, size, number=0):
        """
        Constructs a discrete element defined in a frame of discernement of
        the given size.

        Args:
            size (int): The size of the frame of discernement.
            number (int): The number encoding the element (default: 0).
        Raises:
            ValueError: If size <= 0 (a negative number of possible states
                makes no sense), or if number < 0 because it wouldn't encode
                for anything that makes sense.
            
        """
        #Exception management:
        if size <= 0:
            raise ValueError(
                "size: " + str(size) + "\n" +
                "The size of the frame of discernment cannot be null nor negative, " +
                "it makes no sense."
            )
        
        #Trivial case (to save computation time):
        if number == 0:
            self._card = 0
            self._size = size
            self._number = 0
            return

        #The other trivial case:
        power = 1 << size
        if number == power - 1:
            self._card = size
            self._size = size
            self._number = number
            return
            
        if not (0 <= number < power):
            raise IncompatibleSizeAndNumberError(size, number)

        #Attributes initialisation:
        self._card   = -1
        self._size   = size
        self._number = number

    ################################################################################

    @classmethod
    def factory_constructor_unsafe(cls, size, number=0):
        """
        Constructs a discrete element defined in a frame of discernement of
        the given size. Slightly faster that the safe constructor but does
        not initialise the cardinal.

        WARNING: It does not check the validity of the created element. It
        might raise exceptions later if you messed it up.

        Args:
            size (int): The size of the frame of discernement.
            number (int): The number encoding the element (default: 0).
        Returns:
            Element -- A new element of the given size corresponding to
            the provided number (may be invalid!).
        """
        result = cls(size)
        result._number = number
        result._card = -1
        return result

    ################################################################################

    @classmethod
    def factory_from_ref_list(cls, ref_list, *states):
        """
        Construcs a discrete element from a reference list of objects describing the
        states and a given list of states to include in the element.
        
        Remark 0: The cardinal is put to its real value directly with this constructor.
        Remark 1: The state list can contain multiple times the same value, it won't affect
            the construction of the element.
        Remark 2: The provided object need to support ``==`` or to really be equal.

        Args:
            ref_list (ordered iter[object]): An ordered iterable of possible states for the
                frame of discernment (the states can be anything!).
            states (*object): The states to include in the element.
        Returns:
            DiscreteElement -- A new element containing all the given states.
        Raises:
            ValueError: If one of the states is not contained in the ref_list or if the ref_list
            contains multiple times the same value.
        """
        for i in range(len(ref_list)):
            for j in range(len(ref_list)):
                if i != j and ref_list[i] == ref_list[j]:
                    raise ValueError(
                        "ref_list: " + str(ref_list) + "\n" +
                        "A reference list cannot contain multiple times the same state!"
                    )

        st = set(states)
        for state in st:
            if state not in ref_list:
                raise ValueError(
                    "states: " + str(state) + "\n" +
                    "The given state does not correspond to the given reference list " +
                    str(ref_list) + "!"
                )

        return DiscreteElement.factory_from_ref_list_unsafe(ref_list, *states)

    ################################################################################

    @classmethod
    def factory_from_ref_list_unsafe(cls, ref_list, *states):
        """
        Construcs a discrete element from a reference list of objects describing the
        states and a given list of states to include in the element.
        
        Remark 0: The cardinal is put to its real value directly with this constructor.
        Remark 1: The state list can contain multiple times the same value, it won't affect
            the construction of the element.
        Remark 2: The provided object need to support ``==`` or to really be equal.

        WARNING: This does not check the validity of the provided lists. This might
        create unexpected behaviour.

        Args:
            ref_list (ordered iter[object]): An ordered iterable of possible states for the
                frame of discernment (the states can be anything!).
            states (*object): The states to include in the element.
        Returns:
            DiscreteElement -- A new element containing all the given states.
        """
        st = set(states)
        result = cls(len(ref_list))
        result._card = len(st)
        for state in st:
            i = ref_list.index(state)
            result._number += 1 << i
            
        return result
    
    ################################################################################

    @classmethod
    def factory_from_str(cls, bstr, bigendian=True):
        """
        Constructs a discrete element equivalent to the given binary string (a string
        containing only 0s and 1s. The size of the frame of discernement is given by
        the length of the string. The string might thus contain extra 0s to make it
        to the wanted length.
        
        Remark: The cardinal is put to its real value with this constructor.
        
        Args:
            bstr (str): The binary string used to encode an element, must be made
                only of 0s and 1s.
            bigendian (bool): A boolean to indicate if the given binary string must
                be read as big endian or little endian.
        Returns:
            Element -- A new element corresponding to the provided binary string.
        Raises:
            ValueError: If the given string is not composed only of 0s and 1s.
        """
        
        #Exception management:
        if not re.compile(r'^[0-1]+$').search(bstr):
            raise ValueError(
                "bstr: " + bstr + "\n" +
                "The given string should be made only of 0s and 1s."
            )
        return DiscreteElement.factory_from_str_unsafe(bstr, bigendian)

    ################################################################################

    @classmethod
    def factory_from_str_unsafe(cls, bstr, bigendian=True):
        """
        Constructs a discrete element equivalent to the given binary string (a string
        containing only 0s and 1s. The size of the frame of discernement is given by
        the length of the string. The string might thus contain extra 0s to make it
        to the wanted length.

        Remark: The cardinal is put to its real value with this constructor.
        
        WARNING: This does not check the validity of the provided string. This might
        create unexpected behaviour.

        Args:
            bstr (str): The binary string used to encode an element, must be made
                only of 0s and 1s.
            bigendian (bool): A boolean to indicate if the given binary string must
                be read as big endian or little endian.
        Returns:
            Element -- A new element corresponding to the provided binary string.
        Raises:
            ValueError: If the given string is not composed only of 0s and 1s.
        """
        size = len(bstr)   
        result = cls(size)
        result._card = -1

        #Trivial cases:
        if '1' not in bstr:
            result._card = 0
            result._number = 0
            result._size = size
            return result

        if '0' not in bstr:
            result._card = size
            result._number = (1 << size) - 1
            result._size = size
            return result

        result._card = bstr.count('1')
        
        if bigendian:
            result._number = int(bstr, 2)
        else:
            result._number = int(bstr[::-1], 2) #Reverse string
        return result

    ################################################################################
    ################################################################################
    ################################################################################

    # ***********
    # Properties:
    # ***********

    @property
    def cardinal(self):
        """
        Gets the cardinal of the current element (the number
        of possible states it is composed of).

        Returns:
            int -- The cardinal of the element.
        """
        if self._card != -1:
            return self._card

        self._card = 0
        n = self._number
        while n != 0:
            if n & 1 == 1:
                self._card += 1
            n >>= 1
            
        return self._card

    ################################################################################
    
    @property
    def size(self):
        """
        Gets the size of the frame of discernment on which the element is defined.

        Returns:
            int -- The size of the frame of discernment on which the element
            is defined.
        """
        return self._size

    ################################################################################
    ################################################################################
    ################################################################################
    
    # **********************
    # Set-theoretic methods:
    # **********************
    
    def opposite(self):
        """
        Gets the opposite of the current element.

        Returns:
            Element -- A new element which is the opposite
            of the current one.
        """
        result = DiscreteElement(self._size, (1 << self._size) - 1 - self._number)
        if self._card != -1:
            result.card = self._size - self._card
        return result
    
    ################################################################################

    @check_elements_compatibility
    def conjunction(self, element):
        """
        Gets the conjunction/intersection of the current element with the
        given one.

        Equivalent to ``self.intersection(element)``.

        Args:
            element (Element): The element with which conjunction/intersection
                is requested.
        Returns:
            Element -- A new element which is the conjunction/intersection
            of the current element with the given one.
        Raises:
            IncompatibleElementsError: If the current element and the given
            one are not compatible (typically, there not defined on the same
            frame of discernment, with exceptions for the complete set and the
            empty set).
        """
        return DiscreteElement(self._size, self._number & element._number)
    
    ################################################################################

    def conjunction_unsafe(self, element):
        """
        Gets the conjunction/intersection of the current element with the
        given one.

        Equivalent to ``self.intersection_unsafe(element)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.

        Args:
            element (Element): The element with which conjunction/intersection
                is requested.
        Returns:
            Element -- A new element which is the conjunction/intersection
            of the current element with the given one.
        """
        return DiscreteElement.factory_constructor_unsafe(self._size,
                                                          self._number & element._number)

    ################################################################################

    @check_elements_compatibility
    def disjunction(self, element):
        """
        Gets the disjunction/union of the current element with the
        given one.

        Equivalent to ``self.union(element)``.

        Args:
            element (Element): The element with which disjunction/union
                is requested.
        Returns:
            Element -- A new element which is the disjunction/union
            of the current element with the given one.
        Raises:
            IncompatibleElementsError: If the current element and the given
            one are not compatible (typically, there not defined on the same
            frame of discernment, with exceptions for the complete set and the
            empty set).
        """
        return DiscreteElement(self._size, self._number | element._number)

    ################################################################################

    def disjunction_unsafe(self, element):
        """
        Gets the disjunction/union of the current element with the
        given one.

        Equivalent to ``self.union_unsafe(element)``.

        WARNING: Does not check elements compatibility. This might create
        unexpected behaviour.

        Args:
            element (Element): The element with which disjunction/union
                is requested.
        Returns:
            Element -- A new element which is the disjunction/union
            of the current element with the given one.
        """
        return DiscreteElement.factory_constructor_unsafe(self._size,
                                                          self._number | element._number)

    ################################################################################

    def get_compatible_empty_element(self):
        """
        Gets the empty element compatible with the current element.

        Returns:
            Element -- A new element, which is empty and compatible
            with the current element.
        """
        return DiscreteElement.get_empty_element(self._size)

    ################################################################################

    def get_compatible_complete_element(self):
        """
        Gets the complete set as an element compatible with the current
        one.

        Returns:
            Element -- A new element, which is the complete set of stats
            and compatible with the current element.
        """
        return DiscreteElement.get_complete_element(self._size)

    ################################################################################

    def is_empty(self):
        """
        Checks if the current element is the empty set.

        Returns:
            bool -- ``True`` if the current element is empty,
            ``False`` otherwise.
        """
        return self._number == 0

    ################################################################################

    def is_complete(self):
        """
        Checks if the current element corresponds to the complete set.

        Returns:
            bool -- ``True`` if the current element corresponds to the
            complete set, ``False`` otherwise.
        """
        return self._number == (1 << self._size) - 1
        
    ################################################################################
    ################################################################################
    ################################################################################

    # ****************
    # Utility methods:
    # ****************

    def is_compatible(self, element):
        """
        Checks if the current element and the given one are compatible
        (to perform set-theoretic operations) or not.

        Args:
            element (Element): The element to check compatibility with.
        Returns:
            bool -- ``True`` if both elements are compatible, ``False``
            otherwise.
        """
        if not isinstance(element, DiscreteElement):
            return False
        return self._size == element._size

    ################################################################################

    def equals(self, element):
        """
        Checks if the current element and the given one are equal.

        Args:
            element (Element): The element to compare to.
        Returns:
            bool -- ``True`` if both elements are equal, ``False``
            otherwise.
        """
        if not self.is_compatible(element):
            return False

        return self._number == element._number

    ################################################################################

    def formatted_str(self, *references):
        """
        Provides a formatted string representing the element given a list of references.
        References should be given in the order corresponding to the small-endianness
        (the first reference is the first bit).

        Args:
            references (*object): A list of objects representing the "real" states (they
                should support ``==`` and ``str()``).
        Returns:
            str -- Returns a string under the form `{state1 u state2 u ...}`.
        Raises:
            ValueError: If the reference list contains multiple times the same reference.
            IncompatibleReferencesError: If the reference list seems to be incompatible
            with the current element (typically if they differ in size).
        """
        if self._size != len(references):
            raise IncompatibleReferencesError(self, references)

        for i in range(len(references)):
            for j in range(len(references)):
                if i != j and references[i] == references[j]:
                    raise ValueError(
                        "references: " + str(references) + "\n" +
                        "The list of references should not contain duplicates!"
                    )

        result = ""
        first = True
        
        n = self._number
        i = 0
        while n != 0:
            if n & 1 == 1:
                if first:
                    result = str(references[i])
                    first = False
                else:
                    result += " u " + str(references[i])
            n >>= 1
            i += 1
            
        return "{" + result + "}"

    ################################################################################

    # ******************************
    # Overriding built-in functions:
    # ******************************

    def __hash__(self):
        """
        Overrides ``hash()``, necessary to enable elements being used
        as dictionary keys.

        WARNING: DiscreteElements with different sizes but the same
        value will have the same hash. Anyway, you shouldn't mix them
        within the same dictionary, so it should be fine, but you're
        warned.

        Returns:
            int -- The hash code of the current element.
        """
        return self._number

    ################################################################################
    
    def __str__(self):
        """
        Overrides ``str()``. Gives a string representation of the current element under the
        form of a binary string (big endian).
        Can be used to create elements with ``factory_from_str(str(element), bigendian=True)``.

        Returns:
            str -- Returns a binary string representing the current element.
        """
        b = bin(self._number)[2:]
        return "0" * (self._size - len(b)) + b #To add the missing 0s.

    ################################################################################
    ################################################################################
    ################################################################################

    # **************
    # Class methods:
    # **************

    @staticmethod
    def get_empty_element(size):
        """
        Provides the empty element of the given size.

        Args:
            size (int): The size of the frame of discernment on which the element
                should be defined.
        Returns:
            DiscreteElement -- A new element that is the empty set.
        """
        return DiscreteElement(size)

    ################################################################################

    @staticmethod
    def get_complete_element(size):
        """
        Provides the complete element of the given size.

        Args:
            size (int): The size of the frame of discernment on which the element
                should be defined.
        Returns:
            DiscreteElement -- A new element that is the complete set.
        """
        return DiscreteElement(size, (1 << size) - 1)

    ################################################################################

    @staticmethod
    def iterator_powerset(size):
        """
        An iterator that provides all the DiscreteElements of the given size.
        Prevents building a huge set of elements and builds it on the fly instead.
        This corresponds to an iteration over the powerset.
        WARNING: IT CAN HARM YOUR POOR COMPUTER IF USED WITH AN UNREASONABLY BIG SIZE.

        Args:
            size (int): The size of the frame of discernment for the discrete elements.
        Returns:
            DiscreteElements (iterable): An iteration on the powerset of discrete elements.
        """
        for i in range(1 << size):
            yield DiscreteElement(size, i)

    ################################################################################

    @staticmethod
    def iterator_atomic(size):
        """
        An iterator that provides all the atomic DiscreteElements of the given size.
        Prevents building a huge set of elements and builds it on the fly instead.

        Args:
            size (int): The size of the frame of discernment for the discrete elements.
        Returns:
            DiscreteElements (iterable): An iteration on atomic discrete elements.
        """
        for i in range(size):
            yield DiscreteElement(size, 1 << i)

################################################################################
################################################################################
################################################################################


