#!/usr/bin/python

################################################################################
# thegame.benchmark_massfunction.py                                            #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@insight-centre.org                              #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module runs benchmarks for the massfunction classes. This is a good way #
# to understand what might take most of the computation time in your code.     #
################################################################################

if __name__ == '__main__':
    #Gory imports, honestly, who cares?
    import sys
    import os
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
    
    from thegame.element import *
    from thegame.massfunction import *
    from benchmark_utility import *

    import random
    
    print(
        "*" * 80 + "\n" +
        "*" + "{:^78}".format(os.path.basename(__file__)) + "*\n" +
        "*" * 80
    )

    nb_iterations = 10000
    timeout = 60

    f = open("Results - massfunction.txt", "w")
    f.write(
        "*" * 80 + "\n" +
        "*" + "{:^78}".format("MassFunction benchmark") + "*\n" +
        "*" * 80 + "\n\n"
    )

    
    s = "CONSTRUCTORS:"
    print(s)
    f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Empty mass function:"
    print(s)
    f.write(s + "\n")
    time_function(nb_iterations, MassFunction, timeout=timeout, file=f)
    time_function(nb_iterations, MassFunction.factory_constructor_unsafe, timeout=timeout, file=f)

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    print("Working on the element construction...")
    
    #Get some elements:
    print(" ... building small size elements.")
    smallElements = []
    for e in DiscreteElement.iterator_powerset(3):
        smallElements.append(e)

    print(" ... building medium size elements.")
    mediumElements = []
    for e in DiscreteElement.iterator_powerset(10):
        mediumElements.append(e)

    print(" ... building big size elements.")
    bigElements = []
    biggest = int("1"*10000, 2) #Faster than 2**10000
    
    #numbers = random.sample(range(biggest), 10000)  # Overflow, too large for C types!
    #for i in numbers:
    #    bigElements.append(DiscreteElement(10000, i))
    
    selectedInts = []
    for i in range(10000):
        randomInt = random.randint(0, biggest)
        while randomInt in selectedInts:
            randomInt = random.randint(0, biggest)
        randomElement = DiscreteElement(10000, randomInt)
        bigElements.append(randomElement)

    #Sets of small size elements:
    print(" ... buildings the sets.")
    numberOfElements = [1, 3, 7, 15, 30, 50, 100, 200, 500, 1000]
    smallSets  = []
    mediumSets = []
    bigSets    = []
    for number in numberOfElements:
        print("  ... of " + str(number) + " focals.")
        if number <= len(smallElements):
            smallSets.append([(x, 1.0/number) for x in random.sample(smallElements, number)])
        if number <= len(mediumElements):
            mediumSets.append([(x, 1.0/number) for x in random.sample(mediumElements, number)])
        if number <= len(bigElements):
            bigSets.append([(x, 1.0/number) for x in random.sample(bigElements, number)])

    print("... done!")
    print("- " * 40)

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    
    nb_iterations = 100

    s = "Classic mass functions construction:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])), time_function(nb_iterations, MassFunction, *smallSet, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])), time_function(nb_iterations, MassFunction, *mediumSet, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])), time_function(nb_iterations, MassFunction, *bigSet, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    nb_iterations = 1000
    
    s = "Classic mass functions construction (unsafe):"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])), time_function(nb_iterations, MassFunction.factory_constructor_unsafe, *smallSet, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])), time_function(nb_iterations, MassFunction.factory_constructor_unsafe, *mediumSet, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])), time_function(nb_iterations, MassFunction.factory_constructor_unsafe, *bigSet, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    s = "-" * 80
    print(s)
    f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    nb_iterations = 1000

    s = "DECISION MAKING:"
    print(s)
    f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Access mass:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(smallSet, 1)[0][0]
        element_not_in = random.sample(smallElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in smallSet] and i < 100:
            element_not_int = random.sample(smallElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", in", time_function(nb_iterations, m.mass, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", not in", time_function(nb_iterations, m.mass, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(mediumSet, 1)[0][0]
        element_not_in = random.sample(mediumElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in mediumSet] and i < 100:
            element_not_int = random.sample(mediumElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", in", time_function(nb_iterations, m.mass, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", not in", time_function(nb_iterations, m.mass, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(bigSet, 1)[0][0]
        element_not_in = random.sample(bigElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in bigSet] and i < 100:
            element_not_int = random.sample(bigElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", in", time_function(nb_iterations, m.mass, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", not in", time_function(nb_iterations, m.mass, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Access belief:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(smallSet, 1)[0][0]
        element_not_in = random.sample(smallElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in smallSet] and i < 100:
            element_not_int = random.sample(smallElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", in", time_function(nb_iterations, m.belief, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", not in", time_function(nb_iterations, m.belief, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(mediumSet, 1)[0][0]
        element_not_in = random.sample(mediumElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in mediumSet] and i < 100:
            element_not_int = random.sample(mediumElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", in", time_function(nb_iterations, m.belief, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", not in", time_function(nb_iterations, m.belief, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(bigSet, 1)[0][0]
        element_not_in = random.sample(bigElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in bigSet] and i < 100:
            element_not_int = random.sample(bigElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", in", time_function(nb_iterations, m.belief, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", not in", time_function(nb_iterations, m.belief, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Access betP:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(smallSet, 1)[0][0]
        element_not_in = random.sample(smallElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in smallSet] and i < 100:
            element_not_int = random.sample(smallElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", in", time_function(nb_iterations, m.betP, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", not in", time_function(nb_iterations, m.betP, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(mediumSet, 1)[0][0]
        element_not_in = random.sample(mediumElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in mediumSet] and i < 100:
            element_not_int = random.sample(mediumElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", in", time_function(nb_iterations, m.betP, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", not in", time_function(nb_iterations, m.betP, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(bigSet, 1)[0][0]
        element_not_in = random.sample(bigElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in bigSet] and i < 100:
            element_not_int = random.sample(bigElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", in", time_function(nb_iterations, m.betP, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", not in", time_function(nb_iterations, m.betP, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Access plausibility:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(smallSet, 1)[0][0]
        element_not_in = random.sample(smallElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in smallSet] and i < 100:
            element_not_int = random.sample(smallElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", in", time_function(nb_iterations, m.plausibility, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", not in", time_function(nb_iterations, m.plausibility, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(mediumSet, 1)[0][0]
        element_not_in = random.sample(mediumElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in mediumSet] and i < 100:
            element_not_int = random.sample(mediumElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", in", time_function(nb_iterations, m.plausibility, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", not in", time_function(nb_iterations, m.plausibility, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(bigSet, 1)[0][0]
        element_not_in = random.sample(bigElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in bigSet] and i < 100:
            element_not_int = random.sample(bigElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", in", time_function(nb_iterations, m.plausibility, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", not in", time_function(nb_iterations, m.plausibility, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Access commonality:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(smallSet, 1)[0][0]
        element_not_in = random.sample(smallElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in smallSet] and i < 100:
            element_not_int = random.sample(smallElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", in", time_function(nb_iterations, m.commonality, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", not in", time_function(nb_iterations, m.commonality, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(mediumSet, 1)[0][0]
        element_not_in = random.sample(mediumElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in mediumSet] and i < 100:
            element_not_int = random.sample(mediumElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", in", time_function(nb_iterations, m.commonality, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", not in", time_function(nb_iterations, m.commonality, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Get one element in the set, one outside the set:
        element_in = random.sample(bigSet, 1)[0][0]
        element_not_in = random.sample(bigElements, 1)[0]
        i = 0
        while element_not_in in [x[0] for x in bigSet] and i < 100:
            element_not_int = random.sample(bigElements, 1)[0]
            i += 1

        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", in", time_function(nb_iterations, m.commonality, element_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", not in", time_function(nb_iterations, m.commonality, element_not_in, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    nb_iterations = 1000

    s = "Get the minima:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        #Build a mass function:
        m = MassFunction(*smallSet)
        realSet = [x[0] for x in smallSet]

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    nb_iterations = 10

    for mediumSet in mediumSets:
        #Build a mass function:
        m = MassFunction(*mediumSet)
        realSet = [x[0] for x in mediumSet]

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    nb_iterations = 1

    for bigSet in bigSets:
        #Build a mass function:
        m = MassFunction(*bigSet)
        realSet = [x[0] for x in bigSet]

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.mass, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.bel, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.betP, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_min, m.pl, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    nb_iterations = 100

    s = "Get the maxima:"
    print(s)
    f.write(s + "\n")
    for smallSet in smallSets:
        #Build a mass function:
        m = MassFunction(*smallSet)
        realSet = [x[0] for x in smallSet]

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 1, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 1, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 2, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])) + ", set " + str(len(smallSet)) + ", maxcard 2, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    nb_iterations = 10
    
    for mediumSet in mediumSets:
        #Build a mass function:
        m = MassFunction(*mediumSet)
        realSet = [x[0] for x in mediumSet]

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 3, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 3, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 6, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 6, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])) + ", set " + str(len(mediumSet)) + ", maxcard 9, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 9, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    nb_iterations = 1

    for bigSet in bigSets:
        #Build a mass function:
        m = MassFunction(*bigSet)
        realSet = [x[0] for x in bigSet]

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, mass", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.mass, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, bel", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.bel, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, betP", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.betP, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 300, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 300, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 600, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 600, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
        s = format_time("size 10000, focals " + str(round(1/bigSet[0][1])) + ", set " + str(len(bigSet)) + ", maxcard 900, pl", time_function_cannot_be_pickled(nb_iterations, MassFunction.get_max, m.pl, 900, realSet, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    s = "-" * 80
    print(s)
    f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    
    nb_iterations = 1000

    s = "CHARACTERISATION:"
    print(s)
    f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Specificity:"
    print(s)
    f.write(s + "\n")

    for smallSet in smallSets:
        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])), time_function(nb_iterations, m.specificity, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])), time_function(nb_iterations, m.specificity, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10, focals " + str(round(1/bigSet[0][1])), time_function(nb_iterations, m.specificity, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
    
    s = "- " * 40
    print(s)
    f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "Non-specificity:"
    print(s)
    f.write(s + "\n")

    for smallSet in smallSets:
        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])), time_function(nb_iterations, m.non_specificity, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])), time_function(nb_iterations, m.non_specificity, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10, focals " + str(round(1/bigSet[0][1])), time_function(nb_iterations, m.non_specificity, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "Discrepancy:"
    print(s)
    f.write(s + "\n")

    for smallSet in smallSets:
        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])), time_function(nb_iterations, m.discrepancy, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])), time_function(nb_iterations, m.discrepancy, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10, focals " + str(round(1/bigSet[0][1])), time_function(nb_iterations, m.discrepancy, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "-" * 80
    print(s)
    f.write(s + "\n")

    nb_iterations = 1000

    s = "DISCOUNTING:"
    print(s)
    f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Discounting:"
    print(s)
    f.write(s + "\n")

    for smallSet in smallSets:
        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])), time_function(nb_iterations, m.discounting, 0.1, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])), time_function(nb_iterations, m.discounting, 0.1, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10, focals " + str(round(1/bigSet[0][1])), time_function(nb_iterations, m.discounting, 0.1, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Weakening:"
    print(s)
    f.write(s + "\n")

    for smallSet in smallSets:
        #Build a mass function:
        m = MassFunction(*smallSet)

        s = format_time("size 3, focals " + str(round(1/smallSet[0][1])), time_function(nb_iterations, m.weakening, 0.1, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for mediumSet in mediumSets:
        #Build a mass function:
        m = MassFunction(*mediumSet)

        s = format_time("size 10, focals " + str(round(1/mediumSet[0][1])), time_function(nb_iterations, m.weakening, 0.1, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")

    for bigSet in bigSets:
        #Build a mass function:
        m = MassFunction(*bigSet)

        s = format_time("size 10, focals " + str(round(1/bigSet[0][1])), time_function(nb_iterations, m.weakening, 0.1, timeout=timeout, verbose=False), nb_iterations, timeout)
        print(s)
        f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "-" * 80
    print(s)
    f.write(s + "\n")

    nb_iterations = 100

    s = "DISTANCES:"
    print(s)
    f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Distance:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.distance, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.distance, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.distance, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.distance, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.distance, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.distance, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.distance, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.distance, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.distance, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.distance, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.distance, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.distance, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Distance (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.distance_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "-" * 80
    print(s)
    f.write(s + "\n")

    nb_iterations = 100

    s = "COMBINATIONS:"
    print(s)
    f.write(s + "\n")

    s = "- " * 40
    print(s)
    f.write(s + "\n")

    s = "Smets:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_smets, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_smets, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_smets, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_smets, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    s = "- " * 40
    print(s)
    f.write(s + "\n")
       
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "Smets (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_smets_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    """
    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Dempster:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dempster, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dempster, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dempster, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dempster, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    """
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Dempster (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dempster_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Disjunctive:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_disjunctive, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
           
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Disjunctive (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_disjunctive_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Yager:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_yager, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_yager, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_yager, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_yager, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Yager (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_yager_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Average:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_average, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_average, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_average, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_average, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Average (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_average_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Dubois Prade:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dubois_prade, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Dubois Prade (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_dubois_prade_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Murphy:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_murphy, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_murphy, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_murphy, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_murphy, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Murphy (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_murphy_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
    
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Chen:"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_chen, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_chen, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_chen, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_chen, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
                                  
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################

    s = "- " * 40
    print(s)
    f.write(s + "\n")
    
    s = "Chen (unsafe):"
    print(s)
    f.write(s + "\n")
    for number in numberOfElements:
        if number <= len(smallElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(smallElements, number)])

            s = format_time("size 3, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 3, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(mediumElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(mediumElements, number)])

            s = format_time("size 10, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")

    for number in numberOfElements:
        if number <= len(bigElements):
            m1 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m2 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m3 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m4 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])
            m5 = MassFunction(*[(x, 1.0/number) for x in random.sample(bigElements, number)])

            s = format_time("size 10000, focals " + str(number) + ", 2 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 3 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 4 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, m4, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
            s = format_time("size 10000, focals " + str(number) + ", 5 bbas", time_function(nb_iterations, m1.combination_chen_unsafe, m2, m3, m4, m5, timeout=timeout, verbose=False), nb_iterations, timeout)
            print(s)
            f.write(s + "\n")
                                  
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    ########################################################################################################################################################################################################
    
    f.close()



