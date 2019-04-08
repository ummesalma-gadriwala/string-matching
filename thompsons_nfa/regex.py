from parse import Lexer, Parser, Token, State, NFA, Handler
from approx_parse import *

def compile(p, debug = False):
    
    def print_tokens(tokens):
        for t in tokens:
            print(t)

    lexer = Lexer(p)
    parser = Parser(lexer)
    tokens = parser.parse()

    handler = Handler()
    
    if debug:
        print_tokens(tokens) 

    nfa_stack = []
    
    for t in tokens:
        handler.handlers[t.name](t, nfa_stack)
    
    assert len(nfa_stack) == 1
    return nfa_stack.pop() 


reg = compile("(a|b)a*", True)
approx = ApproximateNFA(reg)
app = approx.approximateNFA("ba")
