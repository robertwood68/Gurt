###########################################################################################################
#                                     PredefinedTokensAndPatterns                                         #
#      PROGRAMMER:         Robert Wood                                                                    #
#      COURSE:             CS340                                                                          #
#      DATE:               10/22/2023                                                                     #
#      REQUIREMENT:        Assignment 7                                                                   #
#                                                                                                         #
#      DESCRIPTION:                                                                                       #
#      The following class is simply a storage method for lists of tokens for the GurtCompiler class and  #
#      search patterns for the TokenEncoder class.                                                        #
#                                                                                                         #
#      COPYRIGHT:  This code is copyright (C) 2023 Robert Wood and Dean Zeller.                           #
#                                                                                                         #
###########################################################################################################

# define a list of the most common keywords across programming languages
common_keywords = [
    "if", "else", "for", "in", "return", "class", "import", "from", "while",
    "do", "try", "catch", "finally", "break", "switch", "case", "throw",
    "async", "await", "new", "this", "super", "default", "int", "float",
    "double", "string", "char", "public", "boolean", "byte", "extends",
    "final", "implements", "instanceof", "interface", "long", "native",
    "package", "private", "protected", "short", "static", "strictfp",
    "synchronized", "transient", "false", "null", "true", "void",
    "and", "as", "assert", "elif", "enum", "except", "global", "lambda",
    "nonlocal", "not", "or", "pass", "with", "yield", "auto", "goto", "inline",
    "mutable", "namespace", "operator", "sealed", "stackalloc", "unchecked",
    "unsafe", "virtual", "volatile", "fixed", "decimal", "event", "override",
    "params", "readonly", "ref", "sbyte", "ushort", "ulong", "var", "extern",
    "dynamic", "object", "params", "out", "delegate", "lock", "async", "let",
    "const", "await", "else", "false", "finally", "switch", "this", "System", 
    "print", "println", "String", "bool", "not in", "input"
]

# define a list of the most common operators across programming languages
operators_list = [
    "++", "--", "==", "!=", ">=", "<=",
    "&&", "||", "!", "&", "|", "^", "~", ">>", "<<", ">>>", ">>>=", ">>=", "<<=",
    "&=", "|=", "^=", "~=", "+=", "-=", "*=", "/=", "%=", "?:",
    "=>", "is", "is not", "delete", "typeid", 
    "dynamic_cast", "static_cast", "const_cast", "reinterpret_cast", "->", "as", "nameof", 
    "sizeof", "typeof", "+", "-", "*", "/", "%", ">", "<", "=", "?",
]

# define a regular expression search pattern that identifies common keywords accross programming languages
keywords = r'\b(if|else|while|for|in|def|class|import|from|return|function|var|let|const|while|do|switch|case|break|try|catch|finally|throw|async|await|new|this|super|module|export|default|int|float|double|string|char|input)\b'

# define a regular expression search pattern that identifies common symbols accross programming languages
symbols = r'(\(|\)|\[|\]|\{|\}|\,|;|:|\.|->|\+=|-=|\*=|/=|%=|\*=|/=|<<|>>|>>>|\||&|\?)'

# define a list of the most common separators across programming languages
separators_list = [",", ";", "{", "}", "(", ")", "[", "]", ".", ":", "~"]

# define the regular expression pattern to match double operators first
double_operators = r'(>>>=|>>>|<=|>=|==|!=|\+\+|--|\+=|-=|\*=|/=|%=|&=|\|=|\^=|~=|&&|\|\||\*\*)' 

# define the regular expression pattern to match single operators
single_operators = r'(\+|-|\*|/|<|>|=|%|!|&|\||\^|~)' 

# define the regular expression pattern to match comments and remove them
comment_pattern = r'(/\*[\s\S]*?\*/|//.*|(?:(?<!\\)(?:\\\\)*)#.*)' 

# define the regular expression pattern to match strings
string_pattern = r'("[^"]*"|\'[^\']*\')' 

# regular expression pattern to match a literal (a number, also allows for integers and float numbers)
literal_pattern = r'^[+-]?\d+(\.\d+)?$' 

# define regular expression pattern to match valid variable names
symbol_pattern = r'^(?!if|else|for|while|do|class|function)[a-zA-Z_][a-zA-Z0-9_]*$|.*_$|.*\(.*\)|[a-z][a-zA-Z0-9]*' 