###########################################################################################################
#                                           TokenIDGenerator                                              #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/22/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The following class is used to call the generate method in the GurtCompiler class to generate an   #
#      initial list of token IDs which will have any new tokens added to it throughout execution.         #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################

###########################################################################################################
#      METHOD:             generate                                                                       #
#      DESCRIPTION:        takes a list of the most common keywords, operators, and separators accross    #
#                          all languages and generates dictionaries for each that include their type,     #
#                          token, id, new status, and printed status.                                     #
#      PARAMETERS:         kw, op, and sep                                                                #
#      RETURN VALUE:       a list of all keyword, operator, and separator codes                           #
###########################################################################################################
def generate(kw, op, sep):
    keywordCodes = [] # create a list of codes for keywords
    operatorCodes = [] # create a list of codes for operators
    symbolCodes = [{"type": "Symbol:\t", "token": "x", "id": 400, "new": "new symbol", "printed": False}] # create a list of codes for separators
    separatorCodes = [] # create a list of codes for separators
    literalCodes = [{"type": "Literal:", "token": 0, "id": 700, "new": "new literal", "printed": False}] # create a list of codes for literals
    stringCodes = [{"type": "String:\t", "token": "", "id": 950, "new": "new string", "printed": False}] # create a list of codes for literals

    commonIter = 100 # initialize common iterator for all loops

    # iterate over list of keywords and assign a code to each of them, incrementing the common iter by 1 each loop
    for keyword in kw:
        keywordCodes.append({
            "type": "Keyword:",
            "token": keyword,
            "id": commonIter,
            "new": "",
            "printed": False
            })
        commonIter = commonIter + 1
        
    commonIter = 300 # set starting range for operators

    # iterate over list of operators and assign a code to each of them, incrementing the common iter by 1 each loop
    for operator in op:
        operatorCodes.append({
            "type": "Operation:",
            "token": operator,
            "id": commonIter,
            "new": "",
            "printed": False
            })
        commonIter = commonIter + 1

    commonIter = 650 # set starting range for separators

    # iterate over list of separators and assign a code to each of them, incrementing the common iter by 1 each loop
    for separator in sep:
        separatorCodes.append({
            "type": "Separator:",
            "token": separator,
            "id": commonIter,
            "new": "",
            "printed": False
            })
        commonIter = commonIter + 1

    tokenCodes = {
            'kCodes': keywordCodes, 
            'oCodes': operatorCodes,
            'symCodes': symbolCodes,
            'sepCodes': separatorCodes,
            'litCodes': literalCodes,
            'strCodes': stringCodes
        }
    # return each list of token codes
    return tokenCodes