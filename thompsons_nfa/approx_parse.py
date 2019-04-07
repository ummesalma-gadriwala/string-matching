from parse import *

class ApproximateState(State):
    def __init__(self, name, counter, kind, pre):
        State. __init__(self, name)
        self.counter = counter
        self.pre = pre
        self.kind = kind # L or epsilon


class ApproximateNFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.start = {nfa.start}
        self.end = {nfa.end}

    def approximateNFA(self, s):
        n = len(s) 
        approxNFA = [self.nfa] * n
        for i in range(n):
            goStart = approxNFA[i]
            toStart = approxNFA[i+1]
            
            # add character transition
            char = s[i]
            if char in go.start.transitions.keys():
                goStart.transitions[char] = [goStart.transitions[char], toStart]
            else:
                goStart.transitions[char] = toStart

            # add epsilon transition
            
            
            

    def match(self, k, s):
        
        for i in s:
            pass
             
