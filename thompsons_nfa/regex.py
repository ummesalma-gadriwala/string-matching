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


reg = compile("(a|b)a*")
print(reg.match("ba"))
nfa = ApproximateNFA("(a|b)a*")
app = nfa.approximateNFA("ba")

print(nfa.pretty_states())


##reg = compile("(a|b)a*")
approx = ApproximateNFA("(a|b)a*")
app = approx.approximateNFA("ba")
start = app.start
print("Start: ",start.name)
end = app.end.name
print("End: ",end)
dictionary = approx.nfaTOdictionary(app)
#print(dictionary)
lengthOfPath = breadth_first_search(dictionary, start)
#print("BFS on graph:", lengthOfPath)
