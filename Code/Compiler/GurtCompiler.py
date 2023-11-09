###########################################################################################################
#                                          GurtCompiler                                                   #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/24/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The GurtCompiler program calls a variety of different methods and classes from separate programs   #
#      to tokenize a Gurt program file, output each token and its type, ID, and value, and output lists   #
#      of token ID's by what type they are, along with a list of all of the token ID's used throughout    #
#      the Gurt file and a list of all of the unique token ID;s used in the same file.  While this is     #
#      being done, some of the methods attempt to compile the Gurt code into a MIPS assembly program, and #
#      if the code is successfully compiled, a .asm file will be created in the Output folder.  This file #
#      can then be run using the MARSCode VSCode extension, or in the MARS MIPS assembler .jar and the    #
#      output expected from the Gurt file will be the output of the newly created .asm file when run.     #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################

# imports
import os
from PrettyPrinter import specialPrint, uniquePrint
from TokenIDGenerator import generate
from TokenEncoder import tokenEncoder
from PredefinedTokensAndPatterns import common_keywords, operators_list, separators_list
from WriteFile import writeMIPSFile
from CodeGenerator import getTxtInstrs, getVarInstrs
from TerminalColors import bcolors

###########################################################################################################
#      METHOD:             main()                                                                         #
#      DESCRIPTION:        takes the name of a Gurt program file given by the user along with a list of   #
#                          pregenerated encoded tokens (keywords, operators, and separators) and iterates #
#                          over each line, outputs each line with its corresponding number, and prints    #
#                          out each token in each line with its type, token, id, and whether or not it is #
#                          a new token of that type.  During this, the code is compiled and if it         #
#                          compiles successfully, a MIPS .asm file is created that is the assembly        #
#                          equivalent to the Gurt program file passed in by the user.                     #
#      PARAMETERS:         input, filename, codesList                                                     #
#      RETURN VALUE:       none                                                                           #
###########################################################################################################
def main(input, filename, codesList):
    # attempt to open and read file provided
    try:
        with open(filename, 'r') as file:
            # iterator for printing each line number
            line_number = 1

            # create list that holds dictionaries of each token read throughout the program
            tableTokens = []

            # for every line in the file
            for line in file:
                tokens = tokenEncoder(line, codesList, tableTokens, line_number, filename)
                if len(tokens) != 0:

                    # print the line number followed by the current line with leading whitespace stripped
                    print(bcolors.OKBLUE + f'{line_number}.  {line.strip()}' + bcolors.ENDC)

                    # for every token in the list of encoded tokens, print out the type, token, id, and new status fields, then set the new status to blank
                    for tok in tokens:
                        print(bcolors.BOLD + f"\t{tok['type']}\t{tok['token']}\t\tid {tok['id']}\t{tok['new']}" + bcolors.ENDC)
                        tok['new'] = ""
                    print('')

                    # increase the iterator value
                    line_number += 1

            print(bcolors.HEADER + bcolors.UNDERLINE + bcolors.BOLD + "\tSymbol Table:" + bcolors.ENDC)
            for i in range(0, len(tableTokens)):
                if (tableTokens[i]['type'] == "Symbol:\t"):
                    if (tableTokens[i]['printed'] == False):
                        print(bcolors.BOLD + "\t" + str(tableTokens[i]['id']) + "   " + str(tableTokens[i]['token']) + bcolors.ENDC)
                        tableTokens[i]['printed'] = True        

            print(bcolors.HEADER + bcolors.UNDERLINE + bcolors.BOLD + "\n\tLiteral Table:" + bcolors.ENDC)
            for i in range(0, len(tableTokens)):
                if (tableTokens[i]['type'] == "Literal:"):
                    if (tableTokens[i]['printed'] == False):
                        print(bcolors.BOLD + "\t"+str(tableTokens[i]['id']) + "   " + str(tableTokens[i]['token']) + bcolors.ENDC)
                        tableTokens[i]['printed'] = True    
            
            print(bcolors.HEADER + bcolors.UNDERLINE + bcolors.BOLD + "\n\tString Table:" + bcolors.ENDC)
            for i in range(0, len(tableTokens)):
                if (tableTokens[i]['type'] == "String:\t"):
                    if (tableTokens[i]['printed'] == False):
                        print(bcolors.BOLD + "\t"+str(tableTokens[i]['id']) + "   " + str(tableTokens[i]['token']) + bcolors.ENDC)
                        tableTokens[i]['printed'] = True  

            print(bcolors.HEADER + bcolors.UNDERLINE + bcolors.BOLD + "\n\tProgram Codes:" + bcolors.ENDC)
            iterators = [i for i in range(10, 1001, 10)]
            pCodeString = specialPrint(iterators, tableTokens)
            print(bcolors.BOLD + "" + pCodeString + "" + bcolors.ENDC)

            print(bcolors.HEADER + bcolors.UNDERLINE + bcolors.BOLD + "\n\tUnique, In-Order Program Codes:" + bcolors.ENDC)
            uniqueCodeString = uniquePrint(iterators, tableTokens)
            print(bcolors.BOLD + "" + uniqueCodeString + "" + bcolors.ENDC)

    except FileNotFoundError:
        # tell use the file was not found
        print(f"File '{filename}' not found.")

    # send resulting data section and text section instruction lists from the CodeGenerator class to the writeMIPSFile() method from the WriteFile class
    vars = getVarInstrs()
    text = getTxtInstrs()
    writeMIPSFile(vars, text, input)

    print(bcolors.OKGREEN + bcolors.BOLD +"\n\tSuccess!" + bcolors.ENDC + bcolors.BOLD + " Code Compiled!" + bcolors.ENDC)

# executes the code when the file is run directly, rather than imported
if __name__ == "__main__":
    # prompt user for name of file in the current folder
    input = input("Enter the name of a .gurt file in the current directory to compile: ")

    # locate file path, add name of file that the user entered to it, and store in variable "filename"
    name, ext = os.path.splitext(input)
    folder_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(folder_dir, input) 

    # generate predefined token codes and store in variable
    codes = generate(common_keywords, operators_list, separators_list)

    # call main method and pass the filename and token codes list into it
    main(name, filename, codes)