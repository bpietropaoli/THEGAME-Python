################################################################################
# thegame.tests_utility.py                                                     #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@cit.ie                                          #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module provides some functions to better handle tests provided in the   #
# main of each module. Nothing fancy, but hey, it facilitates a bit the job.   #
################################################################################


def expected_output_test(tests, verbose=True):
    """
    Runs tests, check the expected output and list the failures. Prints things
    in the console if put in verbose mode.

    Args:
        tests (list[(expected_output, function_to_call, *args)]): The list of tests to
            run in the form of a list of tuples containing in order:
                - expected_output: The expected output.
                - function_to_call: The function to call.
                - *args: The args for the function to call.
        verbose (bool): If ``True``, prints results in the console, prints nothing
            otherwise.
    Returns:
        list[(function_called, str_failure_description, exception)] -- The list of
        failures that occurred within the conducted tests.

    test: (expected_output, function, *args)
    """

    failed = []
    
    for test in tests:
        expected_output = test[0]
        function = test[1]
        if not hasattr(function, '__call__'):
            raise ValueError("The second object in the provided test tuples should be callable!")
        args = test[2:]
        s = ""
        try:
            s += str(function.__self__) + "."
        except:
            pass
        try:
            s += function.__name__ + "("
        except:
            s += str(function).split(' ')[1][1:-2] + "("
        for arg in args:
            s += str(arg) + ", "
        s = s[:-2] + ")"
        try:
            if verbose:
                print(" ... " + s)
                print("   - Expected output: " + str(expected_output))
            result = function(*args)
            if verbose:
                print("   - Real output    : " + str(result))
            assert result == expected_output, ("Output " + str(result) +
                                        " instead of the expected " + str(expected_output) + "!")
            if verbose:
                print("  ... SUCCESS.")
        except AssertionError as e:
            if verbose:
                print("  ... FAILED: not the expected output value!")
            failed.append((s, "Not the expected value!", e))
        except Exception as e:
            if verbose:
                print("  ... FAILED: raised an unexpected exception!")
            failed.append((s, "Raised an unexpected exception!", e))

    if verbose:
        print("... done: %i/%i tests were successful!" % (len(tests)-len(failed), len(tests)))
    
    return failed

################################################################################

def expected_property_test(tests, verbose=True):
    """
    Runs tests, check the expected output and list the failures. Prints things
    in the console if put in verbose mode.

    Args:
        tests (list[(expected_output, object, property)]): The list of tests to
            run in the form of a list of tuples containing in order:
                - expected_output: The expected output.
                - object: The object on which the property will be accessed.
                - property: The name (as a string) of the porperty to access.
        verbose (bool): If ``True``, prints results in the console, prints nothing
            otherwise.
    Returns:
        list[(function_called, str_failure_description, exception)] -- The list of
        failures that occurred within the conducted tests.

    test: (expected_output, function, *args)
    """

    failed = []
    
    for test in tests:
        expected_output = test[0]
        obj = test[1]
        prop = test[2]
        s = str(obj) + "." + prop
        try:
            if verbose:
                print(" ... " + s)
                print("   - Expected output: " + str(expected_output))
            result = getattr(obj, prop)
            if verbose:
                print("   - Real output    : " + str(result))
            assert result == expected_output, ("Output " + str(result) +
                                        " instead of the expected " + str(expected_output) + "!")
            if verbose:
                print("  ... SUCCESS.")
        except AssertionError as e:
            if verbose:
                print("  ... FAILED: not the expected output value!")
            failed.append((s, "Not the expected value!", e))
        except Exception as e:
            if verbose:
                print("  ... FAILED: raised an unexpected exception!")
            failed.append((s, "Raised an unexpected exception!", e))

    if verbose:
        print("... done: %i/%i tests were successful!" % (len(tests)-len(failed), len(tests)))
    
    return failed

################################################################################

def exception_test(tests, verbose=True):
    """
    Runs tests, checks if the expected exceptions are raised and list the failures.
    Prints things in the console if put in verbose mode.

    Args:
        tests (list[(expected_exception, function_to_call, *args)]): The list of tests to
            run in the form of a list of tuples containing in order:
                - expected_exception: The exception excetion to be raised.
                - function_to_call: The function to call.
                - *args: The arguments for the function.
        verbose (bool): If ``True``, prints results in the console, prints nothing
            otherwise.

    Returns:
        list[(function_called, str_failure_description, exception)] -- The list of
        failures that occurred within the conducted tests.
    """

    failed = []
    
    for test in tests:
        expected_exception = test[0]
        function = test[1]
        if not hasattr(function, '__call__'):
            raise ValueError("The second object in the provided test tuples should be callable!")
        args = test[2:]
        s = ""
        try:
            s += str(function.__self__) + "."
        except:
            pass
        try:
            s += function.__name__ + "("
        except:
            s += str(function).split(' ')[1][1:-2] + "("
        for arg in args:
            s += str(arg) + ", "
        s = s[:-2] + ")"
        
        #None would raise a type error exception when trying to catch the exception.
        if expected_exception == None:
            try:
                if verbose:
                    print(" ... " + s)
                function(*args)
                if verbose:
                        print("  ... SUCCESS: as expected, no exception was raised.")
            except Exception as e:
                if verbose:
                    print("  ... FAILED: an unexpected exception was raised while none was expected!")
                failed.append((s, "An unexpected exception was raised while none was expected!", e))
        else:
            try:
                if verbose:
                    print(" ... " + s)
                function(*args)
                if verbose:
                    print("  ... FAILED: an exception of type " + expected_exception.__name__ +
                          " was expected but none was raised!")
                failed.append((s, "Should have raised a " + expected_exception.__name__ +
                                        " exception!", None))
            except expected_exception as e:
                if verbose:
                    print("  ... SUCCESS: it raised the expected " + expected_exception.__name__ + " exception.")
            except Exception as e:
                if verbose:
                    print("  ... FAILED: it raised an unexpected exception; should have raised a " +
                            expected_exception.__name__ + " exception!")
                failed.append((s, "It raised an unexpected exception; should have raised a " +
                                        expected_exception.__name__ + " exception!", e))
    
    if verbose:
        print("... done: %i/%i tests were successful!" % (len(tests)-len(failed), len(tests)))
        
    return failed

################################################################################

def modifying_method_test(tests, verbose=True):
    """
    Runs tests for modifying methods, checks if the string corresponding
    to the modified object corresponds to the expected string representation.

    Args:
        tests (list[(expected_str, function_to_call, *args)]): The list of tests to
            run in the form of a list of tuples containing in order:
                - expected_str: The expected string representation of the object after modification;
                - function_to_call: The function to call, should be bound to an object;
                - *args: The arguments for the function.

            Calls ``object.function_to_call(*args)``.
            
            Do not forget that the methods here modify the object, thus, if you always
            provide the same object to all tests, you have to take into account the
            modification made by each call.
        verbose (bool): If ``True``, prints results in the console, prints nothing
            otherwise.

    Returns:
        list[(function_called, str_failure_description, exception)] -- The list of
        failures that occurred within the conducted tests.
    """
    failed = []

    for test in tests:
        expected_str = test[0]
        function = test[1]
        if not hasattr(function, '__call__'):
            raise ValueError("The second object in the provided test tuples should be callable!")
        obj = function.__self__
        args = test[2:]
        s = ""
        try:
            s += str(function.__self__) + "."
        except:
            pass
        try:
            s += function.__name__ + "("
        except:
            s += str(function).split(' ')[1][1:-2] + "("
        for arg in args:
            s += str(arg) + ", "
        s = s[:-2] + ")"
        try:
            if verbose:
                print(" ... " + s)
                print(" - Expected str(object) = " + expected_str)
            function(*args)
            assert str(obj) == expected_str, ("Resulted in " + str(obj) +
                                               " instead of the expected " + expected_str + "!")
            if verbose:
                print(" - Resulting str(object) = " + str(obj))
                print("  ... SUCCESS.")
        except AssertionError as e:
            if verbose:
                print("  ... FAILED: not the expected output value!")
            failed.append((s, "Not the expected value!", e))
        except Exception as e:
            if verbose:
                print("  ... FAILED: raised an unexpected exception!")
            failed.append((s, "Raised an unexpected exception!", e))

    if verbose:
        print("... done: %i/%i tests were successful!" % (len(tests)-len(failed), len(tests)))
    
    return failed

################################################################################

def browse_failures(failures):
    """
    Enables the browsing (in console) of the tests that failed.

    Args:
        failures (dict{function:list[tuple("call","failure_description",exception)], ...}):
            A dictionary of failures with function names as keys and as values a list of tests
            that failed under the form of a tuple (function_called, str_failure_description,
            exception) as returned by ``exception_test(tests)`` or ``expected_output_test(tests)``.
    """
    #Check there is something to browse:
    if len(failures) == 0:
        print(
            "*-" * 40 + "\n" +
            "*" + "{:^78}".format("EVERYTHING WENT FINE! LET'S CELEBRATE!") + "*\n" +
            "*-" * 40
        )
        print("Press enter to quit.")
        input()
        return

    print(
        "!-" * 40 + "\n" +
        "!" + "{:^78}".format("SOME TESTS FAILED! NOT COOL MAN!") + "!\n" +
        "!-" * 40
    )

    #Browsing main loop:
    mainLoop = True

    while mainLoop:
        print("Here is the list of functions that failed. Select one to get more details.")
        orderedList = sorted(failures.keys())
        i = 0
        for failure in orderedList:
            i += 1
            print(" " + "{:^2}".format(i) + " - " + failure)

        print(" " + "{:^2}".format(i+1) + " - Quit")

        correct = False
        answer = 0
        while not correct:
            try:
                answer = int(eval(input()))
                if 0 < answer <= len(orderedList) + 1:
                    correct = True
                else:
                    print("You must type a valid number, try again!")
            except KeyboardInterrupt:
                mainLoop = False
                correct = True
                continue
            except:
                print("What? Try again!")

        if answer == i+1:
            mainLoop = False
            continue

        print("- " * 40)
        print("List of calls that failed for " + orderedList[answer-1] + ":")
        for fail in failures[orderedList[answer-1]]:
            print(
                " - " + fail[0] + "\n" +
                "   -> Failure description: " + fail[1] + "\n" +
                "   -> Exception: " + str(fail[2]) + "\n"
            )

        print("Press enter to go back.")
        input()
        print("- " * 40)
        
    print("See you again!")
    print("-" * 80)
        
    
