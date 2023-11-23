from lexer import Lexer
from parser import Parser
from codegen import CodeGen

filename = str(input("Input the name of the file to compile: "))
with open(filename) as f:
    text_input = f.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()

codegen.create_ir()
codegen.save_ir("output.ll")

# llc -filetype=o output.ll
# gcc output.o -o output
# ./output