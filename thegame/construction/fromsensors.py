################################################################################
# thegame.construction.fromsensors.py                                          #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@insight-centre.org                              #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module contains the classes to build mass functions from sensor measu-  #
# rements. For more details on how it works, please refer to "B. Pietropaoli,  #
# Stable context recognition in smart home, 2013" (French) or "B. Pietropaoli  #
# et al., Belief Inference with Timed Evidence, 2012".                         #
# ---------------------------------------------------------------------------- #
# Main classes:                                                                #
#   - DiscreteMassFunctionsFromSensorsGenerator: A generator of discrete mass  #
#     functions from sensor measurements.                                      #
################################################################################

import thegame.element as element
import thegame.massfunction as massfunction
import thegame.utility.prettyxml as prettyxml

from enum import Enum

import xml.etree.ElementTree as ET
import time
import copy
import os
import shutil

################################################################################
################################################################################
################################################################################

# ***********
# Exceptions:
# ***********

class SensorModelError(Exception):
    """
    Raised when an error occurs in this module.
    """
    pass


class EmptyFocalModelError(SensorModelError):
    """
    Raised when an attempt to extract evidence from an empty focal model is made.
    """

    def __init__(self, element):
        self.element = element

    def __str__(self):
        return ("Element: " + str(self.element) + "\n" +
                "The model is empty, you cannot get anything out of it!")

    
class EmptyFocalError(SensorModelError):
    """
    Raised when an attempt to extract evidence from an empty model is made.
    """

    def __init__(self, sensor_type):
        self.sensor_type = sensor_type

    def __str__(self):
        return ("Sensor type: " + str(self.sensor_type) + "\n" +
                "The model is empty, you cannot get anything out of it!")

    
class DuplicateValueError(SensorModelError):
    """
    Raised when a duplicate value is found in a sensor model.
    """

    def __init__(self, element, value):
        self.element = element
        self.value = value

    def __str__(self):
        return ("Element: " + str(self.element) + ", sensor value duplicate: " +
                str(self.value) + "\n" +
                "A sensor model cannot contain multiple mass values " +
                "for the same sensor measure!")


class DuplicateFocalElementError(SensorModelError):
    """
    Raised when a duplicate focal element is found in a sensor model.
    """

    def __init__(self, sensor_type, element):
        self.sensor_type = sensor_type
        self.element = element

    def __str__(self):
        return ("Sensor type: " + str(self.sensor_type) + ", element: " + str(self.element) + "\n" +
                "A sensor model cannot contain multiple times the same focal element!")


class DuplicateOptionError(SensorModelError):
    """
    Raised when a duplicate option is found in a sensor model.
    """

    def __init__(self, sensor_type, option):
        self.sensor_type = sensor_type
        self.option = option

    def __str__(self):
        return ("Sensor type: " + str(self.sensor_type) + ", option: " + str(self.option) + "\n" +
                "A sensor model cannot contain twice the same option!")


class IncompatibleOptionsError(SensorModelError):
    """
    Raised when a sensor model contains two or more incompatible options.
    """

    def __init__(self, sensor_type, o1, o2):
        self.sensor_type = sensor_type
        self.option1 = o1
        self.option2 = o2

    def __str__(self):
        return ("Sensor type: " + str(self.sensor_type) + ", option 1: " + str(self.option1) +
                ", option 2: " + str(self.option2) + "\n" +
                "Those options are incompatible!")


class UnknownOptionType(SensorModelError):
    """
    Raised when an unknown option is created within a sensor model.
    """

    def __init__(self):
        pass

    def __str__(self):
        return ("The requested option cannot be recognised. Check the " +
                "DiscreteSensorModelOption.Option enumeration for a list " +
                "of the existing options.")


class MissingInformationError(SensorModelError):
    """
    Raised when an invalid model is found: lacking a file, lackling certain data, etc.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return message


class InvalidBeliefsFromSensorsModelError(SensorModelError):
    """
    Raised when parsing couldn't be performed because of a mistake in the model files.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return message

################################################################################
################################################################################
################################################################################

class DiscreteSensorModelOption:
    """
    A small class to store option data for sensor models.

    Attributes:
        self.option_type (DiscreteSensorModelOption.Option): The type of option.
        self.parameter (float): The parameter to apply the option.
        self.data (list[whatever]): Data storage to apply the option.
    """

    class Option(Enum):
        """
        The enumeration of the currently implemented options
        for the sensor models.
        """
        """Consider the variation of the sensor measurements instead of
        the measurements themselves."""
        variation = 1,
        """Applies the temporisation based on specificity when inferring
        belief from sensor measures. The parameter is the time in seconds
        before a belief is totally forgotten.
        For more details, refer to "B. Pietropaoli, Stable context recognition
        in smart home, 2013" (French)."""
        temporisation_specificity = 2,
        """Applies the temporisation based on the Dubois and Prade's combination
        rule when inferring belief from sensor measures. The parameter is the time
        in seconds before a belief is totally forgotten.
        For more details, refer to "B. Pietropaoli, Stable context recognition
        in smart home, 2013" (French)."""
        temporisation_fusion = 3

    """The list of incompatible options."""
    incompatible = [
        (2, 3),
        (3, 2)
    ]

    def __init__(self, option_type, parameter):
        """
        Constructs an option.

        Args:
            option_type (DiscreteSensorModelOption.Option): The option to construct.
            parameter (float): A parameter to apply the option (a time or a number of
                measurements to consider).
        Raises:
            UnknownOptionError: If an unknown option type is given.
        """
        if option_type not in DiscreteSensorModelOption.Option:
            raise UnknownOptionError()
        
        self.option_type = option_type
        self.parameter = parameter
        self.data = []

        if (option_type == DiscreteSensorModelOption.Option.temporisation_specificity or
            option_type == DiscreteSensorModelOption.Option.temporisation_fusion):
            self.data.append(-1)
            self.data.append(massfunction.MassFunction())

    def add_measure(self, measure):
        """
        Adds a sensor measurement to the data storage. SHOULD BE APPLIED ONLY TO VARIATION OPTIONS.

        Args:
            measure (float): The sensor measurement to add to the storage.
        """
        self.data.insert(0, measure)
        if len(self.data) > self.parameter:
            del self.data[-1]

    def get_previous_time(self):
        """
        """
        return self.data[0]

    def set_previous_time(self, time):
        """
        """
        self.data[0] = time

    def get_previous_mass(self):
        """
        """
        return self.data[1]

    def set_previous_mass(self, mass):
        """
        """
        self.data[1] = mass

    def __str__(self):
        """
        Overrides ``str()``.
        """
        if self.option_type == DiscreteSensorModelOption.Option.temporisation_specificity:
            return "Temporisation Specificity: " + str(self.parameter) + "s"
        elif self.option_type == DiscreteSensorModelOption.Option.temporisation_fusion:
            return "Temporisation Fusion: " + str(self.parameter) + "s"
        elif self.option_type == DiscreteSensorModelOption.Option.variation:
            return "Variation: " + str(self.parameter) + " measures"

################################################################################
################################################################################
################################################################################

class DiscreteSensorFocalBelief:
    """
    A class to store the sensor model for a single focal elements
    under the form of a list of tuples (sensor_measure, mass).

    The model works as a set of key sensor measurements to which masses
    are associated. The retrieve mass for a given sensor measurement,
    if it corresponds to a key measure, then the returned mass will be equal
    to the one stored in the model. If it is inbetween two key measures, then
    the mass is obtained by performing a linear approximation between the two
    key values' masses. If the measure is smaller than the smallest measure in
    the model, then it returns the mass of the smallest key value. It does the
    same symmetrically for the biggest value.

    Look at ``get_mass(self, sensor_measure)``for an algorithmic idea of how the
    mass is obtained from the model.

    Attributes:
        self.element (Element): The focal element for which the model
            is stored.
        self.points (list[tuple(float, float)]): The key sensor measurements
            of the model.
    """

    def __init__(self, element, *points):
        """
        Builds the model for the given focal element, given a set of points
        under the form (sensor_measure, mass). 

        Args:
            element (Element): The focal element for which the model is stored.
            points (*tuple(sensor_measure, mass)): The key measurements for the
                model.
        Raises:
            DuplicateValueError: If the same key measurement is provided multiple
            times.
        """
        self.element = element
        self.points = []
        self.add_points(*points)

    def add_point(self, sensor_measure, mass):
        """
        Adds the given key measurement to the model.

        Args:
            sensor_measure (float): The key sensor measurement.
            mass (float): The mass that should be associated to the key measurement.
        Raises:
            DuplicateValueError: If the given key sensor_measure is already in the
            model.
        """
        if sensor_measure in [x[0] for x in self.points]:
            raise DuplicateValueError(self.element, sensor_measure)

        self.points.append((sensor_measure, mass))
        self.points = sorted(self.points, key=lambda x: x[0])

    def add_points(self, *points):
        """
        Adds the given key measurements to the model.

        Args:
            points (tuple(float, float)): The points to add to the model under
                the form of an iterable of tuples in the form (sensor_measure, mass).
        Raises:
            DuplicateValueError: If a key sensor measurement is given multiple times
            or was already present in the model.
        """
        for point in points:
            self.add_point(point[0], point[1])

    def get_mass(self, sensor_measure):
        """
        Gets the mass for the given sensor measurement in the current model.

        Args:
            sensor_measure (float): The sensor measurement.
        Returns:
            float -- The mass for the given sensor measure in the current model.
        Raises:
            EmptyModelError: If the current model does not contain any key measurement.
        """
        if len(self.points) == 0:
            raise EmptyFocalModelError(self.element)

        if sensor_measure <= self.points[0]:
            return self.points[0][1]
        elif sensor_measure >= self.points[-1]:
            return self.points[-1][1]
        else:
            for i in range(len(self.points)-1):
                if self.points[i] <= sensor_measure <= self.points[i+1]:
                    return (self.points[i][1] +
                            (self.points[i+1][1] - self.points[i][1]) *
                            (sensor_measure - self.points[i][0]) /
                            (self.points[i+1][0] - self.points[i][0]))
                

################################################################################
################################################################################
################################################################################

class DiscreteSensorModel:
    """
    A class to store a complete sensor model.

    Attributes:
        self.sensor_type (str): the name of the sensor type to which the model
            is associated.
        self.options (list[DiscreteSensorModelOption]): The options applied to the
            moidel.
        self.focals (list[DiscreteSensorFocalBelief]): The masses associated to the
            focal elements and the sensor measurements key values.
    """

    def __init__(self, sensor_type, *focals):
        """
        Builds the sensor model.

        Args:
            sensor_type (str): The type of sensor to which this model is associated.
            focals (*DiscreteSensorFocalBelief): The models for focal elements containing
                sensor measurement key values.
        """
        self.sensor_type = sensor_type
        self.options = []
        self.focals = []
        for focal in focals:
            self.add_focal(focal)

    def add_focal(self, focal):
        """
        Adds a focal element model to the sensor model.

        Args:
            focal (DiscreteSensorFocalBelief): The focal model to add.
        Raises:
            DuplicateFocalElementError: If the focal element to which the focal model
            is associated is already present in the sensor model.
        """
        for f in self.focals:
            if focal.element == f.element:
                raise DuplicateFocalElementError(self.sensor_type, focal.element)

        self.focals.append(focal)

    def add_focals(self, *focals):
        """
        Adds focal element models to the sensor model.

        Args:
            focals (*DiscreteSensorFocalBelief): The focal models to add.
        Raises:
            DuplicateFocalElementError: If one of the focal elements to which the focal models
            are associated is already present in the sensor model.
        """
        for focal in focals:
            self.add_focal(focal)

    def add_option(self, option):
        """
        Adds an option to the sensor model.

        Args:
            option (DiscreteSensorModelOption): The option to add to the model.
        Raises:
            IncompatibleOptionsError: If the added option is incompatible with one
                of the already applied options.
            DuplicateOptionError: If an option of the same type was already applied
                to the sensor model.
        """
        for o in self.options:
            if (o, option) in DiscreteSensorModelOption.incompatible:
                raise IncompatibleOptionsError(self.sensor_type, o, option)

        for o in self.options:
            if o == option:
                raise DuplicateOptionError(self.sensor_type, option)

        self.options.append(option)

    def add_options(self, *options):
        """
        Adds options to the sensor model.

        Args:
            options (*DiscreteSensorModelOption): The options to add to the model.
        Raises:
            IncompatibleOptionsError: If one of the added options is incompatible with one
                of the already applied options.
            DuplicateOptionError: If an option of the same type was already applied
                to the sensor model.
        """
        for option in options:
            self.add_option(option)

    def get_evidence(self, sensor_measurement):
        """
        Gets a mass function given a sensor measurement and the current sensor model.
        Returns a vacuous mass function if sensor_measurement == None.

        Remark: As the model might be used for multiple identical sensors, the effect
        of options is not applied here.

        Args:
            sensor_measurement (float): The measurement provided by the sensor.
        Returns:
            MassFunction -- A new mass function that corresponds to the projection
            of the sensor measurement on the sensor model.
        """
        if len(self.focals) == 0:
            raise EmptyModelError(self.sensor_type)

        if sensor_measurement == None:
            complete = self.focals[0].element.get_compatible_complete_element()
            return massfunction.MassFunction((complete, 1)) #No measure = vacuous mass function
        else:
            result = massfunction.MassFunction()
            for focal in self.focals:
                result.add_mass((focal.element, focal.get_mass(sensor_measurement)))
            return result

    def is_valid(self):
        """
        Checks that the model is valid.

        Returns:
            bool -- ``True`` if the model is valid, ``False`` otherwise.
        """
        values = []
        for focal in self.focals:
            for point in focal.points:
                if point[0] not in values:
                    values.append(point[0])

        for value in values:
            mass = self.get_evidence(value)
            if not mass.is_valid():
                return False
        return True

        
################################################################################
################################################################################
################################################################################

class DiscreteSensorModelData:
    """
    A class to store a complete sensor model and associate it with a specific sensor.
    It stores option data specifically for the sensor to which it is associated.
    Thus, the same model can be applied to multiple sensors.

    Attributes:
        self.sensor_name (str): The name of the sensor to which the model is associated.
        self.model (DiscreteSensorModel): The sensor model to apply to the sensor.
        self.options (list[DiscreteSensorModelOption]): The options with their data.
    """

    def __init__(self, sensor_name, model):
        """
        Associate a model a given sensor.

        Args:
            sensor_name (str): The name of the sensor.
            model (DiscreteSensorModel): The model to associate to the sensor.
        """
        self.sensor_name = sensor_name
        self.model = model
        self.options = []
        for option in model.options:
            self.options.append(DiscreteSensorModelOption(option.option_type, option.parameter))

    def update_model(self, model):
        """
        Updates the current model with the given one. This thus resets the options as well as they
        might have changed.

        Args:
            model (DiscreteSensorModel): The new sensor model to associate to the current sensor.
        """
        self.model = model
        self.reset_options()

    def reset_options(self):
        """
        Resets the options by reseting their data.
        """
        self.options = []
        for option in self.model.options:
            self.options.append(DiscreteSensorModelOption(option.option_type, option.parameter))

    def get_evidence(self, sensor_measurement):
        """
        Gets the mass function for the current sensor given the model associated to it and the provided
        sensor measurement. It applies the options here (variation, temporisations...).

        Args:
            sensor_measurement (float): The measurement provided by the sensor.
        Returns:
            MassFunction -- A new mass function that is the projection of the sensor measurement
            in the model + the application of various options if required (variation, temporisation).
        """
        newMeasure = sensor_measurement

        #Check if "variation" applies:
        variationOption = None
        for option in self.options:
            if option.option_type == DiscreteSensorModelOption.Option.variation:
                variationOption = option
                break

        #Apply variation:
        if variationOption != None:
            s = 0
            nbMeasures = 0
            for measure in variationOption.data:
                if measure != None:
                    s += sensor_measurement - measure
                    nbMeasures += 1
            if nbMeasures != 0:
                newMeasure = s / nbMeasures
            else:
                newMeasure = None
            variationOption.add_measure(sensor_measurement)

        #Get the evidence:
        evidence = self.model.get_evidence(newMeasure)

        #Check if temporisation fusion applies:
        tempoOption = None
        for option in self.options:
            if option.option_type == DiscreteSensorModelOption.Option.temporisation_fusion:
                tempoOption = option
                break

        #Apply tempo fusion:
        if tempoOption != None:
            new_time = time.time()
            old_time = tempoOption.get_previous_time()
            old_mass_function = tempoOption.get_previous_mass()

            evidence, new_old_time, new_old_mass= old_mass_function.temporisation_fusion(old_time, new_time,
                                                                                         tempoOption.parameter,
                                                                                         evidence, got_data=newMeasure!=None)

            tempoOption.set_previous_time(new_old_time)
            tempoOption.set_previous_mass(new_old_mass)

        #Check if temporisation specificity applies:
        tempoOption = None
        for option in self.options:
            if option.option_type == DiscreteSensorModelOption.Option.temporisation_specificity:
                tempoOption = option
                break

        #Apply tempo specificity:
        if tempoOption != None:
            new_time = time.time()
            old_time = tempoOption.get_previous_time()
            old_mass_function = tempoOption.get_previous_mass()

            evidence, new_old_time, new_old_mass= old_mass_function.temporisation_specificity(old_time, new_time,
                                                                                              tempoOption.parameter,
                                                                                              evidence, got_data=newMeasure!=None)

            tempoOption.set_previous_time(new_old_time)
            tempoOption.set_previous_mass(new_old_mass)

        return evidence
                
    
################################################################################
################################################################################
################################################################################

class DiscreteMassFunctionsFromSensorsGenerator:
    """
    A generator of mass functions from sensor measurements. For details on how it works,
    please refer to "B. Pietropaoli, Stable context recognition in smart home, 2013" (French)
    or "B. Pietropaoli et al., Belief Inference with Timed Evidence, 2012".

    Args:
        self.frame_name (str): The name of the frame of discernment (e.g. presence).
        self.sensor_models (dict{sensor_type:DiscreteSensorModel}): The models currently
            loaded in this generator.
        self.current_sensors (dict{sensor_name:DiscreteSensorModelData}): The sensor
            currently registered in this generator with their models associated.
    """

    class ModelFormat(Enum):
        """
        The different types of formats for the models.
        """
        XML = 1,
        custom_directory = 2
    
    ################################################################################

    def __init__(self, frame_name=""):
        """
        Constructs the generator.

        Args:
            frame_name (str): The name of the frame of discernment.
        """
        self.frame_name = frame_name
        self.sensor_models = {}
        self.current_sensors = {}
        self.ref_list = []

    ################################################################################

    def load_model(self, path, model_format):
        """
        Loads a model from either an XML file or from a custom directory.

        Args:
            path (str): Either the complete path to the XML file, OR the path
                to the directory containing the model (the name of the directory
                is used as the name of the frame of discernment).
            model_format (ModelFormat): The format of the model to load.
        Raises:
            A lot of various errors to help understand what's wrong in your model.
        """
        if model_format not in DiscreteMassFunctionsFromSensorsGenerator.ModelFormat:
            raise ValueError(
                "model_format: " + str(model_format) + "\n" +
                "The model format should be of the type ModelFormat!"
            )

        if not os.path.exists(path):
            raise ValueError(
                "path: " + str(path) + "\n" +
                "The given path is invalid!"
            )

        # ***********
        # XML FORMAT:
        # ***********
        if model_format == DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.XML:
            if not os.path.isfile(path):
                raise ValueError(
                    "path: " + str(path) + "\n" +
                    "A file was expected!"
                )

            #Reset the current model:
            self.sensor_models = {}
            self.ref_list = []
            
            #Parse the xml:
            root = ET.parse(path).getroot()

            #Load the frame of discernment:
            frame_element = root.findall("frame")
            if len(frame_element) != 1:
                raise InvalidModelError(
                    "File: " + str(path) + "\n" +
                    "This should contain exactly one <frame> tag!"
                )
            frame_element = frame_element[0]
            self.frame_name = frame_element.get("name")
            for state in frame_element.iter("state"):
                self.ref_list.append(state.text)

            #Load the sensor beliefs:
            beliefs_element = root.findall("sensor-beliefs")
            if len(beliefs_element) != 1:
                raise InvalidBeliefsFromSensorsModelError(
                    "File: " + str(path) + "\n" +
                    "This should contain exactly one <sensor-beliefs> tag!"
                )
            beliefs_element = beliefs_element[0]
            for sensor_belief in beliefs_element.iter("sensor-belief"):
                sensor_type = sensor_belief.get("name")
                model = DiscreteSensorModel(sensor_type)
                
                focals = {}
                for point in sensor_belief.iter("point"):
                    sensor_measure = float(point.find("value").text)
                    for mass in point.iter("mass"):
                        states = mass.get("set")
                        m = float(mass.text)
                        if states not in focals:
                            focals[states] = []
                        focals[states].append((sensor_measure, m))
                
                for states, points in focals.items():
                    focal_element = element.DiscreteElement.factory_from_ref_list(self.ref_list, *(states.split(" ")))
                    focal_belief = DiscreteSensorFocalBelief(focal_element, *points)
                    model.add_focal(focal_belief)

                options_element = sensor_belief.findall("options")
                if len(options_element) > 1:
                    raise InvalidBeliefsFromSensorsModelError(
                        "File: " + str(path) + "\n" +
                        "This should contain maximum one <options> tag per <sensor-belief> tag!"
                    )
                if len(options_element) != 0:
                    options_element = options_element[0]
                    for option in options_element.iter("option"):
                        option_type = option.get("name")
                        parameter = float(option.text)

                        if option_type.lower() == "tempo-specificity":
                            model.add_option(DiscreteSensorModelOption(DiscreteSensorModelOption.Option.temporisation_specificity, parameter))
                        elif option_type.lower() == "tempo-fusion":
                            model.add_option(DiscreteSensorModelOption(DiscreteSensorModelOption.Option.temporisation_fusion, parameter))
                        elif option_type.lower() == "variation":
                            model.add_option(DiscreteSensorModelOption(DiscreteSensorModelOption.Option.variation, parameter))
                        else:
                            raise UnknownOptionType()

                self.sensor_models[sensor_type] = model

            #Load the already registered sensors:
            sensors_element = root.findall("sensors")
            if len(sensors_element) > 1:
                raise InvalidBeliefsFromSensorsModelError(
                    "File: " + str(path) + "\n" +
                    "This should contain exactly one <sensors> tag!"
                )
            if len(sensors_element) != 0:
                sensors_element = sensors_element[0]
                for sensor in sensors_element.iter("sensor"):
                    sensor_name = sensor.get("name")
                    sensor_model = sensor.get("belief")
                    self.current_sensors[sensor_name] = DiscreteSensorModelData(sensor_name, self.sensor_models[sensor_model])
            
        # *****************
        # CUSTOM DIRECTORY:
        # *****************
        elif model_format == DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.custom_directory:
            #Get the name of the frame of discernment:
            if not os.path.isdir(path):
                raise ValueError(
                    "path: " + str(path) + "\n" +
                    "A directory was expected!"
                )
            self.frame_name = os.path.basename(path)

            #Reset the current model:
            self.sensor_models = {}
            self.ref_list = []

            #Get the reference list for the elements:
            reflistfile = os.path.join(path, "values")
            if not os.path.exists(reflistfile):
                raise MissingInformationError(
                    "Invalid model: " + path + " should contain a file called 'values'!"
                )
            f = open(reflistfile, "r")
            self.ref_list = [line.replace("\n", "") for line in f.readlines()]
            f.close()

            #Load the sensor models:
            sensordirs = [x[0] for x in os.walk(path)] #Get the sensor directories
            sensordirs.remove(path)

            for sensordir in sensordirs:
                sensor_type = os.path.basename(sensordir)
                model = DiscreteSensorModel(sensor_type)

                files = os.listdir(sensordir)
                for f in files:
                    if f[-1] != "~": #Do not consider temp files
                        file = open(os.path.join(sensordir, f))
                        lines = [l.replace("\n", "") for l in file.readlines()]
                        #Options file:
                        if f == "options":
                            try:
                                nbOptions = int(lines[0].split(" ")[0])
                                for i in range(nbOptions):
                                    words = lines[i+1].split(" ")
                                    words[0] = words[0].lower()
                                    if words[0] == "tempo-specificity":
                                        model.add_option(DiscreteSensorModelOption(DiscreteSensorModelOption.Option.temporisation_specificity, float(words[1])))
                                    elif words[0] == "tempo-fusion":
                                        model.add_option(DiscreteSensorModelOption(DiscreteSensorModelOption.Option.temporisation_fusion, float(words[1])))
                                    elif words[0] == "variation":
                                        model.add_option(DiscreteSensorModelOption(DiscreteSensorModelOption.Option.variation, float(words[1])))
                            except:
                                raise InvalidBeliefsFromSensorsModelError("The 'options' file in " + str(sensordir) + "was not formatted as expected!")
                        #Key measures files:
                        else:
                            try:
                                nbAtoms = int(lines[0].split(" ")[0])
                                atoms = []
                                for i in range(1, 1 + nbAtoms):
                                    atoms.append(lines[i])

                                nbPoints = int(lines[1 + nbAtoms].split(" ")[0])
                                points = []
                                for i in range(2 + nbAtoms, 2 + nbAtoms + nbPoints):
                                    values = lines[i].split(" ")
                                    points.append((float(values[0]), float(values[1])))

                                focal_element = element.DiscreteElement.factory_from_ref_list(self.ref_list, *atoms)
                                focal_belief = DiscreteSensorFocalBelief(focal_element, *points)
                                model.add_focal(focal_belief)
                            except:
                                raise InvalidBeliefsFromSensorsModelError("The file '" + f + "' was not formatted as expected!")
                                
                        file.close()

                self.sensor_models[sensor_type] = model

        #Update the models:
        to_suppress = []
        for sensor_name, data in self.current_sensors.items():
            if data.model.sensor_type in self.sensor_models:
                data.update_model(self.sensor_models[data.model.sensor_type])
            else:
                to_suppress.append(sensor_name)
        for sensor_name in to_suppress:
            del self.current_sensors[sensor_name]

    ################################################################################

    def save_model(self, path, model_format):
        """
        Saves the current model at the given path in the requested format.

        Args:
            path (str): The path to which the model will be saved. If it is an XML
                file, the .xml extension won't be added, so put it in the path. If
                it is a custom directory, then a new directory will be created with
                name the frame of discernment's name. If it already exists, it is
                erased first!
            model_format (ModelFormat): The format to which the model should be saved.
        Raises:
            ValueError: If the format provided cannot be recognised.
        """
        if model_format not in DiscreteMassFunctionsFromSensorsGenerator.ModelFormat:
            raise ValueError(
                "model_format: " + str(model_format) + "\n" +
                "The model format should be of the type ModelFormat!"
            )
        
        # ***********
        # XML FORMAT:
        # ***********
        if model_format == DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.XML:
            root = ET.Element("belief-from-sensors")
            frame = ET.SubElement(root, "frame", {"name":self.frame_name})
            
            for ref in self.ref_list:
                state = ET.SubElement(frame, "state", {})
                state.text = str(ref)

            sensor_beliefs = ET.SubElement(root, "sensor-beliefs")
            for sensor_type, model in self.sensor_models.items():
                model_node = ET.SubElement(sensor_beliefs, "sensor-belief", {"name":sensor_type})

                #Options:
                if len(model.options) > 0:
                    options = ET.SubElement(model_node, "options")
                    for o in model.options:
                        if o.option_type == DiscreteSensorModelOption.Option.variation:
                            option = ET.SubElement(options, "option", {"name":"variation"})
                        elif o.option_type == DiscreteSensorModelOption.Option.temporisation_fusion:
                            option = ET.SubElement(options, "option", {"name":"tempo-fusion"})
                        elif o.option_type == DiscreteSensorModelOption.Option.temporisation_specificity:
                            option = ET.SubElement(options, "option", {"name":"tempo-specificity"})
                        option.text = str(o.parameter)
                    
                #Points:
                points = {}
                for focal in model.focals:
                    for point in focal.points:
                        if point[0] not in points:
                            points[point[0]] = []
                        s = focal.element.formatted_str(*self.ref_list)[1:-1].replace(" u ", " ")
                        points[point[0]].append((s, point[1]))

                for value, masses in points.items():
                    point_node = ET.SubElement(model_node, "point")
                    value_node = ET.SubElement(point_node, "value")
                    value_node.text = str(value)
                    for mass in masses:
                        mass_node = ET.SubElement(point_node, "mass", {"set":mass[0]})
                        mass_node.text = str(mass[1])

            sensors_element = ET.SubElement(root, "sensors")
            for sensor_name, model_data in self.current_sensors.items():
                ET.SubElement(sensors_element, "sensor", {"name":sensor_name, "belief":model_data.model.sensor_type})

            f = open(path, "w")
            f.write(prettyxml.pretty_str(root))
            f.close()

        # *****************
        # CUSTOM DIRECTORY:
        # *****************
        elif model_format == DiscreteMassFunctionsFromSensorsGenerator.ModelFormat.custom_directory:
            real_path = os.path.join(path, self.frame_name)
            #Suppress the existing directory:
            if os.path.exists(real_path):
                shutil.rmtree(real_path)
            os.mkdir(real_path)

            #Write the ref_list:
            f = open(os.path.join(real_path, "values"), "w")
            for ref in self.ref_list:
                f.write(ref + "\n")
            f.close()

            for sensor_type, sensor_model in self.sensor_models.items():
                sensor_model_path = os.path.join(real_path, sensor_type)
                os.mkdir(sensor_model_path)

                if len(sensor_model.options) > 0:
                    f = open(os.path.join(sensor_model_path, "options"), "w")
                    f.write(str(len(sensor_model.options)) + " options\n")
                    for option in sensor_model.options:
                        if option.option_type == DiscreteSensorModelOption.Option.variation:
                            f.write("variation " + str(option.parameter) + "\n")
                        elif option.option_type == DiscreteSensorModelOption.Option.temporisation_specificity:
                            f.write("tempo-specificity " + str(option.parameter) + "\n")
                        elif option.option_type == DiscreteSensorModelOption.Option.temporisation_fusion:
                            f.write("tempo-fusion " + str(option.parameter) + "\n")
                    f.close()

                for focal in sensor_model.focals:
                    s = focal.element.formatted_str(*self.ref_list)[1:-1]
                    f = open(os.path.join(sensor_model_path, s.replace(" u ", "")), "w")
                    f.write(str(focal.element.cardinal) + " atoms\n")
                    f.write(s.replace(" u ", "\n") + "\n")
                    f.write(str(len(focal.points)) + " points\n")
                    for point in focal.points:
                        f.write(str(point[0]) + " " + str(point[1]) + "\n")
                    f.close()

    
    ################################################################################

    def add_sensor(self, model_name, sensor_name):
        """
        Registers a sensors and associate it with a model.

        Args:
            model_name (str): The name of the model to which the sensor should be
                associated.
            sensor_name (str): The name of the sensor to register.
        Raises:
            ValueError: If the requested model is not found or if the provided
            sensor is already registered.
        """
        if sensor_name in self.current_sensors:
            raise ValueError(
                "sensor_name: " + str(sensor_name) + "\n" +
                "A sensor is already registered under this name!"
            )

        if model_name not in self.sensor_models:
            raise ValueError(
                "model_name: " + str(sensor_name) + "\n" +
                "There is no model with this name!"
            )

        self.current_sensors[sensor_name] = self.sensor_models[model_name]
    
    ################################################################################

    def remove_sensor(self, sensor_name):
        """
        Unregisters a sensor.

        Args:
            sensor_name (str): The name of the sensors to unregister.
        """
        if sensor_name in self.current_sensors:
            del self.current_sensors[sensor_name]
        
    ################################################################################

    def reset_model(self, sensor_name=None):
        """
        Resets the sensor model data for the provided sensor. If set to None, then
        it does it for all the models.

         Args:
             sensor_name (str): The name of the sensor for which the model data
                 should be reset.
        """
        if sensor_name == None:
            for name, model in self.current_sensors.items():
                model.reset_options()
        elif sensor_name in self.current_sensors:
            self.current_sensors[sensor_name].reset_options()
        
    ################################################################################

    def is_valid(self):
        """
        Checks if all the models are valid.

        Returns:
            bool -- ``True`` if all the models are valid, ``False`` otherwise.
        """
        for name, model, in self.sensor_models.items():
            if not model.is_valid():
                return False
        return True
            
    ################################################################################

    def get_evidence(self, *sensor_measurements):
        """
        Gets the evidence from the given sensor measurements and the current models.

        Args:
            sensor_measurements (*tuple(str, float)): The sensor measurements in the
                form of tuples (sensor_name, measurement).
        Returns:
            dict{sensor_name:MassFunction} -- A dictionary with the name of sensors
            as keys and the resulting mass functions as values. The mass function is
            None if the sensor wasn't registered.
        """
        results = {}
        for measurement in sensor_measurements:
            if measurement[0] in self.current_sensors:
                results[measurement[0]] = self.current_sensors[measurement[0]].get_evidence(measurement[1])
            else:
                results[measurement[0]] = None
        return results


