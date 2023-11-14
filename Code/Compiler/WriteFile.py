"""
WriteRISCFile

Writes a RISC-V assembly program in the correct format using two lists passed to the writeRISCFile() method. The writing order of the program to the .asm file is: .globl main -> .data: -> .text: -> main: -> done

COPYRIGHT: This code is copyright (C) 2023 Robert Wood and Dean Zeller.
"""
# imports
import os

"""
Description:
Takes two lists, one of data section instructions and one of text section instructions, and writes the instructions in order by section to a .asm file of the name {fileName}Compiled.asm.

Parameters:
- variableInstructions: list of variable instructions
- textInstructions: list of text instructions
- fileName: the name if the file to create/write to

Return Value:
None
"""
def writeMIPSFile(variableInstructions, textInstructions, fileName):
        with open(getOutputPath(fileName), 'w') as file:
            file.write(".globl main\n.data:\n\t")
            for var in variableInstructions:      
                file.write(var)
            file.write("\n.text:\nmain:\n\t")
            for instr in textInstructions:
                 file.write(instr)
            exitInstruction = "li $v0, 10\n\tsyscall"
            file.write(exitInstruction)
            
"""
Description:
Takes two lists, one of data section instructions and one of text section instructions, and writes the instructions in order by section to a .asm file of the name {fileName}Compiled.asm.

Parameters:
- variableInstructions: list of variable instructions
- textInstructions: list of text instructions
- fileName: the name if the file to create/write to

Return Value:
None
"""
def writeRISCFile(variableInstructions, textInstructions, fileName):
        with open(getOutputPath(fileName), 'w') as file:
            file.write(".globl main\n.data:\n\t")
            for var in variableInstructions:      
                file.write(var)
            file.write("\n.text:\nmain:\n\t")
            for instr in textInstructions:
                 file.write(instr)
            exitInstruction = "li $v0, 10\n\tsyscall" ############# Need to edit this for RISC ###############
            file.write(exitInstruction)

"""
Description:
Takes the name of the file that the user entered in the GurtCompiler program, modifies the current path of the current script to make the writing file path of the .asm file two directories higher than current, then adds "/Output/{fileName}Compiled.asm" to the path to pass the variable to the writeMIPSFile() and writeRISCFile() methods

Parameters:
- fileName: the name if the file to create/write to

Return Value:
The path to write the file to
"""
def getOutputPath(fileName):
    # get the path of the current script
    currentFile = os.path.abspath(__file__)
    # get the parent directory path (compiler directory)
    parent_directory = os.path.dirname(currentFile)
    # get grandparent directory path (Assignment 7 Code directory)
    gparent_dir = os.path.dirname(parent_directory)
    # return path to output file
    folderPath = os.path.join(gparent_dir, "CompiledOutput")
    folderPath = os.path.join(folderPath, "MIPS")
    return os.path.join(folderPath, fileName + "Compiled.asm")

################ NEED TO ADD RISC PATH TO THIS METHOD ###################