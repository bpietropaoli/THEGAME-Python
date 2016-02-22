#!/usr/bin/python3

################################################################################
# Tutorial.py (for THEGAME - Python version)                                   #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@cit.ie                                          #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module is meant to be used as a short tutorial to learn how to use the  #
# library and that's about it. The philosophy, main operations and vocabulary  #
# are explicit here.                                                           #
# Each function that is not trivial (at least within the theory) should have   #
# a reference pointer in its documentation. I can only advise for you to read  #
# them carefully before using any of those functions.                          #
# ---------------------------------------------------------------------------- #
# This tutorial does not teach the basics of the theory. For this, refer to    #
# the few thousands of publications on the subject. Of course, I can recommend #
# the 3rd chapter of my thesis "B. Pietropaoli, Reconnaissance de Contexte     #
# Stable pour l'Habitat Intelligent, 2013" (French) (An English translation    #
# might be on its way...).                                                     #
################################################################################

# The belief functions theory (also called Dempster-Shafer's theory or theory of
# evidence assigns masses to states defined within a frame of discernment. Let's
# thus start with the definition of "elements" that will be used as focal elements
# within the mass functions.

# The elements are within the module thegame.element.
import thegame.element as element

# It provides two main classes:
#  - Element: An abstract class providing the API of the set-theoretic operations
#             the focal elements must implement in order to be usable within the
#             mass functions.
#  - DiscreteElement: A class to represent discrete focal elements, which corresponds
#                     to the classic theory.

# Let's see how we can build DiscreteElements.
# The discrete elements here are encoded as numbers (for details on how this might
# be done, refer to "A. Martin, Implementing general belief function framework
# with a practical codification for low complexity, 2009").

# The focal elements (which are sets of states) are represented under their binary
# forms using numbers then. If we represent the sets as binary numbers (bigendian),
# then if we have a frame of discernment Omega = {A, B, C}, then we have the fol-
# lowing elements in the powerset:
#  {}          = 000 = 0
#  {A}         = 001 = 1
#  {B}         = 010 = 2
#  {C}         = 100 = 4
#  {A u B}     = 011 = 3
#  {A u C}     = 101 = 5
#  {B u C}     = 110 = 6
#  {A u B u C} = 111 = 7
# The atoms are always the powers of 2.

# Vocabulary:
# -----------
# 1) Frame of discernment = Omega: a set of possible states.
# 2) States: What you're trying to represent inside your mass functions.
# 3) Powerset = 2^Omega: The set of all the subsets of Omega.
# 4) Element: I use this term for elements of the powerset, thus for any subset of
#             Omega, the elements are used as focal elements in mass functions.
# 5) Focal element: an element with mass > 0.

# Let's then create discrete element with our library with the default constructor
# taking two arguments: the size of the frame of discernment, and the number encoding
# an element of the powerset (i.e. a subset of the frame of discernment).
e1 = element.DiscreteElement(3, 0) # => 000
e2 = element.DiscreteElement(3, 5) # => 101

# str() has been overridden to enable printing the elements:
print("First print of elements:")
print(str(e1)) # should print 000
print(str(e2)) # should print 101

# If you find this method a bit difficult and too abstracted, the DiscreteElement class
# provides factory class methods (DiscreteElement.factory_*) to build elements in different
# ways:

# Using a binary string:
e3 = element.DiscreteElement.factory_from_str("101")
e4 = element.DiscreteElement.factory_from_str("011")

# Using a list of references (objects representing your states:
# It takes first a reference list then the "states" that should be included.
e5 = element.DiscreteElement.factory_from_ref_list("abc", "a", "c")
e6 = element.DiscreteElement.factory_from_ref_list("abc", "b", "c")
# The reference list provided can be any ordered iterable of objects.
# Thus, here, we use a string and the characters are the objects.

# Here, e2, e3 and e5 should all be equal:
print("Elements should be equal:")
print(e2 == e3)
print(e2 == e5)

# The elements then provide all the classical set-theoretical operations. All the
# operations that could result in a new element are actually constructing a new
# element. Elements are implemented to be immutable (even though nothing prevents
# you from modifying them, but they are used as keys in mass functions so I would
# not advise modifying them).

# Cardinal: 
card  = e2.cardinal
card2 = len(e2)
# Be careful with this one, it is not computed by default (if it is not trivial).
# It is computed only but the first access can then be a bit slow.

# Opposite:
opp  = e2.opposite()
opp2 = ~e2

# Exclusion:
rest  = e2.exclusion(e4)
rest2 = e2 - e4

# Conjunction/Intersection:
conj  = e2.conjunction(e4)
conj2 = e2.intersection(e4)
conj3 = e2 * e4
conj4 = e2 & e4

# Disjunction/Union:
disj  = e2.disjunction(e4)
disj2 = e2.union(e4)
disj3 = e2 + e4
disj4 = e2 | e4

# Emptiness check:
e2.is_empty()

# Completeness check:
e2.is_complete()

# Finally, if you have a reference list for your elements, you can get formatted
# strings to represent your elements:
print("Element formatted strings:")
print(conj.formatted_str(*"abc"))
print(disj.formatted_str(*"abc"))

# The DiscreteElement class provides some static utility methods.

# Access the empty and the complete set:
empty_set    = element.DiscreteElement.get_empty_element(3)
complete_set = element.DiscreteElement.get_complete_element(3)

# Iterate over elements:
for e in element.DiscreteElement.iterator_powerset(3):
    pass

for e in element.DiscreteElement.iterator_atomic(5):
    pass


################################################################################
################################################################################
################################################################################

# The mass functions are provided by thegame.massfunction
import thegame.massfunction as massfunction

# Focal elements are passed as tuples composed of an element and a mass.
# Let's build some elements first.

e0 = element.DiscreteElement(3, 0)
e1 = element.DiscreteElement(3, 1)
e2 = element.DiscreteElement(3, 2)
e3 = element.DiscreteElement(3, 3)
e4 = element.DiscreteElement(3, 4)
e5 = element.DiscreteElement(3, 5)
e6 = element.DiscreteElement(3, 6)
e7 = element.DiscreteElement(3, 7)

# You can create mass functions directly:
m1 = massfunction.MassFunction((e2, 0.4), (e4, 0.3), (e5, 0.3))
m2 = massfunction.MassFunction((e1, 0.8), (e7, 0.2))

# They do not have to be normalised nor contain "valid" values:
m3 = massfunction.MassFunction((e2, 2), (e3, -0.3), (e5, 0.1))

# They can also be constructed by adding mass sequentially.
m4 = massfunction.MassFunction()
m4.add_mass((e2, 0.4))
m4.add_mass((e4, 0.4))
m4.add_mass((e3, 0.2))
m4.add_mass((e7, 0))

# The mass functions are handling only focal elements to save computation time.
# To make sure that it really contains only focal elements, you can call the
# method clean().
m4.clean() # Gets rid of e7 here.

# To clean mass functions, it considers that anything with a mass lower than
# 0.000001 should be removed. You should thus not use clean() on mass functions
# containing negative values (for instance the result of a difference()).

# You can also normalise mass functions if necessary. For instance, if you had build
# mass functions using integers.
m3.clean()
m3.normalise()
# Those methods modify the mass function.


# Then, the MassFunction class implements many classical methods you could find in
# the literature. Most methods, like for elements, do not modify the mass function
# on which they are applied. Instead, they return a new mass function. It prevents
# destroying data.

# Combination rules: (You can combine any number of mass functions.)
m1.combination_dempster(m2, m3)
m1.combination_smets(m2, m3, m4) 
m1.combination_disjunctive(m2)
m1.combination_yager(m3, m2)
m1.combination_dubois_prade(m2)
m1.combination_average(m2, m3, m4)
m1.combination_murphy(m2, m3, m4)
m1.combination_chen(m2, m3, m4)

# Some characteristics:
m1.specificity()
m1.discrepancy()
m1.non_specificity()

# Discounting:
m1.discounting(0.2)

# Conditioning:
m1.conditioning(e6)

# Belief:
m1.belief(e3)
m1.bel(e3)

# Pignistic transformation:
m1.pignistic_transformation(e3)
m1.betP(e3)

# Plausibility:
m1.plausibility(e3)
m1.pl(e3)

# Commonality:
m1.commonality(e3)
m1.q(e3)

# Decision making support:
massfunction.MassFunction.get_max(m1.bel, 2, element.DiscreteElement.iterator_powerset(3)) # Using the iterators provided in DiscreteElement
massfunction.MassFunction.get_min(m1.pl,  2, element.DiscreteElement.iterator_atomic(3))

# The mass functions works more or less like dictionaries.
# You can get/set masses using []:
m1[e3]
m1[e3] = 0.5 # Of course, this does modify the mass function.

# And they are iterable:
for focal_element in m1:
    pass

for focal_element, mass in m1.items():
    pass

# And finally, mass functions can be printed in the console in an easy to read format:
print("Printing mass functions:")
print(m1)
print(m2)






