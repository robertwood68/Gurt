###########################################################################################################
#                                           Token                                                         #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/22/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The following class is define an object of type Token that has a value and a type such as string,  #
#      literal, operator, etc.                                                                            #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################
class Token(object):
    def __init__ (self):
        self.value = ""
        self.type = "token"