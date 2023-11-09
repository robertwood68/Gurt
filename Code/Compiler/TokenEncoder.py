###########################################################################################################
#                                           TokenEncoder                                                  #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/22/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The following program is used to call the tokenEncoder method in the GurtCompiler program to       #
#      encode each token read on a line in a file passed to the program.                                  #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################

# imports 
import re
import os
from CodeGenerator import codeGenerator
from Token import Token
from PredefinedTokensAndPatterns import (
    symbols, comment_pattern, single_operators, 
    double_operators, string_pattern, symbol_pattern, 
    literal_pattern)

###########################################################################################################
#      METHOD:             tokenEncoder()                                                                 #
#      DESCRIPTION:        tokenizes a single line of text based on common language components and        #
#                          regular expression search patterns and encodes recently found tokens.  Also    #
#                          appends every encoded token to the returned list and a list labled "tokenList" #
#                          that is used print the tokens out in the main function.  Finally, the method   #
#                          calls the codeGenerator() method from the CodeGenerator program to compile     #
#                          each line of code passed through the tokenEncoder() method.                    #
#      PARAMETERS:         line, codes, tableList, num, fileName                                          #
#      RETURN VALUE:       the list of encoded tokens.                                                    #
###########################################################################################################
def tokenEncoder(line, codes, tableList, num, fileName):
    tokensList = [] # initialize list of token objects

    # Remove comments from the line before tokenizing
    line = re.sub(comment_pattern, '', line)

    # combine the regular expressions into searchable pattern variable
    pattern = rf'{double_operators}|{single_operators}|{symbols}|{string_pattern}|\w+' 

    codeGenTokenList = []

    # tokenize the line and categorize tokens
    for match in re.finditer(pattern, line):
        token = Token()
        token.value = str(match.group()) # group match object as token
        
        # check if token exists in list of keyword codes, if so append it to both lists
        for k in range(0, len(codes['kCodes'])):
            if token.value == codes['kCodes'][k]['token']:
                tokensList.append(codes['kCodes'][k])
                tableList.append(codes['kCodes'][k])
                token.type = "Keyword"
        
        # check if token exists in list of operator codes, if so append it to both lists
        for o in range(0, len(codes['oCodes'])):
            if token.value == codes['oCodes'][o]['token']:
                token.type = "Operator"
                tokensList.append(codes['oCodes'][o])
                tableList.append(codes['oCodes'][o])

        # check if token exists in list of separator codes, if so append it to both lists
        for sep in range(0, len(codes['sepCodes'])):
            if token.value == codes['sepCodes'][sep]['token']:
                token.type = "Separator"
                tokensList.append(codes['sepCodes'][sep])
                tableList.append(codes['sepCodes'][sep])

        # check if the token is a string by matching the token to the string pattern variable
        if re.match(string_pattern, token.value):
            status = 0 # set status indicating whether or not to create a new string token or not
            token.type = "String"

            # iterate over every encoded token in the list of string codes
            for string in range(0, len(codes['strCodes'])):
                if token.value == codes['strCodes'][string]['token']: # if the token is in the list
                    status = string # set status to something other than 0
                    codes['strCodes'][string]['new'] = "" # set the new status field to blank
                    tokensList.append(codes['strCodes'][string]) # append the token to the returned list
                    tableList.append(codes['strCodes'][string]) # append the token to the passed in list "tableList" to be printed in main
            if status == 0: # if the status is not set
                # create a new token and append it to both lists
                codes['strCodes'].append({
                    "type": "String:\t",
                    "token": token.value,
                    "id": codes['strCodes'][len(codes['strCodes']) - 1]['id'] + 1,
                    "new": "new string",
                    "printed": False
                })
                tokensList.append(codes['strCodes'][len(codes['strCodes']) - 1])
                tableList.append(codes['strCodes'][len(codes['strCodes']) - 1])

        # Check if the token is a symbol by matching the token with the symbol pattern variable and checking if it does not contain whitespaces
        elif re.match(symbol_pattern, token.value) and not re.search(r'\s', token.value):
            status = 0 # set status indicating whether or not to create a new symbol token or not
            breakStatus = 0 # set break status indicating whether or not to create a new string token or not
            
            # double check that token is not a keyword, if it is skip the appending operations
            for i in range(0, len(codes['kCodes'])):
                if token.value == codes['kCodes'][i]['token']:
                    breakStatus = 1

            if breakStatus != 1:       
                # generate id for it if not already generated, set status variable, and append to both lists
                for sym in range(0, len(codes['symCodes'])):
                    if token.value == codes['symCodes'][sym]['token']:
                        status = 1
                        tokensList.append(codes['symCodes'][sym])
                        tableList.append(codes['symCodes'][sym])
                        token.type = "Symbol"
                
                # if both statuses are unchanged, create a new encoded symbol token and append to both lists
                if breakStatus == 0:
                    if status == 0:
                        codes['symCodes'].append({
                            "type": "Symbol:\t",
                            "token": token.value,
                            "id": codes['symCodes'][len(codes['symCodes']) - 1]['id'] + 1,
                            "new": "new symbol",
                            "printed": False
                        })
                        tokensList.append(codes['symCodes'][len(codes['symCodes']) - 1])
                        tableList.append(codes['symCodes'][len(codes['symCodes']) - 1])
                        token.type = "Symbol"
        
        # Check if the token is a literal by matching the token with the literal pattern variable
        elif re.match(literal_pattern, token.value):
            token.type = "Literal"
            status = 0 # set status indicating whether or not to create a new literal token or not
            # generate id for it if not already generated, set status and append to both lists if it is in the existing list of literals
            for lit in range(0, len(codes['litCodes'])):
                if token.value == codes['litCodes'][lit]['token']:
                    status = lit
                    codes['litCodes'][lit]['new'] = ""
                    tokensList.append(codes['litCodes'][lit])
                    tableList.append(codes['litCodes'][lit])

            # if the status is unchanged, create a new encoded literal token and append to both lists
            if status == 0:
                codes['litCodes'].append({
                    "type": "Literal:",
                    "token": token.value,
                    "id": codes['litCodes'][len(codes['litCodes']) - 1]['id'] + 1,
                    "new": "new literal",
                    "printed": False
                })
                tokensList.append(codes['litCodes'][len(codes['litCodes']) - 1])
                tableList.append(codes['litCodes'][len(codes['litCodes']) - 1])
        codeGenTokenList.append(token)

    # pass parameters to codeGenerator method to compile the tokenized line of code
    fileName = os.path.basename(fileName)
    codeGenerator(codeGenTokenList, num, line, fileName)

    # return a list of all encoded tokens from the line of the file passed into the function
    return tokensList