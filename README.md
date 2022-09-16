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


## Usage

```bash
./hackaA.py Example.asm
```
You can also pass a path to the source code file:
```bash
./hacka.py ~/Desktop/Example.asm
```
The resting .hack file will be saved in the current working directory.
### Example.asm source file
```asm
// Computes R0 = 2 + 3  (R0 refers to RAM[0])

@2
D=A
@3
D=D+A
@0
M=D
```
### Resulting Example.hack file
```binary
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000
```

## An Overview of the Hack Assembly Language

  Hack is a simple, minimal, yet elegant and powerful assembly language developed for the 16-bit Hack Computer Architecture.
  Comments are lines that begin with //, `// this is a comment`. The HackA assembler ignores all comments 
  and whitespace in the source file.
  Labels are declared as follows:
  ```asm
  (LOOP)
  ....
  // instructions
  ...
  @LOOP
  0;JMP
  ```
There are two types of instructions in Hack:

### A-instructions
`@value`, where value is either a non-negative constant, or a symbol.
The effects of the A-instructions are:
1. if `value` is a non-negative integer, the **A register** is set to the specified value hence selecting RAM[VALUE] as 
the currently referenced memory location. Apart from referencing memory locations, this is also the only way to load constants
into registers.
   ```asm
   @21  // load 21 into the A register, currently selected RAM adress is RAM[21]
   D=A  // set register D to A, A=21... that is D is set to 21
   ```
2. If `value` is a symbol, then the A register is set to the value of what the symbol refers to in the symbol table. That is
   if `value` is a variable, the **A register** is set to the value of the variable in the symbol table. 

   ```asm
       @var  // var is a refrence to a variable
       D=M // where M is RAM[A]
   ```
   If `value` is a 
   label, then the **A register** is set to the value of the line number(after stripping whitespaces and comments) of the first instruction in the codeblock where the
   label was declared.

    ```asm
   (LOOP)  // this is how to declare a symbol
    ....
   // instructions
   ...
   @LOOP // set A register to the address of the first instruction inside LOOP 
   0;JMP   // jump back to the begining of LOOP
    ```
 

The opcode of an A-instruction is zero that is `0xxxxxxxxxxxxxx`, where `x` is a bit.
### C-instructions
These are instructions used to perform computations. The general format of a C-instruction is:

*DEST*=*COMP*;*JUMP*
Where:
1. *DEST* is the destination register to store the result of a computation.
2. *COMP* is the computation to be performed.
3. *JUMP* is an optional jump directive to specify the next instruction to be executed

Example code:

```asm
(LOOP)
@1 // set A=1
D=A;  // effectively setting D to 1
@LOOP   // where you want to jump to
D;JNQ    //re-execute the loop if D is not equal to zero
```

The opcode of C-instruction is 1 with a general binary format of `1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3`, where:
- `111` bits: C-Instructions always begin with bits `111`.
- `a` bit: Chooses to load the contents of either **A** register or **M** (Main Memory register addressed by **A**) into the ALU for computation.
- Bits `c1` through `c6`: Control bits expected by the ALU to specify the operation to be performed.
- Bits `d1` through `d3`: Specify which memory location to store the result of ALU computation into: **A**, **D** or **M**.
- Bits `j1` through `j3`: Specify which JUMP directive to execute (either conditional or unconditional).

