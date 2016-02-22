################################################################################
# thegame.benchmark_utility.py                                                 #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@cit.ie                                          #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module provides some functions to better handle benchmarks for this     #
# library. Nothing fancy, just some nice methods.                              #
################################################################################

import time
import copy

from multiprocessing import Process, Queue

################################################################################
################################################################################
################################################################################

# *********************************
# Methods to call within processes:
# *********************************

def __execute(queue, nb_iterations, function, *args):
    """
    Executes the provided function nb_iterations times and
    pushes the time it took into the queue.

    Args:
        queue (Queue): The queue to push the result in.
        nb_iterations (int): The number of times the function should be called.
        function (func.): The function to call.
        args (whatever): The arguments for the function to call.
    """
    try:
        start = time.clock()
        for i in range(nb_iterations):
            function(*args)
        queue.put(time.clock() - start)
    except Exception as e:
        queue.put(e)

################################################################################

def __execute_multiple(queue, functions, *args):
    """
    Executes the provided functions exactly once each. They'll all be called
    with the same provided arguments. This is to be used with bounded methods
    on multiple copies of the provided object. Pushes the time it took into the
    queue.

    Args:
        queue (Queue): The queue to push the result in.
        functions (list[func]): The functions to call.
        args: The arguments for the functons to call.
    """
    try:
        start = time.clock()
        for function in functions:
            function(*args)
        queue.put(time.clock() - start)
    except Exception as e:
        queue.put(e)

################################################################################

def __access_property(queue, nb_iterations, obj, property_name):
    """
    Accesses the provided property nb_iterations times and
    pushes the time it took into the queue.

    Args:
        queue (Queue): The queue to push the result in.
        nb_iterations (int): The number of times the property should be accessed.
        obj (object): The object on which the property should be accessed.
        property_name (str): The name of the property to access.
    """
    try:
        start = time.clock()
        for i in range(nb_iterations):
            getattr(obj, property_name)
        queue.put(time.clock() - start)
    except Exception as e:
        queue.put(e)

################################################################################

def __access_property_multiple(queue, objects, property_name):
    """
    Accesses the provided property once on every object provided in objects.

    Args:
        queue (Queue): The queue to push the result in.
        objects (list[object]): The objects on which the property should be accessed.
        property_name (str): The name of the property to access.
    """
    try:
        start = time.clock()
        for obj in objects:
            getattr(obj, property_name)
        queue.put(time.clock() - start)
    except Exception as e:
        queue.put(e)

################################################################################
################################################################################
################################################################################

# ******************************
# Methods to call in benchmarks:
# ******************************

def format_time(function_name, time, nb_iterations, timeout):
    """
    Provides a nicely formatted string given a function name, a time of execution
    and the number of iterations.

    Args:
        function_name (str): The name of the function that was executed.
        time (float): The time it took for the function to execute.
        nb_iterations (int): The nb of times the function was executed.
        timeout (float): The timeout that was used.
    Returns:
        str -- A nicely formatted string to print the time the execution took.
    """
    s = function_name
    if time == -1:
        s = ("{:<50}".format(s if len(s) <= 50 else s[0:36] + "...)") +
             ": " + "{:>15}".format("> {:.3f}".format(timeout * 1000000/nb_iterations)) + "µs")
    elif time == -2:
        s = ("{:<50}".format(s if len(s) <= 50 else s[0:36] + "...)") +
             ": miserably crashed, without any exception, magic!")
    else:
        s = ("{:<50}".format(s if len(s) <= 50 else s[0:36] + "...)") +
             ": " + "{:>15}".format("{:.3f}".format(time*1000000/nb_iterations)) + "µs")
    return s

################################################################################

def time_function(nb_iterations, function, *args, timeout=30, bounded_copy=False, verbose=True, file=None):
    """
    Returns the number of seconds it took to execute the provided function X
    number of times. If put to verbose, prints the time it takes for the
    function to be executed once, in microseconds. There is a default timeout
    of 30s. An open file can be provided to write the results as well.

    Args:
        nb_iterations (int): The number of times the function should be
            executed.
        function (func): The function to execute.
        args (whatever): The arguments to pass the the function to benchmark.
        timeout (int): The maximum time for the execution before it times out.
            If set to 0 or a negative number, there will be no timeout for tests.
        bounded_copy (bool): If set to ``True``, function must be a method bounded
            to an object, then the object to which it is bounded will be copied
            nb_iterations times (yep, this is a lot) and the method will be called
            once on each object.
        verbose (bool): If set to ``True``, prints results in the console.
        file (file): An open file to write results in.
    Returns:
        float -- The number of seconds the execution took, -1 if it timed out.
    """
    #Executing the function in another process to be able to time it out.
    #The queue is used to gather the time of execution.
    queue = Queue()
    if bounded_copy:
        functions = []
        obj = function.__self__  #Get the instance to which the function is bounded
        name = function.__name__ #Get the name of the function
        for i in range(nb_iterations):
            functions.append(getattr(copy.deepcopy(obj), name)) #Get the method and bound it to a deep copy
        p = Process(target=__execute_multiple, args=((queue, functions) + args))
    else:
        p = Process(target=__execute, args=((queue, nb_iterations, function) + args))
    p.start()
    if timeout > 0:
        p.join(timeout)
    else:
        p.join()

    result = -1
    if p.is_alive():
        p.terminate()
        p.join()
    else:
        if not queue.empty():
            result = queue.get(False)
            if isinstance(result, Exception):
                raise result
        else:
            result = -2
    
    if verbose or file != None:
        s = function.__name__ + "("
        for arg in args:
            s += str(arg) + ", "
        s = s[:-2] + ")" if len(args) > 0 else s + ")"
        s = format_time(s, result, nb_iterations, timeout)
        if verbose:
            print(s)
        if file != None:
            file.write(s + "\n")

    return result

################################################################################

def time_function_cannot_be_pickled(nb_iterations, function, *args, bounded_copy=False, verbose=True, file=None):
    """
    Returns the number of seconds it took to execute the provided function X
    number of times. This is specific for methods that cannot be pickled (because
    of decorators for instance...). Thus, no timeout can be applied. Just pray it
    won't take too long. An open file can be provided to write the results as well.

    Args:
        nb_iterations (int): The number of times the function should be
            executed.
        function (func): The function to execute.
        args (whatever): The arguments to pass the the function to benchmark.
        bounded_copy (bool): If set to ``True``, function must be a method bounded
            to an object, then the object to which it is bounded will be copied
            nb_iterations times (yep, this is a lot) and the method will be called
            once on each object.
        verbose (bool): If set to ``True``, prints results in the console.
        file (file): An open file to write results in.
    Returns:
        float -- The number of seconds the execution took, -1 if it timed out.
    """
    #Executing the function in another process to be able to time it out.
    #The queue is used to gather the time of execution.
    queue = Queue()
    if bounded_copy:
        functions = []
        obj = function.__self__  #Get the instance to which the function is bounded
        name = function.__name__ #Get the name of the function
        for i in range(nb_iterations):
            functions.append(getattr(copy.deepcopy(obj), name)) #Get the method and bound it to a deep copy
        start = time.time()
        for function in functions:
            function(*args)
        result = time.time() - start
    else:
        start = time.time()
        for i in range(nb_iterations):
            function(*args)
        result = time.time() - start
    
    if verbose or file != None:
        s = function.__name__ + "("
        for arg in args:
            s += str(arg) + ", "
        s = s[:-2] + ")" if len(args) > 0 else s + ")"
        s = format_time(s, result, nb_iterations, timeout)
        if verbose:
            print(s)
        if file != None:
            file.write(s + "\n")

    return result

################################################################################

def time_property(nb_iterations, obj, property_name, timeout=30, bounded_copy=False):
    """
    Returns the number of seconds it took to access the given property X
    number of times. If put to verbose, prints the time it takes for the
    function to be executed once, in microseconds. There is a default timeout
    of 30s. An open file can be provided to write the results as well.

    Args:
        nb_iterations (int): The number of times the function should be
            executed.
        obj (object): The object on which the property should be accessed.
        property_name (str): The name of the property to access.
        timeout (int): The maximum time for the execution before it times out.
            If set to 0 or a negative number, there will be no timeout for tests.
        bounded_copy (bool): If set to ``True`` then the object will be copied
            nb_iterations times (yep, this is a lot) and the property will be accessed
            once on each object.
    Returns:
        float -- The number of seconds the execution took, -1 if it timed out.
    """
    #Executing the function in another process to be able to time it out.
    #The queue is used to gather the time of execution.
    queue = Queue()
    if bounded_copy:
        objects = []
        for i in range(nb_iterations):
            objects.append(copy.deepcopy(obj))
        p = Process(target=__access_property_multiple, args=(queue, objects, property_name))
    else:
        p = Process(target=__access_property, args=(queue, nb_iterations, obj, property_name))
    p.start()
    if timeout > 0:
        p.join(timeout)
    else:
        p.join()

    result = -1
    if p.is_alive():
        p.terminate()
        p.join()
    else:
        if not queue.empty():
            result = queue.get(False)
            if isinstance(result, Exception):
                raise result
        else:
            result = -2

    return result
