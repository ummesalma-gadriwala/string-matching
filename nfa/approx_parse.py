class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value

class Lexer:
    def __init__(self, pattern):
        self.source = pattern
        self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT', '+':'PLUS', '?':'QMARK'}
        self.current = 0
        self.length = len(self.source)
       
    def get_token(self): 
        if self.current < self.length:
            c = self.source[self.current]
            self.current += 1
            if c not in self.symbols.keys(): # CHAR
                token = Token('CHAR', c)
            else:
                token = Token(self.symbols[c], c)
            return token
        else:
            return Token('NONE', '')

class ParseError(Exception):pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.lookahead = self.lexer.get_token()
    
    def consume(self, name):
        if self.lookahead.name == name:
            self.lookahead = self.lexer.get_token()
        elif self.lookahead.name != name:
            raise ParseError

    def parse(self):
        self.exp()
        return self.tokens
    
    def exp(self):
        self.term()
        if self.lookahead.name == 'ALT':
            t = self.lookahead
            self.consume('ALT')
            self.exp()
            self.tokens.append(t)

    def term(self):
        self.factor()
        if self.lookahead.value not in ')|':
            self.term()
            self.tokens.append(Token('CONCAT', '\x08'))
    
    def factor(self):
        self.primary()
        if self.lookahead.name in ['STAR', 'PLUS', 'QMARK']:
            self.tokens.append(self.lookahead)
            self.consume(self.lookahead.name)

    def primary(self):
        if self.lookahead.name == 'LEFT_PAREN':
            self.consume('LEFT_PAREN')
            self.exp()
            self.consume('RIGHT_PAREN')
        elif self.lookahead.name == 'CHAR':
            self.tokens.append(self.lookahead)
            self.consume('CHAR')

class State:
    def __init__(self, name):
        self.epsilon = [] # epsilon-closure
        self.transitions = {} # (epsilon, char) : state
        self.name = name
        self.is_end = False
        self.parent = []
        
    def __str__(self):
        pretty_epsilon = ""
        for s in self.epsilon:
            pretty_epsilon += s.name + ","
        pretty_epsilon = "[" + pretty_epsilon[:-1] + "]"
        pretty_transitions = ""
        for c in self.transitions.keys():
            pretty_transitions += str(c) + " to ["
            
            for s in self.transitions[c]:
                pretty_transitions += s.name + ", "
            pretty_transitions = pretty_transitions[:-2] + "]" 
        pretty_parent = ""
        for p in self.parent:
            pretty_parent += p.name + ","
        pretty_parent = "[" + pretty_parent[:-1] + "]"
                    
        return "Name: " + self.name + "; Transitions: {" + pretty_transitions + "}; Epsilon transitions: " + pretty_epsilon + "; Parent: " + pretty_parent
    
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
        end.is_end = True
        self.states = set()
    
    def __str__(self):
        pretty_nfa = "NFA Start State: " + self.start.name + "; End State: " + self.end.name + "\n"
        for s in self.states:
            pretty_nfa += str(s) + "\n"
        return pretty_nfa

class Handler:
    def __init__(self):
        self.handlers = {'CHAR':self.handle_char, 'CONCAT':self.handle_concat,
                         'ALT':self.handle_alt, 'STAR':self.handle_rep,
                         'PLUS':self.handle_rep, 'QMARK':self.handle_qmark}
        self.state_count = 0

    def create_state(self):
        self.state_count += 1
        return State('s' + str(self.state_count))
    
    def handle_char(self, t, nfa_stack):
        s0 = self.create_state()
        s1 = self.create_state()
        s0.transitions[("epsilon",t.value)] = [s1]
        s1.parent.append(s0) # add parent
        nfa = NFA(s0, s1)
        nfa.states.add(s0) # add to states
        nfa.states.add(s1) # add to states
        nfa_stack.append(nfa)
    
    def handle_concat(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        n1.end.is_end = False
        n1.end.epsilon.append(n2.start)
        n2.start.parent.append(n1.end) # add parent
        nfa = NFA(n1.start, n2.end)
        nfa.states = nfa.states.union(n1.states, n2.states) # add to states
        nfa_stack.append(nfa)
    
    def handle_alt(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s0.epsilon = [n1.start, n2.start]
        n1.start.parent.append(s0) # add parent
        n2.start.parent.append(s0) # add parent
        s3 = self.create_state()
        n1.end.epsilon.append(s3)
        n2.end.epsilon.append(s3)
        s3.parent.append(n1.end) # add parent
        s3.parent.append(n2.end) # add parent
        n1.end.is_end = False
        n2.end.is_end = False
        nfa = NFA(s0, s3)
        nfa.states.add(s0) # add states
        nfa.states.add(s3) # add states
        nfa.states = nfa.states.union(n1.states, n2.states) # add states
        nfa_stack.append(nfa)
    
    def handle_rep(self, t, nfa_stack):
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s1 = self.create_state()
        s0.epsilon = [n1.start]
        n1.start.parent.append(s0) # add parent
        if t.name == 'STAR':
            s0.epsilon.append(s1)
            s1.parent.append(s0) # add parent
        n1.end.epsilon.extend([s1, n1.start])
        n1.start.parent.append(n1.end) # add parent
        s1.parent.append(n1.end) # add parent
        n1.end.is_end = False
        nfa = NFA(s0, s1)
        nfa.states.add(s0) # add states
        nfa.states.add(s1) # add states
        nfa.states = nfa.states.union(n1.states) # add states
        nfa_stack.append(nfa)

    def handle_qmark(self, t, nfa_stack):
        n1 = nfa_stack.pop()
        n1.start.epsilon.append(n1.end)
        n1.end.parent.append(n1.start) # add parent
        nfa_stack.append(n1)
