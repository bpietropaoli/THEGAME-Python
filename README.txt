################################################################################
# THE (GAME).Py                                                                #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@insight-centre.org                              #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This package provides the basics of the belief functions theory with modules #
# to manage set-theoretic operations (in element.py) and mass functions (in    #
# massfunction.py).                                                            #
# ---------------------------------------------------------------------------- #
# This package has been implemented and tested with and for Python 3.4+.       #
# If you need a version for Python 2.7, let me know via email, I'll see what I #
# can do.                                                                      #
################################################################################

This package is the Python implementation of THE GAME.

		http://bpietropaoli.github.io/THEGAME/

This is a library to work on the belief functions theory (also called theory of 
evidence or Dempster-Shafer theory). This Python version should provide the 
same functionalities, especially, it can load and save the exact same models as 
the C library.

Please have a look at the provided tutorial, at the documentation and at the
provided references in it before using the library.


Here are the modules provided by this package:

 - thegame.element: A module to create and manipulate (focal) elements within
       the belief functions theory. It provides an abstract Element class used 
       in the mass functions. A DiscreteElement class implements the classic 
       sets used in the theory.

 - thegame.massfunction: A module to create and manipulate mass functions. It
       uses the abstract Element class. Thus, if you want to implement other
       types of elements, you won't have to develop anything to get mass functions
       to work on them. The main class it provides is obviously MassFunction.

 - thegame.utility.prettyxml: A single function to provide an equivalent of the
       pretty_print() of most XML libraries without having to rely on any one of
       them.

 - thegame.construction.fromsensors: A module to create mass functions from sensor
       measurements. For an explanation of the models, please refer to 
       "B. Pietropaoli, Stable context recognition in smart home, 2013" (French)
       or "B. Pietropaoli et al., Belief Inference with Timed Evidence, 2012".

 - thegame.construction.fromrandomness: A module to create random mass functions.
 
 - thegame.construction.frombeliefs: A module to create mass functions from mass
       functions. It transfers beliefs from one frame of discernment to another.
       For more details on how it works, please refer to "B. Pietropaoli et al.,
       Propagation of Belief Functions through Frames of Discernment, 2013".



Philosophy:
-----------
1) I've been trying to make this library as pythonic as possible BUT, in order to
facilitate debbuging, I do raise exceptions when something stupid is attempted.
I've created custom exceptions to provide easy to understand error messages.

If you don't care about exceptions and weird behaviour when you messed it up,
then you are free to use *_unsafe() methods. Those methods do not perform any
check on the passed arguments, nor do they check the validity of what is created.
They are usually faster than their safe equivalent (especially when working with
very big elements and mass functions).

2) The main class is MassFunction. The others (plausibility, belief and commonality)
are not really implemented because they require values on the entire powerset,
they are at best slow and in most cases unpractical.

3) This package does not rely on anything else than the standard library to prevent
incompatibilities. It would be great to keep it that way.

4) The discrete focal elements are implemented using numbers for fast operations on
elements (especially conjunctions and disjunctions).

5) I've implemented things the way I was thinking, it might not be the best. Thus,
if you have a better way to implement things, feel free to do it. But always measure,
never guess. So use benchmarks to test if it concerns critical parts of the code.


Directories:
------------

 - thegame: This is the library, you should put this directory into your code's
       directory or install it in your python installation.

 - thegame.benchmark: This provides scripts to run benchmarks for the modules in
       thegame. It basically runs every function and get the time it takes for 
       each one of them to be executed.

 - thegame.tests: This provides unit tests for thegame's modules. If you change
        anything in the source code of thegame, please, make sure your modified 
        code still passes the tests.



For developers:
---------------
Each module provides:

 - Custom exceptions: try to use them where it makes sense and create new ones if
       necessary, it helps debugging programs using this library.

 - Custom decorators: they facilitate checking for inconsistent arguments, try to
       use them as well where it makes sense. This also helps debugging programs 
       using this library.

 - Full documentation: it's important; if you add something, make sure to document
       it correctly following the same format if possible (for consistency).

Also, thegame.benchmark and thegame.tests contain custom utility modules that can
be pretty helpful to build quick test scripts. You can use the existing tests as
examples.



Details:
--------
For an explanation on why I use functools for the decorators:
http://gael-varoquaux.info/programming/decoration-in-python-done-right-decorating-and-pickling.html?p=120

Without it, I couldn't run wrapped functions within a process which I use to create
timeouts in the benchmark. Anyway, that'll be useful for anybody who wants to parallelise
a bit his or her code. Careful though with the decorated static methods, they cannot be called
inside processes because the static prevents pickling.
