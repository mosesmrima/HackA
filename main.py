#!/usr/bin/python3
import sys

from symbols import labels, initialize, variables
from parser import strip_space
from parser import assemble


def main():
    asm_path = sys.argv[1]
    hack_path = asm_path.replace(".asm", ".hack")
    symbol_table = initialize()  # initialize the symbol table with inbuilt symbols
    with open(asm_path, "rt") as f:
        """
        This is the first pass where we build the symbol table
        """
        lines = f.readlines()
        count = 0
        for line in lines:
            if line.isspace() or (line.strip().startswith("//")):
                pass
            else:
                line = strip_space(line)
                key = labels(line)
                if key is not None:
                    symbol_table.update({key: count})
                count = count if line.startswith("(") else count + 1

        free = 16  # unused registers begin from address 16, 0-15 are declared to R0-R15
        for line in lines:
            if line.isspace() or (line.strip().startswith("//")):  # skip comments and white spaces
                pass
            else:
                line = strip_space(line)
                key = variables(line, symbol_table)
                if key is not None:
                    symbol_table.update({key: free})
                    free += 1
                    try:
                        """
                        If the variable name, i.e the key in the symbol table, is an integer, remove it from
                        the symbol table since it is a constant/immediate value being loaded into the A register
                        """
                        int(key)
                        symbol_table.pop(key)
                        free -= 1
                    except ValueError:
                        pass

    with open(asm_path, "rt") as f, open(hack_path, "wt") as h:
        """
        This is the second pass where we generate th code
        """
        lines = f.readlines()
        for line in lines:
            if line.isspace() or (line.strip().startswith("//")):  # skip comments and white space
                pass
            else:
                line = strip_space(line)
                if not line.strip().startswith("("):
                    line = assemble(line, symbol_table)  # generate the 16 bit machine code
                    h.write(line + "\n")  # write out the machine code to the .hack file


if __name__ == "__main__":
    main()
