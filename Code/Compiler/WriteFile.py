###########################################################################################################
#                                           WriteFile                                                     #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/22/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The following program is used to write a MIPS assembly program in the correct format using two     #
#      lists passed to the writeMIPSFile() method.  The writing order of the program to the .asm file is: #
#      .globl main -> .data: -> .text: -> main: -> done                                                   #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################

# imports
import os

###########################################################################################################
#      METHOD:             writeMIPSFile()                                                                #
#      DESCRIPTION:        takes two lists, one of data section instructions and one of text section      #
#                          instructions, and writes the instructions in order by section to a .asm file   #
#                          of the name {fileName}Compiled.asm.                                            #
#      PARAMETERS:         variableInstructions, textInstructions, fileName                               #
#      RETURN VALUE:       none                                                                           #
###########################################################################################################
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

###########################################################################################################
#      METHOD:             writeRISCVFile()                                                               #
#      DESCRIPTION:        takes two lists, one of data section instructions and one of text section      #
#                          instructions, and writes the instructions in order by section to a .asm file   #
#                          of the name {fileName}Compiled.asm.                                            #
#      PARAMETERS:         variableInstructions, textInstructions, fileName                               #
#      RETURN VALUE:       none                                                                           #
###########################################################################################################
def writeRISCVFile(variableInstructions, textInstructions, fileName):
        with open(getOutputPath(fileName), 'w') as file:
            file.write(".globl main\n.data:\n\t")
            for var in variableInstructions:      
                file.write(var)
            file.write("\n.text:\nmain:\n\t")
            for instr in textInstructions:
                 file.write(instr)
            exitInstruction = "li $v0, 10\n\tsyscall"
            file.write(exitInstruction)

###########################################################################################################
#      METHOD:             getOutputPath()                                                                #
#      DESCRIPTION:        takes the name of the file that the user entered in the GurtCompiler program,  #
#                          modifies the current path of the current script to make the writing file path  #
#                          of the .asm file two directories higher than current, then adds                #
#                          "/Output/{fileName}Compiled.asm" to the path to pass the variable to the       #
#                          writeMIPSFile() method.                                                        #
#      PARAMETERS:         filename                                                                       #
#      RETURN VALUE:       the desired file path to write the assembly file to                            #
###########################################################################################################
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