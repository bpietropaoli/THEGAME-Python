#!/usr/bin/python

################################################################################
# thegame.benchmark_element.py                                                 #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@cit.ie                                          #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module runs benchmarks for the element classes. This is a good way to   #
# understand what might take most of the computation time in your code.        #
################################################################################


if __name__ == '__main__':
    #Gory imports, honestly, who cares?
    import sys
    import os
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from thegame.element import *
    from benchmark_utility import *
    
    print(
        "*" * 80 + "\n" +
        "*" + "{:^78}".format(os.path.basename(__file__)) + "*\n" +
        "*" * 80
    )

    nb_iterations = 10000
    timeout = 60

    f = open("Results - element.txt", "w")
    f.write(
        "*" * 80 + "\n" +
        "*" + "{:^78}".format("Element/DiscreteElement benchmark") + "*\n" +
        "*" * 80 + "\n\n" +
        "Nb iterations tested: " + str(nb_iterations) + "\n\n"
    )

    s = "CONSTRUCTORS:"
    print(s)
    f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Empty set creation:"
    print(s)
    f.write(s + "\n")
    
    time_function(nb_iterations, DiscreteElement, 2, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 10, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 100, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 1000, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 10000, 0, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Empty set creation (unsafe):"
    print(s)
    f.write(s + "\n")
    
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 2, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 10, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 100, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 1000, 0, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 10000, 0, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Empty set creation (from string):"
    print(s)
    f.write(s + "\n")
    
    s1 = "0"*2
    s2 = "0"*10
    s3 = "0"*100
    s4 = "0"*1000
    s5 = "0"*10000
    time_function(nb_iterations, DiscreteElement.factory_from_str, s1, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s2, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s3, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s4, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s5, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Complete set creation:"
    print(s)
    f.write(s + "\n")
    
    n1 = 2**2-1
    n2 = 2**10-1
    n3 = 2**100-1
    n4 = 2**1000-1
    n5 = 2**10000-1
    time_function(nb_iterations, DiscreteElement, 2, n1, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 10, n2, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 100, n3, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 1000, n4, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 10000, n5, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Complete set creation (unsafe):"
    print(s)
    f.write(s + "\n")
    
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 2, n1, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 10, n2, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 100, n3, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 1000, n4, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 10000, n5, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Complete set creation (from string):"
    print(s)
    f.write(s + "\n")

    s1 = "1"*2
    s2 = "1"*10
    s3 = "1"*100
    s4 = "1"*1000
    s5 = "1"*10000
    time_function(nb_iterations, DiscreteElement.factory_from_str, s1, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s2, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s3, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s4, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, s5, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Any element creation:"
    print(s)
    f.write(s + "\n")

    time_function(nb_iterations, DiscreteElement, 2, 1, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 10, 123, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 100, 12345, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 1000, 1234567, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement, 10000, 123456789, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Any element creation (unsafe):"
    print(s)
    f.write(s + "\n")

    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 2, 1, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 10, 123, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 100, 12345, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 1000, 1234567, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_constructor_unsafe, 10000, 123456789, timeout=timeout, file=f)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Any element creation (from string):"
    print(s)
    f.write(s + "\n")

    e1 = str(DiscreteElement(2, 1))
    e2 = str(DiscreteElement(10, 123))
    e3 = str(DiscreteElement(100, 12345))
    e4 = str(DiscreteElement(1000, 1234567))
    e5 = str(DiscreteElement(10000, 123456789))
    time_function(nb_iterations, DiscreteElement.factory_from_str, e1, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, e2, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, e3, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, e4, timeout=timeout, file=f)
    time_function(nb_iterations, DiscreteElement.factory_from_str, e5, timeout=timeout, file=f)

    s = "-" * 80
    print(s)
    f.write(s + "\n")

    s = "PROPERTIES:"
    print(s)
    f.write(s + "\n")

    #Get some elements to work on:
    e1 = DiscreteElement(2, 1)
    e2 = DiscreteElement(10, 123)
    e3 = DiscreteElement(100, 12345)
    e4 = DiscreteElement(1000, 1234567)
    e5 = DiscreteElement(10000, 123456789)

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Cardinal (" + str(nb_iterations) + " times on the same object):" 
    print(s)
    f.write(s + "\n")

    s = format_time("size2.cardinal", time_property(nb_iterations, e1, "cardinal", timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.cardinal", time_property(nb_iterations, e2, "cardinal", timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.cardinal", time_property(nb_iterations, e3, "cardinal", timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.cardinal", time_property(nb_iterations, e4, "cardinal", timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.cardinal", time_property(nb_iterations, e5, "cardinal", timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    e1 = DiscreteElement(2, 1)
    e2 = DiscreteElement(10, 123)
    e3 = DiscreteElement(100, 12345)
    e4 = DiscreteElement(1000, 1234567)
    e5 = DiscreteElement(10000, 123456789)

    s = "Cardinal (once on each object):" 
    print(s)
    f.write(s + "\n")

    s = format_time("size2.cardinal", time_property(nb_iterations, e1, "cardinal", timeout=timeout, bounded_copy=True), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.cardinal", time_property(nb_iterations, e2, "cardinal", timeout=timeout, bounded_copy=True), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.cardinal", time_property(nb_iterations, e3, "cardinal", timeout=timeout, bounded_copy=True), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.cardinal", time_property(nb_iterations, e4, "cardinal", timeout=timeout, bounded_copy=True), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.cardinal", time_property(nb_iterations, e5, "cardinal", timeout=timeout, bounded_copy=True), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    s = "-" * 80
    print(s)
    f.write(s + "\n")

    s = "SET-THEORETIC OPERATIONS:"
    print(s)
    f.write(s + "\n")
    
    #Get some elements to work on:
    e1 = DiscreteElement(2, 1)
    e2 = DiscreteElement(10, 123)
    e3 = DiscreteElement(100, 12345)
    e4 = DiscreteElement(1000, 1234567)
    e5 = DiscreteElement(10000, 123456789)
    eA = DiscreteElement(2, 2)
    eB = DiscreteElement(10, 321)
    eC = DiscreteElement(100, 54321543215432154321)
    eD = DiscreteElement(1000, 7654321765432176543217654321)
    eE = DiscreteElement(10000, 987654321987654321987654321987654321)
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Get the opposite:"
    print(s)
    f.write(s + "\n")

    s = format_time("size2.opposite()", time_function(nb_iterations, e1.opposite, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.opposite()", time_function(nb_iterations, e2.opposite, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.opposite()", time_function(nb_iterations, e3.opposite, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.opposite()", time_function(nb_iterations, e4.opposite, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.opposite()", time_function(nb_iterations, e5.opposite, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Get the conjunction:"
    print(s)
    f.write(s + "\n")

    s = format_time("size2.conjunction(size2)", time_function(nb_iterations, e1.conjunction, eA, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.conjunction(size10)", time_function(nb_iterations, e2.conjunction, eB, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.conjunction(size100)", time_function(nb_iterations, e3.conjunction, eC, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.conjunction(size1000)", time_function(nb_iterations, e4.conjunction, eD, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.conjunction(size10000)", time_function(nb_iterations, e5.conjunction, eE, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Get the conjunction (unsafe):"
    print(s)
    f.write(s + "\n")

    s = format_time("size2.conjunction_unsafe(size2)", time_function(nb_iterations, e1.conjunction_unsafe, eA, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.conjunction_unsafe(size10)", time_function(nb_iterations, e2.conjunction_unsafe, eB, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.conjunction_unsafe(size100)", time_function(nb_iterations, e3.conjunction_unsafe, eC, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.conjunction_unsafe(size1000)", time_function(nb_iterations, e4.conjunction_unsafe, eD, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.conjunction_unsafe(size10000)", time_function(nb_iterations, e5.conjunction_unsafe, eE, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Get the disjunction:"
    print(s)
    f.write(s + "\n")

    s = format_time("size2.disjunction(size2)", time_function(nb_iterations, e1.disjunction, eA, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.disjunction(size10)", time_function(nb_iterations, e2.disjunction, eB, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.disjunction(size100)", time_function(nb_iterations, e3.disjunction, eC, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.disjunction(size1000)", time_function(nb_iterations, e4.disjunction, eD, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.disjunction(size10000)", time_function(nb_iterations, e5.disjunction, eE, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Get the disjunction (unsafe):"
    print(s)
    f.write(s + "\n")

    s = format_time("size2.disjunction_unsafe(size2)", time_function(nb_iterations, e1.disjunction_unsafe, eA, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.disjunction_unsafe(size10)", time_function(nb_iterations, e2.disjunction_unsafe, eB, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.disjunction_unsafe(size100)", time_function(nb_iterations, e3.disjunction_unsafe, eC, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.disjunction_unsafe(size1000)", time_function(nb_iterations, e4.disjunction_unsafe, eD, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.disjunction_unsafe(size10000)", time_function(nb_iterations, e5.disjunction_unsafe, eE, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Is complete?:"
    print(s)
    f.write(s + "\n")

    s = format_time("size2.is_complete()", time_function(nb_iterations, e1.is_complete, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.is_complete()", time_function(nb_iterations, e2.is_complete, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.is_complete()", time_function(nb_iterations, e3.is_complete, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.is_complete()", time_function(nb_iterations, e4.is_complete, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.is_complete()", time_function(nb_iterations, e5.is_complete, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    s = "-" * 80
    print(s)
    f.write(s + "\n")

    s = "UTILITIES:"
    print(s)
    f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "str():"
    print(s)
    f.write(s + "\n")

    e1 = DiscreteElement.get_complete_element(2)
    e2 = DiscreteElement.get_complete_element(10)
    e3 = DiscreteElement.get_complete_element(100)
    e4 = DiscreteElement.get_complete_element(1000)
    e5 = DiscreteElement.get_complete_element(10000)
    s = format_time("size2.__str__()", time_function(nb_iterations, e1.__str__, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10.__str__()", time_function(nb_iterations, e2.__str__, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size100.__str__()", time_function(nb_iterations, e3.__str__, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size1000.__str__()", time_function(nb_iterations, e4.__str__, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    s = format_time("size10000.__str__()", time_function(nb_iterations, e5.__str__, verbose=False, timeout=timeout), nb_iterations, timeout)
    print(s)
    f.write(s + "\n")
    
    f.close()

