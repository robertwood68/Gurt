from rply import LexerGenerator


class Lexer:
    """
    Class: Lexer

    Description:
    Initializes an instance object as a lexer, adds tokens to it, and builds the object into a lexer.

    Parameters:
    - None

    Returns:
    - None
    """

    def __init__(self):
        """
        Method: __init__

        Description:
        Initializes the 'self' object passed in as a lexer.

        Parameters:
        - self: The instance of the object to initialize.

        Returns:
        - None
        """
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        """
        Method: _add_tokens

        Description:
        Adds tokens to the `self` object passed in.

        Parameters:
        - self: The instance of the object to add tokens to.

        Returns:
        None
        """
        # print, input, and return
        self.lexer.add('PRINT', r'print')
        self.lexer.add('INPUT', r'input')
        self.lexer.add('RETURN', r'return')

        # parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        # semi-colon
        self.lexer.add('SEMI_COLON', r'\;')

        # operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('MOD', r'\%')
        self.lexer.add('LSHIFT', r'\<<')
        self.lexer.add('RSHIFT', r'\>>')
        self.lexer.add('EQUAL', r'\=')
        self.lexer.add('ORDER_OF_OPERATIONS', r'\:')

        # bitwise operators
        self.lexer.add('BW_AND', r'\&')
        self.lexer.add('BW_OR', r'\|')
        self.lexer.add('BW_NOT', r'\~')
        self.lexer.add('BW_XOR', r'\^')

        # functions
        self.lexer.add('DEFINE', r'define')
        self.lexer.add('MAIN', r'main')
        self.lexer.add('FUNC_START', r'\{')
        self.lexer.add('FUNC_END', r'\}')

        # conditionals
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE_IF', r'elseif')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('LESS_THAN', r'\<')
        self.lexer.add('LESS_OR_EQUAL', r'\<=')
        self.lexer.add('GREATER_THAN', r'\>')
        self.lexer.add('GREATER_OR_EQUAL', r'\>=')
        self.lexer.add('EQUAL_TO', r'\==')
        self.lexer.add('NOT_EQUAL_TO', r'\!=')
        self.lexer.add('AND', r'\&&')
        self.lexer.add('OR', r'\|\|')

        # loops
        self.lexer.add('FOR', r'for')
        self.lexer.add('WHILE', r'while')

        # number and letter
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('LETTER', r'[a-zA-Z]')

        # data types
        self.lexer.add('INTEGER', r'int')
        self.lexer.add('FLOAT', r'flt')
        self.lexer.add('DOUBLE', r'dbl')
        self.lexer.add('STRING', r'str')
        self.lexer.add('BINARY', r'bin')

        # ignore whitespace
        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        """
        Method: get_lexer

        Description:
        Calls the '_add_tokens' method on the `self` object passed in and returns the built lexer.

        Parameters:
        - self: The instance of the object to build as the lexer.

        Returns:
        - The built lexer
        """
        self._add_tokens()
        return self.lexer.build()
