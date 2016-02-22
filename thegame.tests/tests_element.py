#!/usr/bin/python3

################################################################################
# thegame.tests_element.py                                                     #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@cit.ie                                          #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module only provides a main that executes short tests to check that     #
# methods of element.py provide expected results.                              #
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
    
    print(
        "*" * 80 + "\n" +
        "*" + "{:^78}".format(os.path.basename(__file__)) + "*\n" +
        "*" * 80
    )

    # A dictionary with function names as keys and a list of calls that failed for each one of them
    # in the form ("call_that_failed()", "reason", exception if there's one (can be None))
    failed = {}

    ##########################
    # TESTS: DiscreteElement #
    ##########################

    function = "DiscreteElement.__init__(self, size, number=0)"
    print("Test of " + function + " ...")

    #(function_to_call, expected_exception)
    tests = [
        (ValueError,                             element.DiscreteElement, 0, 2),
        (element.IncompatibleSizeAndNumberError, element.DiscreteElement, 2, 5),
        (None,                                   element.DiscreteElement, 3, 4)
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "DiscreteElement.factory_from_str(self, bstr, bigendian=True)"
    print("Test of " + function + "...")
    tests = [
        (None,       element.DiscreteElement.factory_from_str, '1001'),
        (ValueError, element.DiscreteElement.factory_from_str, '100110sfsd'),
        (ValueError, element.DiscreteElement.factory_from_str, '1000123442'),
        (None,       element.DiscreteElement.factory_from_str, '1001', False),
        (ValueError, element.DiscreteElement.factory_from_str, '100110sfsd', False),
        (ValueError, element.DiscreteElement.factory_from_str, '1000123442', False),
        (None,       element.DiscreteElement.factory_from_str, '1010101010101010101010101010101010101010101010100001010101010101') #Test for very big numbers
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "DiscreteElement.factory_from_ref_list(self, ref_list, *states)"
    print("Test of " + function + "...")

    ref_list      = ("Aka", "Bea", "Car", "Dib")
    ref_list_fail = ("Aka", "Bea", "Aka", "Car")

    states      = ("Aka",)
    states2     = ("Bea", "Aka")
    statesFail  = ("Dub",)
    statesFail2 = ("Aka", "Car", "Dub")
    
    tests = [
        (None,       element.DiscreteElement.factory_from_ref_list, ref_list) + states,
        (None,       element.DiscreteElement.factory_from_ref_list, ref_list) + states2,
        (ValueError, element.DiscreteElement.factory_from_ref_list, ref_list) + statesFail,
        (ValueError, element.DiscreteElement.factory_from_ref_list, ref_list) + statesFail2,
        (ValueError, element.DiscreteElement.factory_from_ref_list, ref_list_fail) + states,
        (ValueError, element.DiscreteElement.factory_from_ref_list, ref_list_fail) + states2,
        (ValueError, element.DiscreteElement.factory_from_ref_list, ref_list_fail) + statesFail
    ]
    errors = tests_utility.exception_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "str(DiscreteElement) / DiscreteElement.__str__(self)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1)),
        ("010",      str, element.DiscreteElement(3, 2)),
        ("011",      str, element.DiscreteElement(3, 3)),
        ("100",      str, element.DiscreteElement(3, 4)),
        ("101",      str, element.DiscreteElement(3, 5)),
        ("110",      str, element.DiscreteElement(3, 6)),
        ("111",      str, element.DiscreteElement(3, 7)),
        ("00111",    str, element.DiscreteElement(5, 7)),
        ("01001",    str, element.DiscreteElement(5, 9)),
        ("10000010", str, element.DiscreteElement(8, 130)),

        ("1100", str, element.DiscreteElement.factory_from_str('1100')),
        ("1100", str, element.DiscreteElement.factory_from_str('0011', False)),
        ("11001101", str, element.DiscreteElement.factory_from_str('11001101')),
        ("10110011", str, element.DiscreteElement.factory_from_str('11001101', False))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.formatted_str(self, *references)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        ("{}",                element.DiscreteElement(3, 0).formatted_str, 'Aka', 'Bea', 'Car'),
        ("{Aka}",             element.DiscreteElement(3, 1).formatted_str, 'Aka', 'Bea', 'Car'),
        ("{Bea}",             element.DiscreteElement(3, 2).formatted_str, 'Aka', 'Bea', 'Car'),
        ("{Aka u Bea}",       element.DiscreteElement(3, 3).formatted_str, 'Aka', 'Bea', 'Car'),
        ("{Car}",             element.DiscreteElement(3, 4).formatted_str, 'Aka', 'Bea', 'Car'),
        ("{Aka u Car}",       element.DiscreteElement(3, 5).formatted_str, 'Aka', 'Bea', 'Car'),
        ("{Bea u Car}",       element.DiscreteElement(3, 6).formatted_str, 'Aka', 'Bea', 'Car'),
        ("{Aka u Bea u Car}", element.DiscreteElement(3, 7).formatted_str, 'Aka', 'Bea', 'Car'),

        ("{}",                element.DiscreteElement.factory_from_str('0000').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Aka}",             element.DiscreteElement.factory_from_str('0001').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Bea}",             element.DiscreteElement.factory_from_str('0010').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Aka u Bea}",       element.DiscreteElement.factory_from_str('0011').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Car}",             element.DiscreteElement.factory_from_str('0100').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Aka u Car}",       element.DiscreteElement.factory_from_str('0101').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Bea u Car}",       element.DiscreteElement.factory_from_str('0110').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Aka u Bea u Car}", element.DiscreteElement.factory_from_str('0111').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Dib}",             element.DiscreteElement.factory_from_str('1000').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Aka u Dib}",       element.DiscreteElement.factory_from_str('1001').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Bea u Dib}",       element.DiscreteElement.factory_from_str('1010').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        ("{Aka u Bea u Dib}", element.DiscreteElement.factory_from_str('1011').formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                                element.DiscreteElement(3, 0).formatted_str, 'Aka', 'Bea', 'Car'),
        (element.IncompatibleReferencesError, element.DiscreteElement(3, 0).formatted_str, 'Aka', 'Bea'),
        (element.IncompatibleReferencesError, element.DiscreteElement(3, 0).formatted_str, 'Aka', 'Bea', 'Car', 'Dib'),
        (ValueError,                          element.DiscreteElement(3, 0).formatted_str, 'Aka', 'Bea', 'Aka')
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
    
    function = "DiscreteElement.cardinal(self)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        (1, element.DiscreteElement(3, 1),   "cardinal"),
        (1, element.DiscreteElement(3, 2),   "cardinal"),
        (2, element.DiscreteElement(3, 3),   "cardinal"),
        (1, element.DiscreteElement(3, 4),   "cardinal"),
        (2, element.DiscreteElement(3, 5),   "cardinal"),
        (2, element.DiscreteElement(3, 6),   "cardinal"),
        (3, element.DiscreteElement(3, 7),   "cardinal"),
        (3, element.DiscreteElement(5, 7),   "cardinal"),
        (2, element.DiscreteElement(5, 9),   "cardinal"),
        (2, element.DiscreteElement(8, 130), "cardinal"),

        (2, element.DiscreteElement.factory_from_str('1100'),            "cardinal"),
        (2, element.DiscreteElement.factory_from_str('0011', False),     "cardinal"),
        (5, element.DiscreteElement.factory_from_str('11001101'),        "cardinal"),
        (5, element.DiscreteElement.factory_from_str('11001101', False), "cardinal")
    ]
    errors = tests_utility.expected_property_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.opposite(self)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("110",      str, element.DiscreteElement(3, 1).opposite()),
        ("101",      str, element.DiscreteElement(3, 2).opposite()),
        ("100",      str, element.DiscreteElement(3, 3).opposite()),
        ("011",      str, element.DiscreteElement(3, 4).opposite()),
        ("010",      str, element.DiscreteElement(3, 5).opposite()),
        ("001",      str, element.DiscreteElement(3, 6).opposite()),
        ("000",      str, element.DiscreteElement(3, 7).opposite()),
        ("11000",    str, element.DiscreteElement(5, 7).opposite()),
        ("10110",    str, element.DiscreteElement(5, 9).opposite()),
        ("01111101", str, element.DiscreteElement(8, 130).opposite()),

        ("0011",     str, element.DiscreteElement.factory_from_str('1100').opposite()),
        ("0011",     str, element.DiscreteElement.factory_from_str('0011', False).opposite()),
        ("00110010", str, element.DiscreteElement.factory_from_str('11001101').opposite()),
        ("01001100", str, element.DiscreteElement.factory_from_str('11001101', False).opposite())
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "~e / DiscreteElement.__invert__(self)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("110",      str, ~element.DiscreteElement(3, 1)),
        ("101",      str, ~element.DiscreteElement(3, 2)),
        ("100",      str, ~element.DiscreteElement(3, 3)),
        ("011",      str, ~element.DiscreteElement(3, 4)),
        ("010",      str, ~element.DiscreteElement(3, 5)),
        ("001",      str, ~element.DiscreteElement(3, 6)),
        ("000",      str, ~element.DiscreteElement(3, 7)),
        ("11000",    str, ~element.DiscreteElement(5, 7)),
        ("10110",    str, ~element.DiscreteElement(5, 9)),
        ("01111101", str, ~element.DiscreteElement(8, 130)),

        ("0011",     str, ~element.DiscreteElement.factory_from_str('1100')),
        ("0011",     str, ~element.DiscreteElement.factory_from_str('0011', False)),
        ("00110010", str, ~element.DiscreteElement.factory_from_str('11001101')),
        ("01001100", str, ~element.DiscreteElement.factory_from_str('11001101', False))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.exclusion(self, element)"
    print("Test of " + function + " ...")

    e1  = element.DiscreteElement.factory_from_str('0000')
    e2  = element.DiscreteElement.factory_from_str('0001')
    e3  = element.DiscreteElement.factory_from_str('0010')
    e4  = element.DiscreteElement.factory_from_str('0011')
    e5  = element.DiscreteElement.factory_from_str('0100')
    e6  = element.DiscreteElement.factory_from_str('0101')
    e7  = element.DiscreteElement.factory_from_str('0110')
    e8  = element.DiscreteElement.factory_from_str('0111')
    e9  = element.DiscreteElement.factory_from_str('1000')
    e10 = element.DiscreteElement.factory_from_str('1001')
    e11 = element.DiscreteElement.factory_from_str('1010')
    e12 = element.DiscreteElement.factory_from_str('1011')
    
    tests = [
        ("1011",      str, e12.exclusion(e1)),
        ("1010",      str, e12.exclusion(e2)),
        ("1001",      str, e12.exclusion(e3)),
        ("1011",      str, e12.exclusion(e1)),
        ("0001",      str, e10.exclusion(e9)),
        ("0010",      str, e8.exclusion(e6)),
        ("1000",      str, e9.exclusion(e2)),
        ("0000",      str, e4.exclusion(e8)),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "e1 - e2 / DiscreteElement.__sub__(self, element)"
    print("Test of " + function + " ...")

    e1  = element.DiscreteElement.factory_from_str('0000')
    e2  = element.DiscreteElement.factory_from_str('0001')
    e3  = element.DiscreteElement.factory_from_str('0010')
    e4  = element.DiscreteElement.factory_from_str('0011')
    e5  = element.DiscreteElement.factory_from_str('0100')
    e6  = element.DiscreteElement.factory_from_str('0101')
    e7  = element.DiscreteElement.factory_from_str('0110')
    e8  = element.DiscreteElement.factory_from_str('0111')
    e9  = element.DiscreteElement.factory_from_str('1000')
    e10 = element.DiscreteElement.factory_from_str('1001')
    e11 = element.DiscreteElement.factory_from_str('1010')
    e12 = element.DiscreteElement.factory_from_str('1011')
    
    tests = [
        ("1011",      str, e12 - e1),
        ("1010",      str, e12 - e2),
        ("1001",      str, e12 - e3),
        ("1011",      str, e12 - e1),
        ("0001",      str, e10 - e9),
        ("0010",      str, e8 - e6),
        ("1000",      str, e9 - e2),
        ("0000",      str, e4 - e8),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.conjunction(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1).conjunction(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 2).conjunction(element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 3).conjunction(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 4).conjunction(element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 5).conjunction(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 6).conjunction(element.DiscreteElement(3, 1))),
        ("110",      str, element.DiscreteElement(3, 7).conjunction(element.DiscreteElement(3, 6))),
        ("00000",    str, element.DiscreteElement(5, 7).conjunction(element.DiscreteElement(5, 8))),
        ("00001",    str, element.DiscreteElement(5, 9).conjunction(element.DiscreteElement(5, 7))),
        ("10000000", str, element.DiscreteElement(8, 130).conjunction(element.DiscreteElement(8, 128))),

        ("1000",     str, element.DiscreteElement.factory_from_str('1100').conjunction(element.DiscreteElement(4, 11))),
        ("00001101", str, element.DiscreteElement.factory_from_str('11001101').conjunction(element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).conjunction, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).conjunction, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').conjunction, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').conjunction, element.DiscreteElement(6, 11))
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

    function = "DiscreteElement.conjunction_unsafe(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1).conjunction_unsafe(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 2).conjunction_unsafe(element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 3).conjunction_unsafe(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 4).conjunction_unsafe(element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 5).conjunction_unsafe(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 6).conjunction_unsafe(element.DiscreteElement(3, 1))),
        ("110",      str, element.DiscreteElement(3, 7).conjunction_unsafe(element.DiscreteElement(3, 6))),
        ("00000",    str, element.DiscreteElement(5, 7).conjunction_unsafe(element.DiscreteElement(5, 8))),
        ("00001",    str, element.DiscreteElement(5, 9).conjunction_unsafe(element.DiscreteElement(5, 7))),
        ("10000000", str, element.DiscreteElement(8, 130).conjunction_unsafe(element.DiscreteElement(8, 128))),

        ("1000",     str, element.DiscreteElement.factory_from_str('1100').conjunction_unsafe(element.DiscreteElement(4, 11))),
        ("00001101", str, element.DiscreteElement.factory_from_str('11001101').conjunction_unsafe(element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.intersection(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1).intersection(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 2).intersection(element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 3).intersection(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 4).intersection(element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 5).intersection(element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 6).intersection(element.DiscreteElement(3, 1))),
        ("110",      str, element.DiscreteElement(3, 7).intersection(element.DiscreteElement(3, 6))),
        ("00000",    str, element.DiscreteElement(5, 7).intersection(element.DiscreteElement(5, 8))),
        ("00001",    str, element.DiscreteElement(5, 9).intersection(element.DiscreteElement(5, 7))),
        ("10000000", str, element.DiscreteElement(8, 130).intersection(element.DiscreteElement(8, 128))),

        ("1000",     str, element.DiscreteElement.factory_from_str('1100').intersection(element.DiscreteElement(4, 11))),
        ("00001101", str, element.DiscreteElement.factory_from_str('11001101').intersection(element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).intersection, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).intersection, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').intersection, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').intersection, element.DiscreteElement(6, 11))
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
    
    function = "e1 * e2 / DiscreteElement.__mul__(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1) * (element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 2) * (element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 3) * (element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 4) * (element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 5) * (element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 6) * (element.DiscreteElement(3, 1))),
        ("110",      str, element.DiscreteElement(3, 7) * (element.DiscreteElement(3, 6))),
        ("00000",    str, element.DiscreteElement(5, 7) * (element.DiscreteElement(5, 8))),
        ("00001",    str, element.DiscreteElement(5, 9) * (element.DiscreteElement(5, 7))),
        ("10000000", str, element.DiscreteElement(8, 130) * (element.DiscreteElement(8, 128))),

        ("1000",     str, element.DiscreteElement.factory_from_str('1100') * (element.DiscreteElement(4, 11))),
        ("00001101", str, element.DiscreteElement.factory_from_str('11001101') * (element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).__mul__, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).__mul__, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').__mul__, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').__mul__, element.DiscreteElement(6, 11))
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
    
    function = "e1 & e2 / DiscreteElement.__and__(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1) & (element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 2) & (element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 3) & (element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 4) & (element.DiscreteElement(3, 1))),
        ("001",      str, element.DiscreteElement(3, 5) & (element.DiscreteElement(3, 1))),
        ("000",      str, element.DiscreteElement(3, 6) & (element.DiscreteElement(3, 1))),
        ("110",      str, element.DiscreteElement(3, 7) & (element.DiscreteElement(3, 6))),
        ("00000",    str, element.DiscreteElement(5, 7) & (element.DiscreteElement(5, 8))),
        ("00001",    str, element.DiscreteElement(5, 9) & (element.DiscreteElement(5, 7))),
        ("10000000", str, element.DiscreteElement(8, 130) & (element.DiscreteElement(8, 128))),

        ("1000",     str, element.DiscreteElement.factory_from_str('1100') & (element.DiscreteElement(4, 11))),
        ("00001101", str, element.DiscreteElement.factory_from_str('11001101') & (element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).__and__, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).__and__, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').__and__, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').__and__, element.DiscreteElement(6, 11))
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
    
    function = "DiscreteElement.disjunction(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1).disjunction(element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 2).disjunction(element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 3).disjunction(element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 4).disjunction(element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 5).disjunction(element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 6).disjunction(element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 7).disjunction(element.DiscreteElement(3, 6))),
        ("01111",    str, element.DiscreteElement(5, 7).disjunction(element.DiscreteElement(5, 8))),
        ("01111",    str, element.DiscreteElement(5, 9).disjunction(element.DiscreteElement(5, 7))),
        ("10000010", str, element.DiscreteElement(8, 130).disjunction(element.DiscreteElement(8, 128))),

        ("1111",     str, element.DiscreteElement.factory_from_str('1100').disjunction(element.DiscreteElement(4, 11))),
        ("11001101", str, element.DiscreteElement.factory_from_str('11001101').disjunction(element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).disjunction, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).disjunction, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').disjunction, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').disjunction, element.DiscreteElement(6, 11))
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

    function = "DiscreteElement.disjunction_unsafe(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1).disjunction_unsafe(element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 2).disjunction_unsafe(element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 3).disjunction_unsafe(element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 4).disjunction_unsafe(element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 5).disjunction_unsafe(element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 6).disjunction_unsafe(element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 7).disjunction_unsafe(element.DiscreteElement(3, 6))),
        ("01111",    str, element.DiscreteElement(5, 7).disjunction_unsafe(element.DiscreteElement(5, 8))),
        ("01111",    str, element.DiscreteElement(5, 9).disjunction_unsafe(element.DiscreteElement(5, 7))),
        ("10000010", str, element.DiscreteElement(8, 130).disjunction_unsafe(element.DiscreteElement(8, 128))),

        ("1111",     str, element.DiscreteElement.factory_from_str('1100').disjunction_unsafe(element.DiscreteElement(4, 11))),
        ("11001101", str, element.DiscreteElement.factory_from_str('11001101').disjunction_unsafe(element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")

    function = "DiscreteElement.union(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1).union(element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 2).union(element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 3).union(element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 4).union(element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 5).union(element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 6).union(element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 7).union(element.DiscreteElement(3, 6))),
        ("01111",    str, element.DiscreteElement(5, 7).union(element.DiscreteElement(5, 8))),
        ("01111",    str, element.DiscreteElement(5, 9).union(element.DiscreteElement(5, 7))),
        ("10000010", str, element.DiscreteElement(8, 130).union(element.DiscreteElement(8, 128))),

        ("1111",     str, element.DiscreteElement.factory_from_str('1100').union(element.DiscreteElement(4, 11))),
        ("11001101", str, element.DiscreteElement.factory_from_str('11001101').union(element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).union, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).union, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').union, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').union, element.DiscreteElement(6, 11))
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
    
    function = "e1 + e2 / DiscreteElement.__add__(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1) + (element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 2) + (element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 3) + (element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 4) + (element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 5) + (element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 6) + (element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 7) + (element.DiscreteElement(3, 6))),
        ("01111",    str, element.DiscreteElement(5, 7) + (element.DiscreteElement(5, 8))),
        ("01111",    str, element.DiscreteElement(5, 9) + (element.DiscreteElement(5, 7))),
        ("10000010", str, element.DiscreteElement(8, 130) + (element.DiscreteElement(8, 128))),

        ("1111",     str, element.DiscreteElement.factory_from_str('1100') + (element.DiscreteElement(4, 11))),
        ("11001101", str, element.DiscreteElement.factory_from_str('11001101') + (element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).__add__, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).__add__, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').__add__, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').__add__, element.DiscreteElement(6, 11))
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
    
    function = "e1 | e2 / DiscreteElement.__or__(self, element)"
    print("Test of " + function + " ...")
    #(function_to_call, expected_output)
    tests = [
        ("001",      str, element.DiscreteElement(3, 1) | (element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 2) | (element.DiscreteElement(3, 1))),
        ("011",      str, element.DiscreteElement(3, 3) | (element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 4) | (element.DiscreteElement(3, 1))),
        ("101",      str, element.DiscreteElement(3, 5) | (element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 6) | (element.DiscreteElement(3, 1))),
        ("111",      str, element.DiscreteElement(3, 7) | (element.DiscreteElement(3, 6))),
        ("01111",    str, element.DiscreteElement(5, 7) | (element.DiscreteElement(5, 8))),
        ("01111",    str, element.DiscreteElement(5, 9) | (element.DiscreteElement(5, 7))),
        ("10000010", str, element.DiscreteElement(8, 130) | (element.DiscreteElement(8, 128))),

        ("1111",     str, element.DiscreteElement.factory_from_str('1100') | (element.DiscreteElement(4, 11))),
        ("11001101", str, element.DiscreteElement.factory_from_str('11001101') | (element.DiscreteElement(8, 13)))
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
        
    nbFailed = len(errors)
    nbTests = len(tests)

    tests = [
        (None,                              element.DiscreteElement(3, 1).__or__, element.DiscreteElement(3, 3)),
        (element.IncompatibleElementsError, element.DiscreteElement(3, 1).__or__, element.DiscreteElement(5, 1)),
        (None,                              element.DiscreteElement.factory_from_str('1100').__or__, element.DiscreteElement(4, 11)),
        (element.IncompatibleElementsError, element.DiscreteElement.factory_from_str('1100').__or__, element.DiscreteElement(6, 11))
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
    
    function = "DiscreteElement.get_compatible_empty_element(self)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        ("000",      str, element.DiscreteElement(3, 1).get_compatible_empty_element()),
        ("000",      str, element.DiscreteElement(3, 2).get_compatible_empty_element()),
        ("00000",    str, element.DiscreteElement(5, 7).get_compatible_empty_element()),
        ("00000",    str, element.DiscreteElement(5, 9).get_compatible_empty_element()),
        ("00000000", str, element.DiscreteElement(8, 130).get_compatible_empty_element()),

        ("0000",     str, element.DiscreteElement.factory_from_str('1100').get_compatible_empty_element()),
        ("0000",     str, element.DiscreteElement.factory_from_str('0011', False).get_compatible_empty_element()),
        ("00000000", str, element.DiscreteElement.factory_from_str('11001101').get_compatible_empty_element()),
        ("00000000", str, element.DiscreteElement.factory_from_str('11001101', False).get_compatible_empty_element())
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.get_compatible_complete_element(self)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        ("111",      str, element.DiscreteElement(3, 1).get_compatible_complete_element()),
        ("111",      str, element.DiscreteElement(3, 2).get_compatible_complete_element()),
        ("11111",    str, element.DiscreteElement(5, 7).get_compatible_complete_element()),
        ("11111",    str, element.DiscreteElement(5, 9).get_compatible_complete_element()),
        ("11111111", str, element.DiscreteElement(8, 130).get_compatible_complete_element()),

        ("1111",     str, element.DiscreteElement.factory_from_str('1100').get_compatible_complete_element()),
        ("1111",     str, element.DiscreteElement.factory_from_str('0011', False).get_compatible_complete_element()),
        ("11111111", str, element.DiscreteElement.factory_from_str('11001101').get_compatible_complete_element()),
        ("11111111", str, element.DiscreteElement.factory_from_str('11001101', False).get_compatible_complete_element())
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.is_empty(self)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        (False, element.DiscreteElement(3,   1).is_empty),
        (True,  element.DiscreteElement(3,   0).is_empty),
        (True,  element.DiscreteElement(5,   0).is_empty),
        (False, element.DiscreteElement(5,   9).is_empty),
        (False, element.DiscreteElement(8, 130).is_empty),
        (True,  element.DiscreteElement(8,   0).is_empty),

        (False, element.DiscreteElement.factory_from_str('1100').is_empty),
        (True,  element.DiscreteElement.factory_from_str('0000').is_empty),
        (False, element.DiscreteElement.factory_from_str('0011', False).is_empty),
        (True,  element.DiscreteElement.factory_from_str('0000', False).is_empty),
        (False, element.DiscreteElement.factory_from_str('11001101').is_empty),
        (True,  element.DiscreteElement.factory_from_str('00000000').is_empty),
        (False, element.DiscreteElement.factory_from_str('11001101', False).is_empty),
        (True,  element.DiscreteElement.factory_from_str('00000000', False).is_empty)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.is_complete(self)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        (False, element.DiscreteElement(3, 1).is_complete),
        (True,  element.DiscreteElement(3, 7).is_complete),
        (True,  element.DiscreteElement(5, 31).is_complete),
        (False, element.DiscreteElement(5, 9).is_complete),
        (False, element.DiscreteElement(8, 130).is_complete),
        (True,  element.DiscreteElement(8, 255).is_complete),

        (False, element.DiscreteElement.factory_from_str('1100').is_complete),
        (True,  element.DiscreteElement.factory_from_str('1111').is_complete),
        (False, element.DiscreteElement.factory_from_str('0011', False).is_complete),
        (True,  element.DiscreteElement.factory_from_str('1111', False).is_complete),
        (False, element.DiscreteElement.factory_from_str('11001101').is_complete),
        (True,  element.DiscreteElement.factory_from_str('11111111').is_complete),
        (False, element.DiscreteElement.factory_from_str('11001101', False).is_complete),
        (True,  element.DiscreteElement.factory_from_str('11111111', False).is_complete)
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.is_subset(self, element)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        (True,  element.DiscreteElement(3, 0).is_subset, element.DiscreteElement(3, 1)),
        (False, element.DiscreteElement(3, 0).is_subset, element.DiscreteElement(5, 31)),
        (False, element.DiscreteElement(5, 0).is_subset, element.DiscreteElement(3, 1)),
        (True,  element.DiscreteElement(5, 0).is_subset, element.DiscreteElement(5, 31)),
        (True,  element.DiscreteElement(3, 0).is_subset, element.DiscreteElement(3, 3)),
        (False, element.DiscreteElement(3, 0).is_subset, element.DiscreteElement(5, 12)),
        (False, element.DiscreteElement(5, 0).is_subset, element.DiscreteElement(3, 3)),
        (True,  element.DiscreteElement(5, 0).is_subset, element.DiscreteElement(5, 12)),

        (False, element.DiscreteElement.factory_from_str('1100').is_subset, element.DiscreteElement.factory_from_str('1010')),
        (True,  element.DiscreteElement.factory_from_str('1100').is_subset, element.DiscreteElement.factory_from_str('1110')),
        (False, element.DiscreteElement.factory_from_str('11001101').is_subset, element.DiscreteElement.factory_from_str('10111101')),
        (True,  element.DiscreteElement.factory_from_str('11001101').is_subset, element.DiscreteElement.factory_from_str('11011111')),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    print("--------------------------------------------------------------------------------")
    
    function = "DiscreteElement.is_superset(self, element)"
    print("Test of " + function + " ...")
    
    #(function_to_call, expected_output)
    tests = [
        (False, element.DiscreteElement(3, 0).is_superset, element.DiscreteElement(3, 1)),
        (False, element.DiscreteElement(3, 0).is_superset, element.DiscreteElement(3, 3)),
        (True,  element.DiscreteElement(3, 0).is_superset, element.DiscreteElement(3, 0)),
        (False, element.DiscreteElement(5, 0).is_superset, element.DiscreteElement(3, 1)),
        (False, element.DiscreteElement(5, 0).is_superset, element.DiscreteElement(5, 1)),
        (True,  element.DiscreteElement(5, 0).is_superset, element.DiscreteElement(5, 0)),

        (False, element.DiscreteElement.factory_from_str('1100').is_superset, element.DiscreteElement.factory_from_str('1010')),
        (True,  element.DiscreteElement.factory_from_str('1100').is_superset, element.DiscreteElement.factory_from_str('1000')),
        (False, element.DiscreteElement.factory_from_str('11001101').is_superset, element.DiscreteElement.factory_from_str('10111101')),
        (True,  element.DiscreteElement.factory_from_str('11011111').is_superset, element.DiscreteElement.factory_from_str('11001101')),
    ]
    errors = tests_utility.expected_output_test(tests, False)
    if len(errors) != 0:
        failed[function] = errors
    print("... done: %i/%i tests were successful!" % (len(tests)-len(errors), len(tests)))
    
    ################################################################################
    
    print('\n')
    tests_utility.browse_failures(failed)
