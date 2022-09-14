"""
This module contains three functions that handle initialization of
the symbol table, handling symbols and variables
"""


def initialize():
    """
    This function initializes the symbol table with te language's inbuilt symbols.
    These symbols include, registers 0 to 15 identified by the symbol R0-R15, KBD, SCREEN, SP,LCL.ARG, THIS,THAT.
    :return: dictionary containing the symbol name as the key and te numerical value/address of the register
    """
    return {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }


def labels(line):
    """
    This function check whether the current line is a symbol and removes the parenthesis
    surrounding the label
    :param line: current line being processed
    :return: the label name without the parenthesis.
    """
    if line.startswith("("):
        line = line.replace("(", "").replace(")", "")
        return line


def variables(line, symbol_table):
    """
    This function checks whether the current line is a variable declaration
    and then adds it to the symbol table if it does not already exist.
    :param line: the current line of code being processed
    :param symbol_table: the symbol table
    :return: the variable name if it des not already exist in the symbol table, else returns none
    """

    if line.startswith("@"):
        line = line.replace("@", "")
        if line not in symbol_table:
            return line
