import thegame.element as element
import thegame.massfunction as massfunction
import thegame.construction.fromrandomness as fromrandomness
import thegame.construction.fromsensors as fromsensors
import thegame.construction.frombeliefs as frombeliefs

import os

generator = fromsensors.DiscreteMassFunctionsFromSensorsGenerator()

generator.load_model(r"thegame.tests\Resources\BeliefsFromSensors\XML\BFS-load.xml", fromsensors.DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.XML)
generator.save_model(r"thegame.tests\Resources\BeliefsFromSensors\XML\BFS-save.xml", fromsensors.DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.XML)
generator.load_model(r"thegame.tests\Resources\BeliefsFromSensors\XML\BFS-save.xml", fromsensors.DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.XML)

generator.load_model(r"thegame.tests\Resources\BeliefsFromSensors\test", fromsensors.DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.custom_directory)
generator.frame_name = "test-save"
generator.save_model(r"thegame.tests\Resources\BeliefsFromSensors", fromsensors.DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.custom_directory)

generator.load_model(r"thegame.tests\Resources\BeliefsFromSensors\optionTest", fromsensors.DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.custom_directory)
generator.frame_name = "optionTest-save"
generator.save_model(r"thegame.tests\Resources\BeliefsFromSensors", fromsensors.DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.custom_directory)


generator = frombeliefs.DiscreteMassFunctionsFromBeliefsGenerator()
generator.load_model(r"thegame.tests\Resources\BeliefsFromBeliefs\XML\BFB-load.xml", frombeliefs.DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.XML)
generator.save_model(r"thegame.tests\Resources\BeliefsFromBeliefs\XML\BFB-save.xml", frombeliefs.DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.XML)

generator.load_model(r"thegame.tests\Resources\BeliefsFromBeliefs\Sleeping", frombeliefs.DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.custom_directory)
generator.save_model(r"thegame.tests\Resources\BeliefsFromBeliefs\SavingTest", frombeliefs.DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.custom_directory)


"""
import time

nb_iterations = 100000

generator = fromrandomness.RandomDiscreteMassFunctionsGenerator(15)

start = time.time()
for i in range(nb_iterations):
    generator.build_evidence(10)
print(time.time() - start)

generator = fromrandomness.RandomDiscreteMassFunctionsGenerator(15, False)

start = time.time()
for i in range(nb_iterations):
    generator.build_evidence(10)
print(time.time() - start)
"""

