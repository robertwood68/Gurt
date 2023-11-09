###########################################################################################################
#                                               PrettyPrinter                                             #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/22/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The following program is used to call the specialPrint() and uniquePrint() methods inside of the   #
#      GurtCompiler program.                                                                              #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################

###########################################################################################################
#      METHOD:             specialPrint()                                                                 #
#      DESCRIPTION:        takes a list of iterator values and a list of encoded tokens and creates a     #
#                          printable string that organizes the program codes of each token in order at    #
#                          5 codes per line                                                               #
#      PARAMETERS:         iter, tokens                                                                   #
#      RETURN VALUE:       an organized printable string of program codes                                 #
###########################################################################################################
def specialPrint(iter, tokens):
    codeString = "\t"  # Starting tab of string
    tab_count = 0  # Initialize the tab count

    for i in range(len(tokens)):
        if i >= iter[tab_count]:
            codeString += "\n\t"
            tab_count += 1
        codeString += str(tokens[i]['id']) + "  "

    return codeString

###########################################################################################################
#      METHOD:             uniquePrint()                                                                  #
#      DESCRIPTION:        takes a list of iterator values and a list of encoded tokens and creates a     #
#                          printable string that organizes the program codes of each token in order at    #
#                          5 codes per line, but only prints unique codes generated and prints them in    #
#                          ascending order.                                                               #
#      PARAMETERS:         iter, tokens                                                                   #
#      RETURN VALUE:       a sorted, unique, and printable string of program codes                        #
###########################################################################################################
def uniquePrint(iter, tokens):
    codeString = "\t"  # Starting tab of string
    tab_count = 0  # Initialize the tab count
    codesList = []

    for i in range(len(tokens)):
        codesList.append(tokens[i]['id'])
    
    codesList = list(set(codesList))
    codesList.sort()
    
    for i in range(len(codesList)):
        if i >= iter[tab_count]:
            codeString += "\n\t"
            tab_count += 1
        codeString += str(codesList[i]) + "  "

    return codeString