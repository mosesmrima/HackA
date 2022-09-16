# HackA

HackA is a 2-pass assembler for the Hack assembly language designed to generate 16-bit machine code for the Hack
computer platform. The Hack computer is a 16-bit computer architecture. This project is one of the stages of building a
16-bit computer from scratch using the book Elements of Computing Systems and the course
[Nand to tetris](https://www.coursera.org/learn/build-a-computer).

## Introduction

HackA takes one commandline argument, the name of a Hack assembly language source code file and produces a text file
containing the corresponding machine code. The source file should have a ".asm" file extension and the output file has 
the same name but with a ".hack" extensions.
Hack is a 2-pass assembler.
### Pass-1
This phase involves 2 activities:

1. Initializing the symbol table with the language's predefined symbols. These inbuilt symbols are:

| Symbol   | Memory Address | Description                                 |
|----------|----------------|---------------------------------------------|
 | R0 - R15 | 0 - 15         | RAM 0 to RAM 15                             |
 | SP       | 0              | Base address of the stack                   |
 | LCL      | 1              | Base address of  local variables segment    |
 | ARG      | 2              | Base address of a functions arguments       |
 | THIS     | 3              | Points to the current object                |
 | THAT     | 4              | Points to the current array being processed |
 | SCREEN   | 16384          | Base address of the screens memory map      |
 | KBD      | 24576          | Memory Map of the keyboard                  |


### Pass-2

In the second pass, HackA scans te entire source code file and adding all the variables and labels into the already 
initialized symbol table. Variables are stored in memory beginning from address 16. Labels are used to identify the 
beginning of a code section hence each label is replaced with line number of the beginning of the code block.


  *The symbol table has been implemented using a dictionary with the symbol name as the key and the address as the value*



  