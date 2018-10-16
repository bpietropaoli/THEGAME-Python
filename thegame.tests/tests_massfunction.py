#!/usr/bin/python

################################################################################
# thegame.tests_massfunction.py                                                #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@insight-centre.org                              #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module only provides a main that executes short tests to check that     #
# methods of massfunction.py provide expected results.                         #
################################################################################

###############
# MAIN: TESTS #
###############

if __name__ == '__main__':
    import tests_utility
    import sys
    import os
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
    from thegame import element
    from thegame import massfunction
    from thegame.element import DiscreteElement
    from thegame.massfunction import MassFunction
    
    print(
        "*" * 80 + "\n" +
        "*" + "{:^78}".format(os.path.basename(__file__)) + "*\n" +
        "*" * 80
    )

    # A dictionary with function names as keys and a list of calls that failed for each one of them
    # in the form ("call_that_failed()", "reason", exception if there's one (can be None))
    failed = {}

    validSet1   = ((DiscreteElement(3, 0), 0.1), (DiscreteElement(3, 1), 0.3), (DiscreteElement(3, 2), 0.6))
    validSet2   = ((DiscreteElement.factory_from_str('1100'), 0.2), (DiscreteElement.factory_from_str('0110'), 0.3), 
                  (DiscreteElement.factory_from_str('0011'), 0.4), (DiscreteElement.factory_from_str('1001'), 0.1))
    invalidSet1 = ((DiscreteElement(3, 0), 0.1), (0.3, DiscreteElement(3,1)))
    invalidSet2 = ((DiscreteElement(3, 0), 0.1), (DiscreteElement(4, 1), 0.3), (DiscreteElement(2, 1), 0.6))

    e1 = DiscreteElement.factory_from_str('000')
    e2 = DiscreteElement.factory_from_str('001')
    e3 = DiscreteElement.factory_from_str('010')
    e4 = DiscreteElement.factory_from_str('011')
    e5 = DiscreteElement.factory_from_str('100')
    e6 = DiscreteElement.factory_from_str('101')
    e7 = DiscreteElement.factory_from_str('110')
    e8 = DiscreteElement.factory_from_str('111')

    #######################
    # TESTS: MassFunction #
    #######################

    function = "MassFunction.__init__(self, *focal_elements)"
    print("Test of " + function + " ...")

    #(function_to_call, expected_exception)
    tests = [
        (None,                                                  MassFunction),
        (None,                                                  MassFunction) + validSet1,
        (None,                                                  MassFunction) + validSet2,
        (ValueError,                                            MassFunction) + invalidSet1,
        (massfunction.IncompatibleElementsInAMassFunctionError, MassFunction) + invalidSet2
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "str(MassFunction) / MassFunction.__str__(self)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        ("{}",                                                   str, MassFunction()),
        ("{000:0.1000, 001:0.3000, 010:0.6000}",                 str, MassFunction(*validSet1)),
        ("{0011:0.4000, 0110:0.3000, 1001:0.1000, 1100:0.2000}", str, MassFunction(*validSet2)),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.add_mass(self, *focal_elements) / MassFunction.remove_mass(self, *focal_elements)"
    print("Test of " + function + " ...")

    m = MassFunction()

    #(object_to_modify, function_to_call, expected_output)
    tests = [
        ("{}",                                               m.add_mass),
        ("{000:0.1000, 001:0.3000, 010:0.6000}",             m.add_mass, (e1,0.1), (e2,0.3), (e3,0.6)),
        ("{000:0.2000, 001:0.6000, 010:1.2000}",             m.add_mass, (e1,0.1), (e2,0.3), (e3,0.6)),
        ("{000:0.2000, 001:0.6000, 010:1.2000, 111:0.8000}", m.add_mass, (e8,0.8)),
        
        ("{000:0.2000, 001:0.6000, 010:1.2000, 111:0.0000}", m.remove_mass, (e8,0.8)),
        ("{000:0.2000, 001:0.6000, 010:1.2000, 111:0.0000}", m.remove_mass),
        ("{000:0.2000, 001:0.6000, 010:0.2000, 111:0.0000}", m.remove_mass, (e3,1.0))
    ]
    errors = tests_utility.modifying_method_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors

    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction(*validSet1)

    tests = [
        (None,                                                  m.add_mass),
        (None,                                                  m.remove_mass),
        (ValueError,                                            m.add_mass)    + invalidSet1,
        (massfunction.IncompatibleElementsInAMassFunctionError, m.add_mass)    + invalidSet2,
        (ValueError,                                            m.remove_mass) + invalidSet1,
        (massfunction.IncompatibleElementsInAMassFunctionError, m.remove_mass) + invalidSet2,
        (massfunction.IncompatibleElementsInAMassFunctionError, m.add_mass)    + validSet2,
        (massfunction.IncompatibleElementsInAMassFunctionError, m.remove_mass) + validSet2
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.add_mass_unsafe(self, *focal_elements) / MassFunction.remove_mass_unsafe(self, *focal_elements)"
    print("Test of " + function + " ...")

    m = MassFunction()

    #(object_to_modify, function_to_call, expected_output)
    tests = [
        ("{}",                                               m.add_mass_unsafe),
        ("{000:0.1000, 001:0.3000, 010:0.6000}",             m.add_mass_unsafe, (e1,0.1), (e2,0.3), (e3,0.6)),
        ("{000:0.2000, 001:0.6000, 010:1.2000}",             m.add_mass_unsafe, (e1,0.1), (e2,0.3), (e3,0.6)),
        ("{000:0.2000, 001:0.6000, 010:1.2000, 111:0.8000}", m.add_mass_unsafe, (e8,0.8)),
        
        ("{000:0.2000, 001:0.6000, 010:1.2000, 111:0.0000}", m.remove_mass_unsafe, (e8,0.8)),
        ("{000:0.2000, 001:0.6000, 010:1.2000, 111:0.0000}", m.remove_mass_unsafe),
        ("{000:0.2000, 001:0.6000, 010:0.2000, 111:0.0000}", m.remove_mass_unsafe, (e3,1.0))
    ]
    errors = tests_utility.modifying_method_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.clean(self)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e3,0.6))
    m3 = MassFunction((e1,0.0000000001), (e2,0.3), (e3,0.000000006))
    
    #(object_to_modify, function_to_call, expected_output)
    tests = [
        ("{}",                                   m1.clean),
        ("{000:0.1000, 001:0.3000, 010:0.6000}", m2.clean),
        ("{001:0.3000}",                         m3.clean),
    ]
    errors = tests_utility.modifying_method_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction._sum(self)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e3,0.6))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e3,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e3,0.8))
    
    #(function_to_call, expected_output)
    tests = [
        (0, m1._sum),
        (1, m2._sum),
        (4, m3._sum),
        (2, m4._sum)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.normalise(self)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e3,0.6))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e3,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e3,0.8)) 
    
    #(object_to_modify, function_to_call, expected_output)
    tests = [
        ("{}",                                   m1.normalise),
        ("{000:0.1000, 001:0.3000, 010:0.6000}", m2.normalise),
        ("{000:0.1000, 001:0.3000, 010:0.6000}", m3.normalise),
        ("{000:0.0000, 001:0.6000, 010:0.4000}", m4.normalise),
    ]
    errors = tests_utility.modifying_method_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.is_empty(self)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.0), (e2,0.0), (e3,0.0))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e3,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e3,0.8))
    
    #(function_to_call, expected_output)
    tests = [
        (True,  m1.is_empty),
        (True,  m2.is_empty),
        (False, m3.is_empty),
        (False, m4.is_empty)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.has_valid_values(self)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.0), (e2,0.0), (e3,0.0))
    m3 = MassFunction((e1,0.4), (e2,0.8), (e3,0.3))
    m4 = MassFunction((e1,0.4), (e2,1.2), (e3,2.4))
    m5 = MassFunction((e1,0.0), (e2,1.2), (e3,0.8))
    m6 = MassFunction((e1,-0.3), (e2,1.0), (e3,0.8))
    
    #(function_to_call, expected_output)
    tests = [
        (True,  m1.has_valid_values),
        (True,  m2.has_valid_values),
        (True,  m3.has_valid_values),
        (False, m4.has_valid_values),
        (False, m5.has_valid_values),
        (False, m6.has_valid_values)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.has_valid_sum(self)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.0), (e2,0.0), (e3,0.0))
    m3 = MassFunction((e1,0.4), (e2,0.8), (e3,0.3))
    m4 = MassFunction((e1,0.4), (e2,1.2), (e3, 2.4))
    m5 = MassFunction((e1,-1.0), (e2,1.2), (e3,0.8))
    m6 = MassFunction((e1,-0.3), (e2,0.5), (e3,0.8))
    m7 = MassFunction((e1,0.3), (e2,0.5), (e3,0.2))
    
    #(function_to_call, expected_output)
    tests = [
        (False, m1.has_valid_sum),
        (False, m2.has_valid_sum),
        (False, m3.has_valid_sum),
        (False, m4.has_valid_sum),
        (True,  m5.has_valid_sum),
        (True,  m6.has_valid_sum),
        (True,  m7.has_valid_sum)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.m(self, element) / MassFunction.mass(self, element)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e3,0.6))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e3,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e3,0.8))
    
    #(function_to_call, expected_output)
    tests = [
        (0,   m1.m, e1),
        (0,   m1.m, e3),
        (0,   m1.m, e5),
        (0.1, m2.m, e1),
        (0.3, m2.m, e2),
        (0.6, m2.m, e3),
        (0,   m2.m, e4),
        (0,   m2.m, e5),
        (0.4, m3.m, e1),
        (1.2, m3.m, e2),
        (2.4, m3.m, e3),
        (0,   m3.m, e4),
        (0,   m3.m, e5),
        (0,   m4.m, e1),
        (1.2, m4.m, e2),
        (0.8, m4.m, e3),
        (0,   m4.m, e4),
        (0,   m4.m, e5)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.bel(self, element) / MassFunction.belief(self, element)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e4,0.6))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e4,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e4,0.8))
    
    #(function_to_call, expected_output)
    tests = [
        (0, m1.bel, e1),
        (0, m1.bel, e3),
        (0, m1.bel, e5),
        
        (0,   m2.bel, e1),
        (0.3, m2.bel, e2),
        (0,   m2.bel, e3),
        (0.9, m2.bel, e4),
        (0,   m2.bel, e5),
        (0.3, m2.bel, e6),
        (0,   m2.bel, e7),
        (0.9, m2.bel, e8),
        
        (0,   m3.bel, e1),
        (1.2, m3.bel, e2),
        (0,   m3.bel, e3),
        (3.6, m3.bel, e4),
        (0,   m3.bel, e5),
        (1.2, m3.bel, e6),
        (0,   m3.bel, e7),
        (3.6, m3.bel, e8),
        
        (0,   m4.bel, e1),
        (1.2, m4.bel, e2),
        (0,   m4.bel, e3),
        (2,   m4.bel, e4),
        (0,   m4.bel, e5),
        (1.2, m4.bel, e6),
        (0,   m4.bel, e7),
        (2,   m4.bel, e8)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.betP(self, element) / MassFunction.pignistic_transformation(self, element)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e4,0.6))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e4,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e4,0.8))
    
    #(function_to_call, expected_output)
    tests = [                
        (0, m1.betP, e1),
        (0, m1.betP, e3),
        (0, m1.betP, e5),
        
        (0,   m2.betP, e1),
        (0.6, m2.betP, e2),
        (0.3, m2.betP, e3),
        (0.9, m2.betP, e4),
        (0,   m2.betP, e5),
        (0.6, m2.betP, e6),
        (0.3, m2.betP, e7),
        (0.9, m2.betP, e8),
        
        (0,   m3.betP, e1),
        (2.4, m3.betP, e2),
        (1.2, m3.betP, e3),
        (3.6, m3.betP, e4),
        (0,   m3.betP, e5),
        (2.4, m3.betP, e6),
        (1.2, m3.betP, e7),
        (3.6, m3.betP, e8),
        
        (0,   m4.betP, e1),
        (1.6, m4.betP, e2),
        (0.4, m4.betP, e3),
        (2,   m4.betP, e4),
        (0,   m4.betP, e5),
        (1.6, m4.betP, e6),
        (0.4, m4.betP, e7),
        (2,   m4.betP, e8)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.pl(self, element) / MassFunction.plausibility(self, element)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e4,0.6))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e4,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e4,0.8))
    
    #(function_to_call, expected_output)
    tests = [        
        (0, m1.pl, e1),
        (0, m1.pl, e3),
        (0, m1.pl, e5),
        
        (1,   m2.pl, e1),
        (0.9, m2.pl, e2),
        (0.6, m2.pl, e3),
        (0.9, m2.pl, e4),
        (0,   m2.pl, e5),
        (0.9, m2.pl, e6),
        (0.6, m2.pl, e7),
        (0.9, m2.pl, e8),
        
        (4,   m3.pl, e1),
        (3.6, m3.pl, e2),
        (2.4, m3.pl, e3),
        (3.6, m3.pl, e4),
        (0,   m3.pl, e5),
        (3.6, m3.pl, e6),
        (2.4, m3.pl, e7),
        (3.6, m3.pl, e8),
        
        (2,   m4.pl, e1),
        (2,   m4.pl, e2),
        (0.8, m4.pl, e3),
        (2,   m4.pl, e4),
        (0,   m4.pl, e5),
        (2,   m4.pl, e6),
        (0.8, m4.pl, e7),
        (2,   m4.pl, e8)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.q(self, element) / MassFunction.commonality(self, element)"
    print("Test of " + function + " ...")

    m1 = MassFunction()
    m2 = MassFunction((e1,0.1), (e2,0.3), (e4,0.6))
    m3 = MassFunction((e1,0.4), (e2,1.2), (e4,2.4))
    m4 = MassFunction((e1,0.0), (e2,1.2), (e4,0.8))
    
    #(function_to_call, expected_output)
    tests = [
        (0, m1.q, e1),
        (0, m1.q, e3),
        (0, m1.q, e5),
        
        (1,   m2.q, e1),
        (0.9, m2.q, e2),
        (0.6, m2.q, e3),
        (0.6, m2.q, e4),
        (0,   m2.q, e5),
        (0,   m2.q, e6),
        (0,   m2.q, e7),
        (0,   m2.q, e8),
        
        (4,   m3.q, e1),
        (3.6, m3.q, e2),
        (2.4, m3.q, e3),
        (2.4, m3.q, e4),
        (0,   m3.q, e5),
        (0,   m3.q, e6),
        (0,   m3.q, e7),
        (0,   m3.q, e8),
        
        (2,   m4.q, e1),
        (2,   m4.q, e2),
        (0.8, m4.q, e3),
        (0.8, m4.q, e4),
        (0,   m4.q, e5),
        (0,   m4.q, e6),
        (0,   m4.q, e7),
        (0,   m4.q, e8)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.get_min(criteria, max_card, elements)"
    print("Test of " + function + " ...")

    m1 = MassFunction((e1,0.1), (e2,0.3), (e4,0.6))

    min1 = MassFunction.get_min(m1.mass, 1, DiscreteElement.iterator_powerset(3))
    min2 = MassFunction.get_min(m1.mass, 2, DiscreteElement.iterator_powerset(3))
    min3 = MassFunction.get_min(m1.mass, 3, DiscreteElement.iterator_powerset(3))
    result1 = "[(010, 0.0000), (100, 0.0000)]"
    result2 = "[(010, 0.0000), (100, 0.0000), (101, 0.0000), (110, 0.0000)]"
    result3 = "[(010, 0.0000), (100, 0.0000), (101, 0.0000), (110, 0.0000), (111, 0.0000)]"

    min4 = MassFunction.get_min(m1.bel, 1, DiscreteElement.iterator_powerset(3))
    min5 = MassFunction.get_min(m1.bel, 2, DiscreteElement.iterator_powerset(3))
    min6 = MassFunction.get_min(m1.bel, 3, DiscreteElement.iterator_powerset(3))
    result4 = "[(010, 0.0000), (100, 0.0000)]"
    result5 = "[(010, 0.0000), (100, 0.0000), (110, 0.0000)]"
    result6 = "[(010, 0.0000), (100, 0.0000), (110, 0.0000)]"

    min7 = MassFunction.get_min(m1.betP, 1, DiscreteElement.iterator_powerset(3))
    min8 = MassFunction.get_min(m1.betP, 2, DiscreteElement.iterator_powerset(3))
    min9 = MassFunction.get_min(m1.betP, 3, DiscreteElement.iterator_powerset(3))
    result7 = "[(100, 0.0000)]"
    result8 = "[(100, 0.0000)]"
    result9 = "[(100, 0.0000)]"

    min10 = MassFunction.get_min(m1.pl, 1, DiscreteElement.iterator_powerset(3))
    min11 = MassFunction.get_min(m1.pl, 2, DiscreteElement.iterator_powerset(3))
    min12 = MassFunction.get_min(m1.pl, 3, DiscreteElement.iterator_powerset(3))
    result10 = "[(100, 0.0000)]"
    result11 = "[(100, 0.0000)]"
    result12 = "[(100, 0.0000)]"

    min13 = MassFunction.get_min(m1.q, 1, DiscreteElement.iterator_powerset(3))
    min14 = MassFunction.get_min(m1.q, 2, DiscreteElement.iterator_powerset(3))
    min15 = MassFunction.get_min(m1.q, 3, DiscreteElement.iterator_powerset(3))
    result13 = "[(100, 0.0000)]"
    result14 = "[(100, 0.0000), (101, 0.0000), (110, 0.0000)]"
    result15 = "[(100, 0.0000), (101, 0.0000), (110, 0.0000), (111, 0.0000)]"
    
    #(function_to_call, expected_output)
    tests = [
        (result1, MassFunction.format_extrema_result, min1),
        (result2, MassFunction.format_extrema_result, min2),
        (result3, MassFunction.format_extrema_result, min3),
        (result4, MassFunction.format_extrema_result, min4),
        (result5, MassFunction.format_extrema_result, min5),
        (result6, MassFunction.format_extrema_result, min6),
        (result7, MassFunction.format_extrema_result, min7),
        (result8, MassFunction.format_extrema_result, min8),
        (result9, MassFunction.format_extrema_result, min9),
        (result10, MassFunction.format_extrema_result, min10),
        (result11, MassFunction.format_extrema_result, min11),
        (result12, MassFunction.format_extrema_result, min12),
        (result13, MassFunction.format_extrema_result, min13),
        (result14, MassFunction.format_extrema_result, min14),
        (result15, MassFunction.format_extrema_result, min15),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.get_max(criteria, max_card, elements)"
    print("Test of " + function + " ...")

    m1 = MassFunction((e1,0.1), (e2,0.3), (e4,0.6))

    max1 = MassFunction.get_max(m1.mass, 1, DiscreteElement.iterator_powerset(3))
    max2 = MassFunction.get_max(m1.mass, 2, DiscreteElement.iterator_powerset(3))
    max3 = MassFunction.get_max(m1.mass, 3, DiscreteElement.iterator_powerset(3))
    result1 = "[(001, 0.3000)]"
    result2 = "[(011, 0.6000)]"
    result3 = "[(011, 0.6000)]"

    max4 = MassFunction.get_max(m1.bel, 1, DiscreteElement.iterator_powerset(3))
    max5 = MassFunction.get_max(m1.bel, 2, DiscreteElement.iterator_powerset(3))
    max6 = MassFunction.get_max(m1.bel, 3, DiscreteElement.iterator_powerset(3))
    result4 = "[(001, 0.3000)]"
    result5 = "[(011, 0.9000)]"
    result6 = "[(011, 0.9000), (111, 0.9000)]"

    max7 = MassFunction.get_max(m1.betP, 1, DiscreteElement.iterator_powerset(3))
    max8 = MassFunction.get_max(m1.betP, 2, DiscreteElement.iterator_powerset(3))
    max9 = MassFunction.get_max(m1.betP, 3, DiscreteElement.iterator_powerset(3))
    result7 = "[(001, 0.6000)]"
    result8 = "[(011, 0.9000)]"
    result9 = "[(011, 0.9000), (111, 0.9000)]"

    max10 = MassFunction.get_max(m1.pl, 1, DiscreteElement.iterator_powerset(3))
    max11 = MassFunction.get_max(m1.pl, 2, DiscreteElement.iterator_powerset(3))
    max12 = MassFunction.get_max(m1.pl, 3, DiscreteElement.iterator_powerset(3))
    result10 = "[(001, 0.9000)]"
    result11 = "[(001, 0.9000), (011, 0.9000), (101, 0.9000)]"
    result12 = "[(001, 0.9000), (011, 0.9000), (101, 0.9000), (111, 0.9000)]"

    max13 = MassFunction.get_max(m1.q, 1, DiscreteElement.iterator_powerset(3))
    max14 = MassFunction.get_max(m1.q, 2, DiscreteElement.iterator_powerset(3))
    max15 = MassFunction.get_max(m1.q, 3, DiscreteElement.iterator_powerset(3))
    result13 = "[(001, 0.9000)]"
    result14 = "[(001, 0.9000)]"
    result15 = "[(001, 0.9000)]"
    
    #(function_to_call, expected_output)
    tests = [
        (result1, MassFunction.format_extrema_result, max1),
        (result2, MassFunction.format_extrema_result, max2),
        (result3, MassFunction.format_extrema_result, max3),
        (result4, MassFunction.format_extrema_result, max4),
        (result5, MassFunction.format_extrema_result, max5),
        (result6, MassFunction.format_extrema_result, max6),
        (result7, MassFunction.format_extrema_result, max7),
        (result8, MassFunction.format_extrema_result, max8),
        (result9, MassFunction.format_extrema_result, max9),
        (result10, MassFunction.format_extrema_result, max10),
        (result11, MassFunction.format_extrema_result, max11),
        (result12, MassFunction.format_extrema_result, max12),
        (result13, MassFunction.format_extrema_result, max13),
        (result14, MassFunction.format_extrema_result, max14),
        (result15, MassFunction.format_extrema_result, max15),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    m1 = MassFunction((e2, 0.3), (e3, 0.3), (e4, 0.3), (e5, 0.1))
    m2 = MassFunction((e2, 0.5), (e4, 0.2), (e6, 0.2), (e8, 0.1))
    m3 = MassFunction((e4, 0.6), (e5, 0.4))
    m4 = MassFunction((e1, 1))
    m5 = MassFunction((e2, 1))
    m6 = MassFunction((e7, 1))

    function = "MassFunction.specificity(self)"
    print("Test of " + function + " ...")

    tests = [
        (0.85,     m1.specificity),
        (0.733333, m2.specificity),
        (0.7,      m3.specificity),
        (0,        m4.specificity),
        (1,        m5.specificity),
        (0.5,      m6.specificity),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.non_specificity(self)"
    print("Test of " + function + " ...")

    tests = [
        (0.3,      m1.non_specificity),
        (0.558496, m2.non_specificity),
        (0.6,      m3.non_specificity),
        (0,        m4.non_specificity),
        (0,        m5.non_specificity),
        (1,        m6.non_specificity),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.discrepancy(self)"
    print("Test of " + function + " ...")

    tests = [
        (1.068996, m1.discrepancy),
        (0.30631,  m2.discrepancy),
        (0.970951, m3.discrepancy),
        (0,        m4.discrepancy),
        (0,        m5.discrepancy),
        (0,        m6.discrepancy),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.weakening(self, alpha)"
    print("Test of " + function + " ...")

    tests = [
        ("{000:0.2000, 001:0.2400, 010:0.2400, 011:0.2400, 100:0.0800}", str, m1.weakening(0.2)),
        ("{000:0.2000, 001:0.4000, 011:0.1600, 101:0.1600, 111:0.0800}", str, m2.weakening(0.2)),
        ("{000:0.2000, 011:0.4800, 100:0.3200}",                         str, m3.weakening(0.2)),
        ("{000:1.0000}",                                                 str, m4.weakening(0.2)),
        ("{000:0.2000, 001:0.8000}",                                     str, m5.weakening(0.2)),
        ("{000:0.2000, 110:0.8000}",                                     str, m6.weakening(0.2)),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors

    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    
    tests = [
        (massfunction.EmptyMassFunctionError, m.weakening,   0.2),
        (massfunction.EmptyMassFunctionError, m.weakening,    -1),
        (None,                                m1.weakening,    0),
        (None,                                m1.weakening,    1),
        (ValueError,                          m1.weakening, -0.1),
        (ValueError,                          m1.weakening,  1.1),
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    m1 = MassFunction((e2, 0.3), (e3, 0.3), (e4, 0.3), (e5, 0.1))
    m2 = MassFunction((e2, 0.5), (e4, 0.2), (e6, 0.2), (e8, 0.1))
    m3 = MassFunction((e4, 0.6), (e5, 0.4))
    m4 = MassFunction((e1, 1))
    m5 = MassFunction((e2, 1))
    m6 = MassFunction((e7, 1))
    
    function = "MassFunction.discounting(self, alpha)"
    print("Test of " + function + " ...")

    tests = [
        ("{001:0.2400, 010:0.2400, 011:0.2400, 100:0.0800, 111:0.2000}", str, m1.discounting(0.2)),
        ("{001:0.4000, 011:0.1600, 101:0.1600, 111:0.2800}",             str, m2.discounting(0.2)),
        ("{011:0.4800, 100:0.3200, 111:0.2000}",                         str, m3.discounting(0.2)),
        ("{000:0.8000, 111:0.2000}",                                     str, m4.discounting(0.2)),
        ("{001:0.8000, 111:0.2000}",                                     str, m5.discounting(0.2)),
        ("{110:0.8000, 111:0.2000}",                                     str, m6.discounting(0.2)),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors

    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    
    tests = [
        (massfunction.EmptyMassFunctionError, m.discounting,   0.2),
        (massfunction.EmptyMassFunctionError, m.discounting,    -1),
        (None,                                m1.discounting,    0),
        (None,                                m1.discounting,    1),
        (ValueError,                          m1.discounting, -0.1),
        (ValueError,                          m1.discounting,  1.1),
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    m1 = MassFunction((e2, 0.3), (e3, 0.3), (e4, 0.3), (e5, 0.1))
    m2 = MassFunction((e2, 0.5), (e4, 0.2), (e6, 0.2), (e8, 0.1))
    m3 = MassFunction((e4, 0.6), (e5, 0.4))
    m4 = MassFunction((e1, 1))
    m5 = MassFunction((e2, 1))
    m6 = MassFunction((e7, 1))
    
    function = "MassFunction.difference(self, mass_function)"
    print("Test of " + function + " ...")
    
    tests = [
        ("{}",                                                                          str, m1.difference(m1)),
        ("{001:-0.2000, 010:0.3000, 011:0.1000, 100:0.1000, 101:-0.2000, 111:-0.1000}", str, m1.difference(m2)),
        ("{001:0.3000, 010:0.3000, 011:-0.3000, 100:-0.3000}",                          str, m1.difference(m3)),
        ("{}",                                                                          str, m2.difference(m2)),
        ("{001:0.2000, 010:-0.3000, 011:-0.1000, 100:-0.1000, 101:0.2000, 111:0.1000}", str, m2.difference(m1)),
        ("{001:0.5000, 011:-0.4000, 100:-0.4000, 101:0.2000, 111:0.1000}",              str, m2.difference(m3)),
        ("{}",                                                                          str, m3.difference(m3)),
        ("{001:-0.3000, 010:-0.3000, 011:0.3000, 100:0.3000}",                          str, m3.difference(m1)),
        ("{001:-0.5000, 011:0.4000, 100:0.4000, 101:-0.2000, 111:-0.1000}",             str, m3.difference(m2)),
        ("{}",                                                                          str, m4.difference(m4)),
        ("{000:1.0000, 001:-0.3000, 010:-0.3000, 011:-0.3000, 100:-0.1000}",            str, m4.difference(m1)),
        ("{000:1.0000, 001:-0.5000, 011:-0.2000, 101:-0.2000, 111:-0.1000}",            str, m4.difference(m2)),
        ("{}",                                                                          str, m5.difference(m5)),
        ("{001:0.7000, 010:-0.3000, 011:-0.3000, 100:-0.1000}",                         str, m5.difference(m1)),
        ("{001:0.5000, 011:-0.2000, 101:-0.2000, 111:-0.1000}",                         str, m5.difference(m2)),
        ("{}",                                                                          str, m6.difference(m6)),
        ("{001:-0.3000, 010:-0.3000, 011:-0.3000, 100:-0.1000, 110:1.0000}",            str, m6.difference(m1)),
        ("{001:-0.5000, 011:-0.2000, 101:-0.2000, 110:1.0000, 111:-0.1000}",            str, m6.difference(m2)),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.difference, 0.5),
        (None,                                        m1.difference, m),
        (massfunction.IncompatibleMassFunctionsError, m1.difference, mToFail),
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    m1 = MassFunction((e2, 0.3), (e3, 0.3), (e4, 0.3), (e5, 0.1))
    m2 = MassFunction((e2, 0.5), (e4, 0.2), (e6, 0.2), (e8, 0.1))
    m3 = MassFunction((e4, 0.6), (e5, 0.4))
    m4 = MassFunction((e1, 1))
    m5 = MassFunction((e2, 1))
    m6 = MassFunction((e7, 1))
    
    function = "MassFunction.difference_unsafe(self, mass_function)"
    print("Test of " + function + " ...")
    
    tests = [
        ("{}",                                                                          str, m1.difference_unsafe(m1)),
        ("{001:-0.2000, 010:0.3000, 011:0.1000, 100:0.1000, 101:-0.2000, 111:-0.1000}", str, m1.difference_unsafe(m2)),
        ("{001:0.3000, 010:0.3000, 011:-0.3000, 100:-0.3000}",                          str, m1.difference_unsafe(m3)),
        ("{}",                                                                          str, m2.difference_unsafe(m2)),
        ("{001:0.2000, 010:-0.3000, 011:-0.1000, 100:-0.1000, 101:0.2000, 111:0.1000}", str, m2.difference_unsafe(m1)),
        ("{001:0.5000, 011:-0.4000, 100:-0.4000, 101:0.2000, 111:0.1000}",              str, m2.difference_unsafe(m3)),
        ("{}",                                                                          str, m3.difference_unsafe(m3)),
        ("{001:-0.3000, 010:-0.3000, 011:0.3000, 100:0.3000}",                          str, m3.difference_unsafe(m1)),
        ("{001:-0.5000, 011:0.4000, 100:0.4000, 101:-0.2000, 111:-0.1000}",             str, m3.difference_unsafe(m2)),
        ("{}",                                                                          str, m4.difference_unsafe(m4)),
        ("{000:1.0000, 001:-0.3000, 010:-0.3000, 011:-0.3000, 100:-0.1000}",            str, m4.difference_unsafe(m1)),
        ("{000:1.0000, 001:-0.5000, 011:-0.2000, 101:-0.2000, 111:-0.1000}",            str, m4.difference_unsafe(m2)),
        ("{}",                                                                          str, m5.difference_unsafe(m5)),
        ("{001:0.7000, 010:-0.3000, 011:-0.3000, 100:-0.1000}",                         str, m5.difference_unsafe(m1)),
        ("{001:0.5000, 011:-0.2000, 101:-0.2000, 111:-0.1000}",                         str, m5.difference_unsafe(m2)),
        ("{}",                                                                          str, m6.difference_unsafe(m6)),
        ("{001:-0.3000, 010:-0.3000, 011:-0.3000, 100:-0.1000, 110:1.0000}",            str, m6.difference_unsafe(m1)),
        ("{001:-0.5000, 011:-0.2000, 101:-0.2000, 110:1.0000, 111:-0.1000}",            str, m6.difference_unsafe(m2)),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.distance(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    m1 = MassFunction((e2, 0.3), (e3, 0.3), (e4, 0.3), (e5, 0.1))
    m2 = MassFunction((e2, 0.5), (e4, 0.2), (e6, 0.2), (e8, 0.1))
    m3 = MassFunction((e4, 0.6), (e5, 0.4))
    m4 = MassFunction((e1, 1))
    m5 = MassFunction((e2, 1))
    m6 = MassFunction((e7, 1))
    m7 = MassFunction((e8, 1))
    
    tests = [
        (0,        m1.distance, m1),
        (0.329140, m1.distance, m2),
        (0.3,      m1.distance, m3),
        (0,        m2.distance, m2),
        (0.329140, m2.distance, m1),
        (0.428174, m2.distance, m3),
        (0,        m3.distance, m3),
        (0.871780, m3.distance, m4),
        (0.428174, m3.distance, m2),
        (0,        m4.distance, m4),
        (0.854400, m4.distance, m1),
        (0.909212, m4.distance, m2),
        (0,        m5.distance, m5),
        (0.529150, m5.distance, m1),
        (0.305505, m5.distance, m2),
        (0,        m6.distance, m6),
        (0.655744, m6.distance, m1),
        (1,        m6.distance, m5),
        (0,        m7.distance, m7),
        (1,        m7.distance, m4),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.distance, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.distance, m),
        (massfunction.IncompatibleMassFunctionsError, m1.distance, mToFail),
        (None,                                        m1.distance, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.distance_unsafe(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    m1 = MassFunction((e2, 0.3), (e3, 0.3), (e4, 0.3), (e5, 0.1))
    m2 = MassFunction((e2, 0.5), (e4, 0.2), (e6, 0.2), (e8, 0.1))
    m3 = MassFunction((e4, 0.6), (e5, 0.4))
    m4 = MassFunction((e1, 1))
    m5 = MassFunction((e2, 1))
    m6 = MassFunction((e7, 1))
    m7 = MassFunction((e8, 1))
    
    tests = [
        (0,        m1.distance_unsafe, m1),
        (0.329140, m1.distance_unsafe, m2),
        (0.3,      m1.distance_unsafe, m3),
        (0,        m2.distance_unsafe, m2),
        (0.329140, m2.distance_unsafe, m1),
        (0.428174, m2.distance_unsafe, m3),
        (0,        m3.distance_unsafe, m3),
        (0.871780, m3.distance_unsafe, m4),
        (0.428174, m3.distance_unsafe, m2),
        (0,        m4.distance_unsafe, m4),
        (0.854400, m4.distance_unsafe, m1),
        (0.909212, m4.distance_unsafe, m2),
        (0,        m5.distance_unsafe, m5),
        (0.529150, m5.distance_unsafe, m1),
        (0.305505, m5.distance_unsafe, m2),
        (0,        m6.distance_unsafe, m6),
        (0.655744, m6.distance_unsafe, m1),
        (1,        m6.distance_unsafe, m5),
        (0,        m7.distance_unsafe, m7),
        (1,        m7.distance_unsafe, m4),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests))) 
    print("--------------------------------------------------------------------------------")
    
    #Taken from Chen L.-Z. et al - A new fusion approach based on distance of evidences, 2005
    m1 = MassFunction((e2, 0.5), (e3, 0.2), (e5, 0.3)) #Corrected it to normalise it.
    m2 = MassFunction((e2, 0.0), (e3, 0.9), (e5, 0.1))
    m3 = MassFunction((e2, 0.55), (e3, 0.1), (e5, 0.35))
    m4 = MassFunction((e2, 0.55), (e3, 0.1), (e5, 0.35))
    m5 = MassFunction((e2, 0.55), (e3, 0.1), (e5, 0.35))

    #The first numerical example of Chen L.-Z.
    m1a = MassFunction((e2, 0.6), (e3, 0.1), (e5, 0.3))
    m2a = MassFunction((e2, 0.2), (e3, 0)  , (e5, 0.8))
    m3a = MassFunction((e2, 0.7), (e3, 0.1), (e5, 0.2))

    resultDempster1 = MassFunction((e3, 0.857143), (e5, 0.142857)) # m1 + m2
    resultDempster2 = MassFunction((e3, 0.631579), (e5, 0.368421)) # m1 + m2 + m3
    resultDempster3 = MassFunction((e3, 0.328767), (e5, 0.671233)) # m1 + m2 + m3 + m4
    resultDempster4 = MassFunction((e3, 0.122762), (e5, 0.877238)) # m1 + m2 + m3 + m4 + m5

    resultYager1 = MassFunction((e3, 0.18), (e5, 0.03), (e8, 0.79)) # m1 + m2
    resultYager2 = MassFunction((e3, 0.018), (e5, 0.0105), (e8, 0.9715)) # m1 + m2 + m3
    resultYager3 = MassFunction((e3, 0.0018), (e5, 0.003675), (e8, 0.994525)) # m1 + m2 + m3 + m4
    resultYager4 = MassFunction((e3, 0.00018), (e5, 0.001286), (e8, 0.998534)) # m1 + m2 + m3 + m4 + m5

    resultAverage1 = MassFunction((e2, 0.25), (e3, 0.55), (e5, 0.2)) # m1 + m2
    resultAverage2 = MassFunction((e2, 0.35), (e3, 0.4), (e5, 0.25)) # m1 + m2 + m3
    resultAverage3 = MassFunction((e2, 0.4), (e3, 0.325), (e5, 0.275)) # m1 + m2 + m3 + m4
    resultAverage4 = MassFunction((e2, 0.43), (e3, 0.28), (e5, 0.29)) # m1 + m2 + m3 + m4 + m5
    
    resultMurphy1 = MassFunction((e2, 0.154321), (e3, 0.746914), (e5, 0.098765)) # m1 + m2
    resultMurphy2 = MassFunction((e2, 0.3500), (e3, 0.522449), (e5, 0.127551)) # m1 + m2 + m3
    resultMurphy3 = MassFunction((e2, 0.602696), (e3, 0.262659), (e5, 0.134645)) # m1 + m2 + m3 + m4
    resultMurphy4 = MassFunction((e2, 0.795802), (e3, 0.093165), (e5, 0.111033)) # m1 + m2 + m3 + m4 + m5

    #The results presented in table 1 in Chen's paper where false.
    #I confirmed the results with the first numerical example which seems to be correct.
    #The results in the table are inconsistent with the ones provided in the first example.
    resultChen0 = MassFunction((e2, 0.720566), (e3, 0.001979), (e5, 0.277455)) # m1a + m2a + m3a
    resultChen1 = MassFunction((e2, 0.154321), (e3, 0.746914), (e5, 0.098765)) # m1 + m2
    resultChen2 = MassFunction((e2, 0.645830), (e3, 0.170832), (e5, 0.183338)) # m1 + m2 + m3
    resultChen3 = MassFunction((e2, 0.791611), (e3, 0.068697), (e5, 0.139692)) # m1 + m2 + m3 + m4
    resultChen4 = MassFunction((e2, 0.873405), (e3, 0.029212), (e5, 0.097383)) # m1 + m2 + m3 + m4 + m5

    resultDisjunctive1 = MassFunction((e3, 0.18), (e5, 0.03), (e4, 0.45), (e6, 0.05), (e7, 0.29))
    resultDisjunctive2 = MassFunction((e3, 0.018), (e5, 0.0105), (e4, 0.3915), (e6, 0.0615), (e7, 0.1965), (e8, 0.3220))
    resultDisjunctive3 = MassFunction((e3, 0.0018), (e5, 0.003675), (e4, 0.264375), (e6, 0.061125), (e7, 0.095775), (e8, 0.57325))
    resultDisjunctive4 = MassFunction((e3, 0.00018), (e5, 0.001286), (e4, 0.172834), (e6, 0.057034), (e7, 0.044096), (e8, 0.72457))

    resultDuboisPrade1 = MassFunction((e2, 0), (e3, 0.18), (e4, 0.45), (e5, 0.03), (e6, 0.05), (e7, 0.29), (e8, 0))
    resultDuboisPrade2 = MassFunction((e2, 0), (e3, 0.018), (e4, 0.3915), (e5, 0.0105), (e6, 0.0615), (e7, 0.1965), (e8, 0.322))
    resultDuboisPrade3 = MassFunction((e2, 0), (e3, 0.0018), (e4, 0.264375), (e5, 0.003675), (e6, 0.061125), (e7, 0.095775), (e8, 0.57325))
    resultDuboisPrade4 = MassFunction((e2, 0), (e3, 0.00018), (e4, 0.172834), (e5, 0.001286), (e6, 0.057034), (e7, 0.044096), (e8, 0.72457))

    resultDuboisPrade1.clean()
    resultDuboisPrade2.clean()
    resultDuboisPrade3.clean()
    resultDuboisPrade4.clean()

    function = "MassFunction.combination_dempster(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultDempster1, m1.combination_dempster, m2),
        (resultDempster2, m1.combination_dempster, m2, m3),
        (resultDempster3, m1.combination_dempster, m2, m3, m4),
        (resultDempster4, m1.combination_dempster, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.combination_dempster, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.combination_dempster, m),
        (massfunction.IncompatibleMassFunctionsError, m1.combination_dempster, mToFail),
        (None,                                        m1.combination_dempster, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    function = "MassFunction.combination_dempster_unsafe(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultDempster1, m1.combination_dempster_unsafe, m2),
        (resultDempster2, m1.combination_dempster_unsafe, m2, m3),
        (resultDempster3, m1.combination_dempster_unsafe, m2, m3, m4),
        (resultDempster4, m1.combination_dempster_unsafe, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests))) 
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.combination_yager(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultYager1, m1.combination_yager, m2),
        (resultYager2, m1.combination_yager, m2, m3),
        (resultYager3, m1.combination_yager, m2, m3, m4),
        (resultYager4, m1.combination_yager, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.combination_yager, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.combination_yager, m),
        (massfunction.IncompatibleMassFunctionsError, m1.combination_yager, mToFail),
        (None,                                        m1.combination_yager, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.combination_yager_unsafe(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultYager1, m1.combination_yager_unsafe, m2),
        (resultYager2, m1.combination_yager_unsafe, m2, m3),
        (resultYager3, m1.combination_yager_unsafe, m2, m3, m4),
        (resultYager4, m1.combination_yager_unsafe, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests))) 
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.combination_average(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultAverage1, m1.combination_average, m2),
        (resultAverage2, m1.combination_average, m2, m3),
        (resultAverage3, m1.combination_average, m2, m3, m4),
        (resultAverage4, m1.combination_average, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.combination_average, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.combination_average, m),
        (massfunction.IncompatibleMassFunctionsError, m1.combination_average, mToFail),
        (None,                                        m1.combination_average, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.combination_average_unsafe(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultAverage1, m1.combination_average_unsafe, m2),
        (resultAverage2, m1.combination_average_unsafe, m2, m3),
        (resultAverage3, m1.combination_average_unsafe, m2, m3, m4),
        (resultAverage4, m1.combination_average_unsafe, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests))) 
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.combination_murphy(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultMurphy1, m1.combination_murphy, m2),
        (resultMurphy2, m1.combination_murphy, m2, m3),
        (resultMurphy3, m1.combination_murphy, m2, m3, m4),
        (resultMurphy4, m1.combination_murphy, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.combination_murphy, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.combination_murphy, m),
        (massfunction.IncompatibleMassFunctionsError, m1.combination_murphy, mToFail),
        (None,                                        m1.combination_murphy, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")
    
    function = "MassFunction.combination_murphy_unsafe(self, *mass_function*)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultMurphy1, m1.combination_murphy_unsafe, m2),
        (resultMurphy2, m1.combination_murphy_unsafe, m2, m3),
        (resultMurphy3, m1.combination_murphy_unsafe, m2, m3, m4),
        (resultMurphy4, m1.combination_murphy_unsafe, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests))) 
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.credibility(*mass_functions)"
    print("Test of " + function + "...")

    #Taken from Chen L.-Z. et al - A new fusion approach based on distance of evidences, 2005
    expected_credibility = [0.394660, 0.250146, 0.355194]
    tests = [
        (expected_credibility, MassFunction.credibility, m1a, m2a, m3a),
    ]

    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.credibility_unsafe(*mass_functions)"
    print("Test of " + function + "...")

    #Taken from Chen L.-Z. et al - A new fusion approach based on distance of evidences, 2005
    expected_credibility = [0.394660, 0.250146, 0.355194]
    tests = [
        (expected_credibility, MassFunction.credibility_unsafe, m1a, m2a, m3a),
    ]

    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.combination_chen(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultChen0, m1a.combination_chen, m2a, m3a),
        (resultChen1, m1.combination_chen, m2),
        (resultChen2, m1.combination_chen, m2, m3),
        (resultChen3, m1.combination_chen, m2, m3, m4),
        (resultChen4, m1.combination_chen, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.combination_chen, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.combination_chen, m),
        (massfunction.IncompatibleMassFunctionsError, m1.combination_chen, mToFail),
        (None,                                        m1.combination_chen, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.combination_chen_unsafe(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultChen0, m1a.combination_chen_unsafe, m2a, m3a),
        (resultChen1, m1.combination_chen_unsafe, m2),
        (resultChen2, m1.combination_chen_unsafe, m2, m3),
        (resultChen3, m1.combination_chen_unsafe, m2, m3, m4),
        (resultChen4, m1.combination_chen_unsafe, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.combination_disjunctive(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultDisjunctive1, m1.combination_disjunctive, m2),
        (resultDisjunctive2, m1.combination_disjunctive, m2, m3),
        (resultDisjunctive3, m1.combination_disjunctive, m2, m3, m4),
        (resultDisjunctive4, m1.combination_disjunctive, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.combination_disjunctive, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.combination_disjunctive, m),
        (massfunction.IncompatibleMassFunctionsError, m1.combination_disjunctive, mToFail),
        (None,                                        m1.combination_disjunctive, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.combination_disjunctive_unsafe(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultDisjunctive1, m1.combination_disjunctive_unsafe, m2),
        (resultDisjunctive2, m1.combination_disjunctive_unsafe, m2, m3),
        (resultDisjunctive3, m1.combination_disjunctive_unsafe, m2, m3, m4),
        (resultDisjunctive4, m1.combination_disjunctive_unsafe, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.combination_dubois_prade(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultDuboisPrade1, m1.combination_dubois_prade, m2),
        (resultDuboisPrade2, m1.combination_dubois_prade, m2, m3),
        (resultDuboisPrade3, m1.combination_dubois_prade, m2, m3, m4),
        (resultDuboisPrade4, m1.combination_dubois_prade, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    mToFail = MassFunction((DiscreteElement(4, 1), 1))
    
    tests = [
        (TypeError,                                   m1.combination_dubois_prade, 0.5),
        (massfunction.EmptyMassFunctionError,         m1.combination_dubois_prade, m),
        (massfunction.IncompatibleMassFunctionsError, m1.combination_dubois_prade, mToFail),
        (None,                                        m1.combination_dubois_prade, m2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.combination_dubois_prade_unsafe(self, *mass_functions)"
    print("Test of " + function + " ...")
    
    tests = [
        (resultDuboisPrade1, m1.combination_dubois_prade_unsafe, m2),
        (resultDuboisPrade2, m1.combination_dubois_prade_unsafe, m2, m3),
        (resultDuboisPrade3, m1.combination_dubois_prade_unsafe, m2, m3, m4),
        (resultDuboisPrade4, m1.combination_dubois_prade_unsafe, m2, m3, m4, m5),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "MassFunction.auto_conflict(self, degree)"
    print("Test of " + function + " ...")

    m1 = MassFunction((e2, 1))
    m2 = MassFunction((e2, 0.5), (e3, 0.5))
    m3 = MassFunction((e2, 0.5), (e4, 0.5))
    m4 = MassFunction((e2, 0.25), (e3, 0.5), (e4, 0.25))
    m5 = MassFunction((e2, 0.25), (e3, 0.25), (e5, 0.5))
    m6 = MassFunction((e4, 0.25), (e6, 0.25), (e7, 0.25), (e8, 0.25))

    result1 = [0, 0, 0]
    result2 = [0.5, 0.75, 0.875]
    result3 = [0, 0, 0]
    result4 = [0.25, 0.46875, 0.625]
    result5 = [0.625, 0.84375, 0.9296875]
    result6 = [0, 0.09375, 0.234375]
    
    tests = [
        (result1, m1.auto_conflict, 3),
        (result2, m2.auto_conflict, 3),
        (result3, m3.auto_conflict, 3),
        (result4, m4.auto_conflict, 3),
        (result5, m5.auto_conflict, 3),
        (result6, m6.auto_conflict, 3),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    nbFailed = len(errors)
    nbTests = len(tests)

    m = MassFunction()
    
    tests = [
        (ValueError,                                  m1.auto_conflict, 0.5),
        (ValueError,                                  m1.auto_conflict, 0),
        (massfunction.EmptyMassFunctionError,         m.auto_conflict,  3),
        (None,                                        m1.auto_conflict, 2)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        if function in failed:
            failed[function].extend(errors)
        else:
            failed[function] = errors
    nbFailed += len(errors)
    nbTests += len(tests)
    print("... done: %i/%i tests were successful!" % (nbTests - nbFailed, nbTests))
        
    ################################################################################
    print('\n')
    tests_utility.browse_failures(failed)
        
