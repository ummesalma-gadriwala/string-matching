from parse import *

class ApproximateState(State):
    def __init__(self, name, counter, kind, pre):
        State. __init__(self, name)
        self.counter = counter
        
class ApproximateNFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.start = {nfa.start}
        self.end = {nfa.end}
        self.states = nfa.getStates()

    def approximateNFA(self, s):
        n = len(s) 
        approxNFA = [self.nfa] * (n+1)
        nfaStates = [self.states] * (n+1)
        
        # add deletion edges
        for i in range(1,n+1):
            state = nfaStates[i]
            for t in range(len(state)):
                toState = state[t]
                if toState.epsilon != []:
                    fromState = nfaStates[i-1][t]
                    # is it an epsilon transition?
                    toState.epsilon.append(fromState)
                    
        
        # add substitution edges
        for i in range(1,n+1):
            state = nfaStates[i]
            for t in range(1,len(state)):
                toState = state[t]
                if toState.epsilon != []:
                    fromState = nfaStates[i-1][t-1]
                    # is it an epsilon transition?
                    # toState.epsilon.append(fromState)
                    # or a char transition?
                    char = s[i]
                    fromState.transitions[char] = toState
                    
        # add epsilon start
        for i in range(n+1):
            nfa = approxNFA[i]
            state = State("epsilon")
            state.epsilon = [nfa.start]
            nfa.start = state

        # add character transition
        for i in range(n):
            fromStart = approxNFA[i].start
            toStart = approxNFA[i+1].start
            char = s[i]
            fromStart.transitions[char] = toStart

        # approxNFA[0] is the complete NFA graph,
        # with end = end of last NFA in list
        approxNFA[0].end = approxNFA[-1].end
        return approxNFA[0]
           
    def match(self, k, s):
        approxNFA = approximateNFA(s)
        # perform a BFS on the NFA
        # if length of path from start state to end state is <= to k, then return true
        # else return fales
             
