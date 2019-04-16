## @file regex.py
#  @brief Creates an NFA out of regular expression
#  @date 4/15/2019

from parse import Lexer, Parser, Token, State, NFA, Handler

##@brief Creates an NFA out of regular expression
def compile(p):
    #Initialize symbols into a sequence of tokens
    lexer = Lexer(p)
    #Parse the regular expression 
    parser = Parser(lexer)
    #Create tokens for each character in p
    tokens = parser.parse()
    #Handles NFA construction
    handler = Handler()

    nfa_stack = []
    
    for t in tokens:
        handler.handlers[t.name](t, nfa_stack)

    #return an NFA
    return nfa_stack.pop() 


