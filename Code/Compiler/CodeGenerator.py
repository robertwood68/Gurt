"""
CodeGenerator

Generates MIPS and RISC-V assembly language instructions for a .gurt file passed to it

COPYRIGHT: This code is copyright (C) 2023 Robert Wood and Dean Zeller.
"""
# imports
from TerminalColors import bcolors
from WriteFile import writeMIPSFile, writeRISCFile
from Token import Token
import os

# list definitions
MIPSData = [] # list of generated MIPS data section instructions
MIPSText = [] # list of generated MIPS text section instructions
RISCData = [] # list of generated MIPS data section instructions
RISCText = [] # list of generated MIPS text section instructions
allProgramTokens = [] # list of all tokens used inside of the .gurt file

"""
Generates MIPS assembly code for a line of tokenized code from a Gurt program.

Parameters:
- tokenList: List of tokens
- num: Line number
- currentLine: Current line content
- fileName: Name of the file

Return Value:
None
"""
def MIPSCodeGenerator(tokenList, num, currentLine, fileName):
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
                    MIPSData.append(f"print{num}:\t.asciiz\t{nextToken.value}\n\t")
                    MIPSText.append(f"li $v0, 4\n\tla $a0, print{num}\n\tsyscall\n\t")
                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Symbol" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    MIPSText.append(f"li $v0, 1\n\tlw $a0, {nextToken.value}\n\tsyscall\n\t")
                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Literal" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    MIPSText.append(f"li $v0, 1\n\tli $a0, {nextToken.value}\n\tsyscall\n\t")

                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Separator":
                    print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Print statements can not be empty:"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                    writeMIPSFile(getMIPSData(), getMIPSText(), f"Failed - {name}")
                    exit(1)

            ########################### CONDITIONS TO INITIALIZE VARIABLES #############################
            elif prevToken.type == "Keyword" and token.type == "Symbol":
                ####################### INITIALIZE INTEGER VARIABLE ######################
                if prevToken.value == "int" and token.type == "Symbol":
                    # integer initialization with assignment
                    if nextToken.type == "Operator":
                        # integer initialization with assignment of integer (int number = 5;)
                        if nextToken.value == "=" and tokenList[tokenList.index(nextToken) + 1].type == "Literal" and tokenList[len(tokenList)-1].value == ";":
                            MIPSData.append(f"{token.value}:\t.word\t{int(tokenList[tokenList.index(nextToken) + 1].value)}\n\t")
                        # error handling for syntax errors on assignment to integer variable
                        else:
                            print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Expected a symbol or literal after operator \"=\":"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                            writeMIPSFile(getMIPSData(), getMIPSText(), f"Failed - {name}")
                            exit(1)
                    # integer initialization without assignment (int number;)
                    elif nextToken.type == "Separator": 
                        MIPSData.append(f"{token.value}:\t.word\t0\n\t")
                    # error handling for syntax errors when initializing integer variables
                    else:
                        print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Expected an operator or end of line marker \";\" after variable name, not \"{nextToken.value}\":"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                        writeMIPSFile(getMIPSData(), getMIPSText(), f"Failed - {name}")
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
                                MIPSText.append(f"lw $t0, {prevToken.value}\n\tlw $t1, {nextToken.value}\n\tlw $t2, {tokenList[tokenList.index(nextToken) + 2].value}\n\tadd $t0, $t1, $t2\n\tsw $t0, {prevToken.value}\n\t")
                ############################## MODIFY VARIABLE WITH INPUT ###############################
                elif token.value == "=" and nextToken.type == "Keyword":
                    if nextToken.value == "input" and tokenList[tokenList.index(nextToken) + 1].value == "(":
                        if tokenList[tokenList.index(nextToken) + 2].type == "String" and tokenList[tokenList.index(nextToken) + 3].value == ")" and tokenList[len(tokenList)-1].value == ";":
                            MIPSData.append(f"print{num}:\t.asciiz\t{tokenList[tokenList.index(nextToken) + 2].value}\n\t")
                            MIPSText.append(f"li $v0, 4\n\tla $a0, print{num}\n\tsyscall\n\tli $v0, 5\n\tsyscall\n\tsw $v0, {prevToken.value}\n\t")

"""
Returns the list of .data section MIPS instructions to be written to a file.

Return Value:
variableInstr
"""
def getMIPSData():
    return MIPSData

"""
Returns the list of .text section MIPS instructions to be written to a file.

Return Value:
textInstrs
"""
def getMIPSText():
    return MIPSText


"""
Generates RISC-V assembly code for a line of tokenized code from a Gurt program

Parameters:
- tokenList: List of tokens
- num: Line number
- currentLine: Current line content
- fileName: Name of the file

Return Value:
None
"""
def RISCVCodeGenerator(tokenList, num, currentLine, fileName):
    prevToken = Token()
    nextToken = ""
    name, ext = os.path.splitext(fileName)
    for token in tokenList:
        allProgramTokens.append(token)
        # BEGIN READING LINE AT INSTRUCTION START POINT
        if token != tokenList[0] and len(tokenList) != tokenList.index(token) + 1:
            prevToken = tokenList[tokenList.index(token) - 1]
            nextToken = tokenList[tokenList.index(token) + 1]

            # CONDITIONS FOR PRINT STATEMENTS
            if prevToken.type == "Keyword" and token.type == "Separator":
                if prevToken.value == "print" and token.value =="(" and nextToken.type == "String" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    RISCData.append(f"print{num}:\t.asciiz\t{nextToken.value}\n\t")
                    RISCText.append(f"li $v0, 4\n\tla $a0, print{num}\n\tsyscall\n\t")
                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Symbol" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    RISCText.append(f"li $v0, 1\n\tlw $a0, {nextToken.value}\n\tsyscall\n\t")
                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Literal" and tokenList[tokenList.index(nextToken) + 1].value == ")" and tokenList[len(tokenList)-1].value == ";":
                    RISCText.append(f"li $v0, 1\n\tli $a0, {nextToken.value}\n\tsyscall\n\t")

                elif prevToken.value == "print" and token.value =="(" and nextToken.type == "Separator":
                    print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Print statements can not be empty:"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                    writeRISCFile(getRISCData(), getRISCText(), f"Failed - {name}")
                    exit(1)

            # CONDITIONS TO INITIALIZE VARIABLES
            elif prevToken.type == "Keyword" and token.type == "Symbol":
                # INITIALIZE INTEGER VARIABLE
                if prevToken.value == "int" and token.type == "Symbol":
                    # integer initialization with assignment
                    if nextToken.type == "Operator":
                        # integer initialization with assignment of integer (int number = 5;)
                        if nextToken.value == "=" and tokenList[tokenList.index(nextToken) + 1].type == "Literal" and tokenList[len(tokenList)-1].value == ";":
                            RISCData.append(f"{token.value}:\t.word\t{int(tokenList[tokenList.index(nextToken) + 1].value)}\n\t")
                        # error handling for syntax errors on assignment to integer variable
                        else:
                            print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Expected a symbol or literal after operator \"=\":"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                            writeRISCFile(getRISCData(), getRISCText(), f"Failed - {name}")
                            exit(1)
                    # integer initialization without assignment (int number;)
                    elif nextToken.type == "Separator": 
                        RISCData.append(f"{token.value}:\t.word\t0\n\t")
                    # error handling for syntax errors when initializing integer variables
                    else:
                        print(bcolors.BOLD + bcolors.FAIL + bcolors.UNDERLINE +"Compilation Failure\n" + bcolors.ENDC + bcolors.BOLD + "Syntax Error:" + bcolors.ENDC + f" in file \"{fileName}\":\n" + bcolors.BOLD + f"Syntax Error:{num}: " + bcolors.ENDC + bcolors.FAIL + f"error:" + bcolors.ENDC + f" Expected an operator or end of line marker \";\" after variable name, not \"{nextToken.value}\":"  + bcolors.BOLD + f"\n{num} | " + bcolors.OKCYAN + f"\t{currentLine}" + bcolors.ENDC)
                        writeRISCFile(getRISCData(), getRISCText(), f"Failed - {name}")
                        exit(1)

            # MODIFY VARIABLES
            elif prevToken.type == "Symbol" and token.type == "Operator":
                # MODIFICATION WITH PREVIOUSLY DEFINED VARIABLES
                if token.value == "=" and nextToken.type == "Symbol":
                    # MODIFICATION WITH OPERATIONS ON PREVIOUSLY DEFINED VARIABLES
                    if tokenList[tokenList.index(nextToken) + 1].type == "Operator":
                        # MODIFICATION WITH ADDITION OF PREVIOUSLY DEFINED VARIABLES 
                        if tokenList[tokenList.index(nextToken) + 1].value == "+":
                            if tokenList[tokenList.index(nextToken) + 2].type == "Symbol" and tokenList[len(tokenList)-1].value == ";":
                                RISCText.append(f"lw $t0, {prevToken.value}\n\tlw $t1, {nextToken.value}\n\tlw $t2, {tokenList[tokenList.index(nextToken) + 2].value}\n\tadd $t0, $t1, $t2\n\tsw $t0, {prevToken.value}\n\t")
                # MODIFY VARIABLE WITH INPUT 
                elif token.value == "=" and nextToken.type == "Keyword":
                    if nextToken.value == "input" and tokenList[tokenList.index(nextToken) + 1].value == "(":
                        if tokenList[tokenList.index(nextToken) + 2].type == "String" and tokenList[tokenList.index(nextToken) + 3].value == ")" and tokenList[len(tokenList)-1].value == ";":
                            RISCData.append(f"print{num}:\t.asciiz\t{tokenList[tokenList.index(nextToken) + 2].value}\n\t")
                            RISCText.append(f"li $v0, 4\n\tla $a0, print{num}\n\tsyscall\n\tli $v0, 5\n\tsyscall\n\tsw $v0, {prevToken.value}\n\t")

"""
Returns the list of .data section RISC-V instructions to be written to a file.

Return Value:
variableInstr
"""
def getRISCData():
    return RISCData

"""
Returns the list of .text section RISC-V instructions to be written to a file.

Return Value:
textInstrs
"""
def getRISCText():
    return RISCText