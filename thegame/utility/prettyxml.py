################################################################################
# thegame.utility.prettyxml.py                                                 #
# ---------------------------------------------------------------------------- #
# Author : Bastien Pietropaoli                                                 #
# Contact: Bastien.Pietropaoli@insight-centre.org                              #
#          Bastien.Pietropaoli@gmail.com                                       #
# ---------------------------------------------------------------------------- #
# This module contains methods to write pretty xml files without the need for  #
# external library. It uses only the standard xml.etree.ElementTree.           #
# This is not a complete library, it just offers an equivalent for the func-   #
# tion pretty_print() (called pretty_str() as it returns a string and does not #
# print anything).                                                             #
################################################################################


import xml.etree.ElementTree as ET


def pretty_str(element, encoding="us-ascii", xml_declaration=True, indent=4):
    """
    Gets a string of the provided XML element.

    Args:
        element (xml.etree.ElementTree.Element): The element to get as a string.
        encoding (str): The encoding of the XML string.
        xml_declaration (bool): If the declaration line is required or not.
        indent (int): The number of spaces to use in the indentation.
    Returns:
        str -- A pretty string ready to be written in a file.
    """
    def print_node(nb_indents, node):
        node_str = " " * indent * nb_indents

        has_children = False
        for element in list(node):
            has_children = True
        close_it = False
        if (node.text == None or node.text == "") and not has_children:
            close_it = True

        node_str += "<" + str(node.tag)
        for name, value in node.items():
            node_str += " " + name + '="' + str(value) + '"'
            
        if close_it:
            node_str += "/>\n"
        elif not has_children:
            node_str += ">" + str(node.text) + "</" + node.tag + ">\n"
        else:
            node_str += ">\n"
            for element in list(node):
                node_str += print_node(nb_indents + 1, element)
            node_str += " " * indent * nb_indents + "</" + node.tag + ">\n"
        return node_str
    
    result = ""

    #xml declaration and encoding:
    if xml_declaration == True:
        result += "<?xml version='1.0'"
        if encoding != None and encoding != "":
            result += " encoding='us-ascii'"
        result += "?>\n"

    #Tree:
    result += print_node(0, element)

    return result
