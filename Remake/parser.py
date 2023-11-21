from rply import ParserGenerator
from ast import Number, Letter, Sum, Sub, Div, Mul, Mod, LShift, RShift, Print


class Parser:
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # a list of all token names accepted by the parser.
            ['PRINT',  'OPEN_PAREN', 'CLOSE_PAREN', 'SEMI_COLON', 'SUM', 'SUB', 'DIV', 'MUL', 'MOD',
             'LSHIFT', 'RSHIFT', 'NUMBER', 'LETTER']
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    # 'INPUT', 'RETURN', 'EQUAL', 'ORDER_OF_OPERATIONS', 'BW_AND', 'BW_OR', 'BW_NOT', 'BW_XOR', 'DEFINE', 'MAIN',
    # 'FUNC_START', 'FUNC_END', 'IF', 'ELSE_IF', 'ELSE', 'LESS_THAN', 'LESS_OR_EQUAL', 'GREATER_THAN',
    # 'GREATER_OR_EQUAL', 'EQUAL_TO', 'NOT_EQUAL_TO', 'AND', 'OR', 'FOR', 'WHILE', 'INTEGER',
    # 'FLOAT', 'DOUBLE', 'STRING', 'BINARY'
    def parse(self):
        @self.pg.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def program(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression DIV expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression MOD expression')
        @self.pg.production('expression : expression LSHIFT expression')
        @self.pg.production('expression : expression RSHIFT expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MUL':
                return Mul(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MOD':
                return Mod(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'LSHIFT':
                return LShift(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'RSHIFT':
                return RShift(self.builder, self.module, left, right)

        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.production('expression : LETTER')
        def letter(p):
            return Letter(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
