from rply import ParserGenerator
from ast import Number, Letter, Sum, Sub, Div, Mul, Mod, LShift, RShift, Print


class Parser:
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            ['PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'SEMI_COLON', 'SUM', 'SUB', 'DIV', 'MUL', 'MOD',
             'LSHIFT', 'RSHIFT', 'NUMBER', 'LETTER']
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        precedence = (
            ('left', ['SUM', 'SUB']),
            ('left', ['MUL', 'DIV']),
            ('left', ['LSHIFT', 'RSHIFT']),
            ('left', ['MOD']),
        )

        @self.pg.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def program(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('expression : expression SUM term')
        @self.pg.production('expression : expression SUB term')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1].gettokentype()
            if operator == 'SUM':
                return Sum(self.builder, self.module, left, right)
            elif operator == 'SUB':
                return Sub(self.builder, self.module, left, right)

        @self.pg.production('expression : term')
        def expression_term(p):
            return p[0]

        @self.pg.production('term : term MUL factor')
        @self.pg.production('term : term DIV factor')
        def term(p):
            left = p[0]
            right = p[2]
            operator = p[1].gettokentype()
            if operator == 'MUL':
                return Mul(self.builder, self.module, left, right)
            elif operator == 'DIV':
                return Div(self.builder, self.module, left, right)

        @self.pg.production('term : factor')
        def term_factor(p):
            return p[0]

        @self.pg.production('factor : NUMBER')
        @self.pg.production('factor : LETTER')
        def factor(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.production('factor : MOD factor')
        @self.pg.production('factor : LSHIFT factor')
        @self.pg.production('factor : RSHIFT factor')
        def unused_operators(p):
            # Handle these unused tokens here if necessary
            pass

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
