################################################################################
# thegame.construction.frombeliefs.py                                          #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@insight-centre.org                              #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module contains the classes to transfer belief from one frame of discer-#
# nment to another (thus the construction of beliefs from beliefs). It is usu- #
# ally called "evidential mapping" in the literature. For more details, please #
# refer to "B. Pietropaoli et al., Propagation of Belief Functions through     #
# Frames of Discernment, 2013".                                                #
# ---------------------------------------------------------------------------- #
# Main classes:                                                                #
#   - DiscreteMassFunctionsFromBeliefsGenerator: A generator of discrete mass  #
#     functions from mass functions defined on another frame of discernment.   #
################################################################################

import thegame.element as element
import thegame.massfunction as massfunction
import thegame.utility.prettyxml as prettyxml

from enum import Enum

import xml.etree.ElementTree as ET
import copy
import os
import shutil

################################################################################
################################################################################
################################################################################

# ***********
# Exceptions:
# ***********

class EvidentialMappingError(Exception):
    """
    Raised when an exception occurs in this module.
    """
    pass

class DuplicateRecipientElementError(EvidentialMappingError):
    """
    Raised when a duplicate of a recipient element is found in a mapping vector.
    """

    def __init__(self, element_from, element_to):
        self.element_from = element_from
        self.element_to   = element_to

    def __str__(self):
        return ("The mapping vector for the element " + str(self.element_from) +
                " already contained a transfer point to the element " + str(self.element_to) + "!")

class DuplicateMappingVectorError(EvidentialMappingError):
    """
    Raised when a duplicate mapping vector is found in an evidential mapping.
    """

    def __init__(self, frame_name, element_from):
        self.frame_name = frame_name
        self.element_from = element_from

    def __str__(self):
        return ("The evidential mapping from the frame " + str(self.frame_name) +
                " already contained a mapping vector for the element " + str(self.element_from) + "!")

class InvalidBeliefsFromBeliefsModelError(EvidentialMappingError):
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

class DiscreteMappingVector:
    """
    A mapping vector inside an evidential mapping (a column of the matrix basically).

    Attributes:
        self.element_from (Element): The element from which mass is transferred.
        self.points (dict{Element:float}): The dictionary of the transfer points
            with recipient elements as keys and mass transfer factors as values.
    """

    def __init__(self, element_from, *transfer_points):
        """
        Builds a mapping vector.

        Args:
            element_from (Element): The element from which mass is transferred.
            transfer_points (*tuple(Element, float)): The transfer points for the
                vector in the form of tuples (recipient_element, transfer_factor).
        Raises:
            DiplicateRecipientElementError: If a recipient element is provided
            multiple times.
        """
        self.element_from = element_from
        self.points = {}
        self.add_points(*transfer_points)

    def add_point(self, element, transfer_factor):
        """
        Adds a point to the mapping vector (recipient_element, factor).

        Args:
            element (Element): The recipient element to add to the vector.
            transfer_factor (float): The factor used to transfer mass.
        Raises:
            DuplicateRecipientElementError: If the given element was already
            present in the current vector.
        """
        if element in [x for x in self.points]:
            raise DuplicateRecipientElementError(self.element_from, element)

        self.points[element] = transfer_factor

    def add_points(self, *points):
        """
        Add points in the mapping vector (recipient_element, factor).

        Args:
            points (*tuple(Element, float)): The points to add to the vector in
                the form of tuples (recipient_element, transfer_factor).
        Raises:
            DuplicateRecipientElementError: If one of the given recipient elements
            was already present in the vector.
        """
        for point in points:
            self.add_point(point[0], point[1])

    def get_transfered_mass(self, mass):
        """
        Gets the transferred mass given a mass to transfer and the current
        mapping vector.

        Args:
            mass (float): The mass to transfer.
        Returns:
            MassFunction (invalid) -- The transferred mass in the form of a
            mass function (that should not be valid if the given mass wasn't 1).
        """
        result = MassFunction()
        for element, factor in self.points.items():
            result.add_mass((element, mass * factor))
        return result
    
    def is_valid(self):
        """
        Checks that the vector is valid (the sum of the recipient masses
        equals 1).

        Returns:
            bool -- ``True`` if the vector is valid, ``False`` otherwise.
        """
        s = 0
        for element, factor in self.points.items():
            s += factor
        return s == 1


################################################################################
################################################################################
################################################################################

class DiscreteEvidentialMapping:
    """
    An evidential mapping to transfer mass functions from one frame of discernment
    to another. For more details, please refer to "B. Pietropaoli et al., Propagation
    of Belief Functions through Frames of Discernment, 2013".
    """

    def __init__(self, frame_name, ref_list, *mapping_vectors):
        """
        Builds a discrete evidential mapping.

        Args:
            frame_name (str): The name of the frame of discernment from which mass
                will be transferred.
            ref_list (list[object]): A list of objects representing the actual states
                of the frame of discernment.
            mapping_vectors (*DiscreteMappingVector): The mapping vectors.
        """
        self.frame_name = frame_name
        self.ref_list = ref_list
        self.vectors = {}
        self.add_vectors(*mapping_vectors)

    def add_vector(self, vector):
        """
        Adds a vector to the current mapping.

        Args:
            vector (DiscreteMappingVector): The mapping vector to add to the current
                model.
        Raises:
            DuplicateMappingVectorError: If the element from which mass is transferred
            for the given vector was already present in the mapping.
        """
        if vector.element_from in self.vectors:
            raise DuplicateMappingVectorError(self.frame_name, vector.element_from)

        self.vectors[vector.element_from] = vector

    def add_vectors(self, *vectors):
        """
        Adds mapping vectors to the current mapping.

        Args:
            vectors (*DiscreteMappingVector): The vectors to add to the current model.
        Raises:
            DuplicateMappingVectorError: If one vector was already given in the mapping
            (if the element it comes from was already present in the mapping).
        """
        for vector in vectors:
            self.add_vector(vector)


    def get_evidence(self, mass_function):
        """
        Gets the belief from the given belief (belief transfer).

        Args:
            mass_function (MassFunction): The mass function to build belief
                from (the mass function to transfer on another frame of dis-
                cernment).
        Returns:
            MassFunction -- A new mass function corresponding to the given one
            transferred to another frame of discernment.
        """
        result = MassFunction()
        for element, mass in mass_function.items():
            if not element.is_empty():
                transfer = self.vectors[element].get_transfered_mass(mass)
                for e, v in transfer.items():
                    result.add_mass(e, v)
            else: #The mass on the empty set is transfered entirely
                empty = element.get_compatible_empty_element()
                result.add(empty, mass)
        return result

    def is_valid(self):
        """
        Checks that the current mapping is valid.

        Returns:
            bool -- ``True`` if the model is valid, ``False`` otherwise.
        """
        if len(self.vectors) != 2**len(self.ref_list) - 1:
            False

        for e, vector in self.vectors.items():
            if not vector.is_valid():
                return False
        return True


################################################################################
################################################################################
################################################################################

class DiscreteMassFunctionsFromBeliefsGenerator:
    """
    A discrete mass function generator based on evidential mapping to transfer
    mass functions from one frame of discernment to another. For more details,
    please refer to "B. Pietropaoli et al., Propagation of Belief Functions
    through Frames of Discernment, 2013".

    Attributes:
        self.frame_name (str): The name of the recipient frame of discernment.
        self.ref_list (list[object]): The list of references associated to the
            different possible states in the frame of discernment.
        self.mappings (dict{subframe_name:evidential_mapping}): The evidential
            mappings from which mass can be transferred.
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
        Builds a generator. You should call ``load_model()`` to enable belief construction.
        """
        self.frame_name = frame_name
        self.ref_list = []
        self.mappings = {}

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
        if model_format not in DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat:
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
        if model_format == DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.XML:
            if not os.path.isfile(path):
                raise ValueError(
                    "path: " + str(path) + "\n" +
                    "A file was expected!"
                )

            #Reset the current model:
            self.ref_list = []
            self.mappings = {}

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

            #Load the mappings:
            mappings_element = root.findall("evidential-mappings")
            if len(mappings_element) != 1:
                raise InvalidModelError(
                    "File: " + str(path) + "\n" +
                    "This should contain exactly one <evidential-mappings> tag!"
                )
            mappings_element = mappings_element[0]
            for mapping in mappings_element.iter("evidential-mapping"):
                #Get the subframe:
                subframe_element = mapping.findall("subframe")
                if len(subframe_element) != 1:
                    raise InvalidModelError(
                        "File: " + str(path) + "\n" +
                        "This should contain exactly one <subframe> tag per <evidential-mapping>!"
                    )
                subframe_element = subframe_element[0]
                subframe_name = subframe_element.get("name")
                subframe_ref_list = []
                for state in subframe_element.iter("state"):
                    subframe_ref_list.append(state.text)
                    
                #Get the vectors:
                vectors = []
                for vector_element in mapping.iter("mapping-vector"):
                    from_element = vector_element.findall("from")
                    if len(from_element) != 1:
                        raise InvalidModelError(
                            "File: " + str(path) + "\n" +
                            "This should contain exactly one <from> tag per <mapping-vector>!"
                        )
                    from_element = from_element[0]
                    element_from = element.DiscreteElement.factory_from_ref_list(subframe_ref_list, *from_element.get("element").split(" "))
                    points = []
                    for to_element in vector_element.iter("to"):
                        e = element.DiscreteElement.factory_from_ref_list(self.ref_list, *to_element.get("element").split(" "))
                        v = float(to_element.text)
                        points.append((e, v))
                    vectors.append(DiscreteMappingVector(element_from, *points))
                    
                self.mappings[subframe_name] = DiscreteEvidentialMapping(subframe_name, subframe_ref_list, *vectors)

        # *****************
        # CUSTOM DIRECTORY:
        # *****************
        elif model_format == DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.custom_directory:
            #Get the name of the frame of discernment:
            if not os.path.isdir(path):
                raise ValueError(
                    "path: " + str(path) + "\n" +
                    "A directory was expected!"
                )
            self.frame_name = os.path.basename(path)

            #Reset the current model:
            self.mappings = {}
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

            #Load the subframe models:
            subframesdirs = [x[0] for x in os.walk(path)] #Get the subframe directories
            subframesdirs.remove(path)

            for subframedir in subframesdirs:
                subframe_name = os.path.basename(subframedir)
                
                #Get the reference list for the elements of the subframe:
                reflistfile = os.path.join(subframedir, "values")
                if not os.path.exists(reflistfile):
                    raise MissingInformationError(
                        "Invalid model: " + subframedir + " should contain a file called 'values'!"
                    )
                f = open(reflistfile, "r")
                subframe_ref_list = []
                subframe_ref_list = [line.replace("\n", "") for line in f.readlines()]
                f.close()

                vectors = []
                files = os.listdir(subframedir)
                for file in files:
                    if file != "values":
                        try:
                            f = open(os.path.join(subframedir, file))
                            lines = [l.replace("\n", "") for l in f.readlines()]
                            index = 0
                            nbAtoms = int(lines[0].split(" ")[0])
                            index += 1
                            atoms = []
                            for i in range(index, index + nbAtoms):
                                atoms.append(lines[i])
                                index +=1
                            element_from = element.DiscreteElement.factory_from_ref_list(subframe_ref_list, *atoms)

                            transfer_points = []
                            nbConversions = int(lines[index].split(" ")[0])
                            index += 1
                            for i in range(nbConversions):
                                nbAtoms = int(lines[index].split(" ")[0])
                                index += 1
                                atoms = []
                                for i in range(index, index + nbAtoms):
                                    atoms.append(lines[i])
                                    index +=1
                                element_to = element.DiscreteElement.factory_from_ref_list(self.ref_list, *atoms)
                                transfer_factor = float(lines[index])
                                index += 1
                                transfer_points.append((element_to, transfer_factor))
                            vectors.append(DiscreteMappingVector(element_from, *transfer_points))
                            f.close()
                        except:
                            raise InvalidBeliefsFromBeliefsModelError("The file '" + file + "' was not formatted as expected!")

                self.mappings[subframe_name] = DiscreteEvidentialMapping(subframe_name, subframe_ref_list, *vectors)


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
        if model_format not in DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat:
            raise ValueError(
                "model_format: " + str(model_format) + "\n" +
                "The model format should be of the type ModelFormat!"
            )
        
        # ***********
        # XML FORMAT:
        # ***********
        if model_format == DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.XML:
            root = ET.Element("belief-from-beliefs")
            frame = ET.SubElement(root, "frame", {"name":self.frame_name})
            
            for ref in self.ref_list:
                state = ET.SubElement(frame, "state", {})
                state.text = str(ref)

            evidential_mappings = ET.SubElement(root, "evidential-mappings")
            for mapping_name, mapping in self.mappings.items():
                mapping_element = ET.SubElement(evidential_mappings, "evidential-mapping")
                subframe_element = ET.SubElement(mapping_element, "subframe", {"name":mapping.frame_name})
                for ref in mapping.ref_list:
                    state = ET.SubElement(subframe_element, "state")
                    state.text = ref

                for element_from, vector in mapping.vectors.items():
                    vector_element = ET.SubElement(mapping_element, "mapping-vector")
                    ET.SubElement(vector_element, "from", {"element":element_from.formatted_str(*mapping.ref_list)[1:-1].replace(" u ", " ")})
                    for e, v in vector.points.items():
                        element_to = ET.SubElement(vector_element, "to", {"element":e.formatted_str(*self.ref_list)[1:-1].replace(" u ", " ")})
                        element_to.text = str(v)

            f = open(path, "w")
            f.write(prettyxml.pretty_str(root))
            f.close()

        # *****************
        # CUSTOM DIRECTORY:
        # *****************
        elif model_format == DiscreteMassFunctionsFromBeliefsGenerator.ModelFormat.custom_directory:
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

            for mapping_name, mapping in self.mappings.items():
                mapping_dir = os.path.join(real_path, mapping_name)
                os.mkdir(mapping_dir)

                f = open(os.path.join(mapping_dir, "values"), "w")
                for ref in mapping.ref_list:
                    f.write(ref + "\n")
                f.close()

                for element_from, vector in mapping.vectors.items():
                    s = element_from.formatted_str(*mapping.ref_list)[1:-1]
                    f = open(os.path.join(mapping_dir, s.replace(" u ", "")), "w")
                    f.write(str(element_from.cardinal) + " atoms\n")
                    f.write(s.replace(" u ", "\n") + "\n")
                    f.write(str(len(vector.points)) + " conversions\n")
                    for element_to, factor in vector.points.items():
                        f.write(str(element_to.cardinal) + " atoms\n")
                        f.write(element_to.formatted_str(*self.ref_list)[1:-1].replace(" u ", "\n") + "\n")
                        f.write(str(factor) + "\n")
                    f.close()


    ################################################################################

    def is_valid(self):
        """
        Checks if all the models are valid.

        Returns:
            bool -- ``True`` if all the models are valid, ``False`` otherwise.
        """
        for name, model in self.mappings.items():
            if not model.is_valid():
                return False
        return True

    ################################################################################

    def get_evidence(self, *beliefs):
        """
        Gets the evidence given the beliefs and the current belief transfer models.

        Args:
            beliefs (*tuple(str, MassFunction)): The beliefs to transfer in the form
                of tuples (frame_name, mass_function).
        Returns:
            dict{frame_name:MassFunction} -- A dictionary with the name of the subframes
            as keys and the transferred beliefs as values. If the subframe wasn't found
            in the models, then None is set in the dictionary for the corresponding sub-
            frame name.
        """
        results = {}
        for belief in beliefs:
            if belief[0] in self.mappings:
                results[belief[0]] = self.mappings[belief[0]].get_evidence(belief[1])
            else:
                results[belief[0]] = None
        return results



            
