###########################################################################################################
#                                           CodeGenerator                                                 #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/22/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The following program is used to generate the MIPS assmebly language instructions equivalent to    #
#      the .gurt file passed to the GurtCompiler program.                                                 #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################

# imports
from TerminalColors import bcolors
from WriteFile import writeMIPSFile
from Token import Token
import os

# list of generated data section instructions
variableInstr = []

# list of generated text section instructions
textInstr = []

# list of all tokens used inside of the .gurt file
allProgramTokens = []

###########################################################################################################
#      METHOD:             codeGenerator()                                                                #
#      DESCRIPTION:        reads over a line of tokenized code from a tokenized Gurt program and          #
#                          generates the MIPS assembly code for that line and stores it in a list of      #
#                          instructions for the data and text sections of a MIPS assembly program.        #
#      PARAMETERS:         tokenList, num, currentLine, fileName                                          #
#      RETURN VALUE:       none                                                                           #
###########################################################################################################
def codeGenerator(tokenList, num, currentLine, fileName):
    prevToken = Token()
    nextToken = ""
    name, ext = os.path.splitext(fileName)
    for token in tokenList:
        allProgramTokens.append(token)
    
        ###################### BEGIN READING LINE AT INSTRUCTION START POINT #################
        if token != tokenList[0] and len(tokenList) != tokenList.index(token) + 1:
            prevToken = tokenList[tokenList.index(token) - 1]
            nextToken = tokenList[tokenList.index(token) + 1]

            ####################### CONDITIONS FOR PRINT STATEMENTS ##########################
            if prevToken.type == "Keyword" and token.type == "Separator":
                if prevToken.value == "print" and token.value =="(" and nextToken.type == "String" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    variableInstr.append(f"print{num}:\t.asciiz\t{nextToken.value}\n\t")
                    textInstr.append(f"li $v0, 4\n\tla $a0, print{num}\n\tsyscall\n\t")
                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Symbol" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    textInstr.append(f"li $v0, 1\n\tlw $a0, {nextToken.value}\n\tsyscall\n\t")
                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Literal" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    textInstr.append(f"li $v0, 1\n\tli $a0, {nextToken.value}\n\tsyscall\n\t")

                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Separator":
                    print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Print statements can not be empty:"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                    writeMIPSFile(getVarInstrs(), getTxtInstrs(), f"Failed - {name}")
                    exit(1)

            ########################### CONDITIONS TO INITIALIZE VARIABLES #############################
            elif prevToken.type == "Keyword" and token.type == "Symbol":
                ####################### INITIALIZE INTEGER VARIABLE ######################
                if prevToken.value == "int" and token.type == "Symbol":
                    # integer initialization with assignment
                    if nextToken.type == "Operator":
                        # integer initialization with assignment of integer (int number = 5;)
                        if nextToken.value == "=" and tokenList[tokenList.index(nextToken) + 1].type == "Literal" and tokenList[len(tokenList)-1].value == ";":
                            variableInstr.append(f"{token.value}:\t.word\t{int(tokenList[tokenList.index(nextToken) + 1].value)}\n\t")
                        # error handling for syntax errors on assignment to integer variable
                        else:
                            print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Expected a symbol or literal after operator \"=\":"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                            writeMIPSFile(getVarInstrs(), getTxtInstrs(), f"Failed - {name}")
                            exit(1)
                    # integer initialization without assignment (int number;)
                    elif nextToken.type == "Separator": 
                        variableInstr.append(f"{token.value}:\t.word\t0\n\t")
                    # error handling for syntax errors when initializing integer variables
                    else:
                        print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Expected an operator or end of line marker \";\" after variable name, not \"{nextToken.value}\":"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                        writeMIPSFile(getVarInstrs(), getTxtInstrs(), f"Failed - {name}")
                        exit(1)

            ############################## MODIFY VARIABLES ###############################
            elif prevToken.type == "Symbol" and token.type == "Operator":
                ########################## MODIFICATION WITH PREVIOUSLY DEFINED VARIABLES ###############################
                if token.value == "=" and nextToken.type == "Symbol":
                    ########################## MODIFICATION WITH OPERATIONS ON PREVIOUSLY DEFINED VARIABLES ###############################
                    if tokenList[tokenList.index(nextToken) + 1].type == "Operator":
                        ########################## MODIFICATION WITH ADDITION OF PREVIOUSLY DEFINED VARIABLES ###############################
                        if tokenList[tokenList.index(nextToken) + 1].value == "+":
                            if tokenList[tokenList.index(nextToken) + 2].type == "Symbol" and tokenList[len(tokenList)-1].value == ";":
                                textInstr.append(f"lw $t0, {prevToken.value}\n\tlw $t1, {nextToken.value}\n\tlw $t2, {tokenList[tokenList.index(nextToken) + 2].value}\n\tadd $t0, $t1, $t2\n\tsw $t0, {prevToken.value}\n\t")
                ############################## MODIFY VARIABLE WITH INPUT ###############################
                elif token.value == "=" and nextToken.type == "Keyword":
                    if nextToken.value == "input" and tokenList[tokenList.index(nextToken) + 1].value == "(":
                        if tokenList[tokenList.index(nextToken) + 2].type == "String" and tokenList[tokenList.index(nextToken) + 3].value == ")" and tokenList[len(tokenList)-1].value == ";":
                            variableInstr.append(f"print{num}:\t.asciiz\t{tokenList[tokenList.index(nextToken) + 2].value}\n\t")
                            textInstr.append(f"li $v0, 4\n\tla $a0, print{num}\n\tsyscall\n\tli $v0, 5\n\tsyscall\n\tsw $v0, {prevToken.value}\n\t")

###########################################################################################################
#      METHOD:             getVarInstrs()                                                                 #
#      DESCRIPTION:        returns the list of .data section MIPS instructions to be written to a file.   #
#      PARAMETERS:         none                                                                           #
#      RETURN VALUE:       variableInstr                                                                  #
###########################################################################################################
def getVarInstrs():
    return variableInstr

###########################################################################################################
#      METHOD:             getTxtInstrs()                                                                 #
#      DESCRIPTION:        returns the list of .text section MIPS instructions to be written to a file.   #
#      PARAMETERS:         none                                                                           #
#      RETURN VALUE:       textInstrs                                                                     #
###########################################################################################################
def getTxtInstrs():
    return textInstr