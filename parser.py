"""
this module contains functions that work to parse instructions into components/tokens
"""
from code import destination
from code import jump
from code import computation


def replace(symbol, symbol_table):
    """
    This function looks up & replaces a symbol with the corresponding assigned number
    :param symbol: the symbol to look up
    :param symbol_table: the symbol table to look up in
    :return: the assigned number
    """
    return symbol_table.get(symbol)


def strip_space(line):
    """
    This functions strips trailing white spaces & trailing comments
    :param line: the line to strip
    :return: return the stripped line
    """
    head, part, tail = line.partition("//")
    return head.strip()


def a_instruction(instruction, symbol_table):
    """
    This function converts a-instructions to their binary form
    :param symbol_table: symbol table to lookup
    :param instruction: the instruction to convert
    :return: the binary representation of the instruction
    """
    inst = instruction.replace("@", "")
    try:
        number = int(inst)
    except ValueError:
        number = replace(inst, symbol_table)
    code = "{0:b}".format(number)
    return code.zfill(16)


def c_instruction(instruction):
    """
    This function handles c-instructions
    :param instruction: the instruction
    :return: binary representation
    """
    dest, *_ = instruction.rpartition("=")
    *_, compjmp = instruction.rpartition("=")
    comp = compjmp.rsplit(";")[0]
    jmp = (compjmp.rsplit(";") + [""])[1]
    dmnem = destination(dest)
    jmnen = jump(jmp)
    cmnem = computation(comp)
    return "111" + cmnem + dmnem + jmnen


def assemble(instruction, symbol_table):
    """
    This functions identifies the instruction type i.e. a-instruction or c-instruction &
    calls the corresponding function to unpack
    :param symbol_table: symbol table to do lookup
    :param instruction:  the instruction to unpack
    :return: th
    """
    if instruction.startswith("@"):
        code = a_instruction(instruction, symbol_table)
    else:
        code = c_instruction(instruction)
    return code
