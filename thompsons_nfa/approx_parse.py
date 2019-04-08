from parse import *
        
class ApproximateNFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.start = nfa.start
        self.end = nfa.end
        self.states = list(nfa.states)
        
    def approximateNFA(self, s):
        n = len(s)
        
        approxNFA = []
        nfaStates = []
        for i in range(n+1):
            approxNFA.append(self.nfa.copy(i))
            nfaStates.append([])
            for state in self.states:
                nfaStates[i].append(state.copy(i))

        # TODO: make sure all nfas have states in same order
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
            for j in range(1,len(state)):
                toState = state[j]
                if toState.epsilon != []:
                    fromStates = toState.parent
                    char = s[i-1] #??
                    for fromState in fromStates:
                        # is it a char transition?
                        fromState.transitions[char] = toState

        # and states = all states in all NFAs in list
        flatten = lambda l: [item for sublist in l for item in sublist]
        nfaStates = flatten(nfaStates)
        
        # add epsilon start
        for i in range(n+1):
            nfa = approxNFA[i]
            state = State("epsilon"+str(i))
            state.epsilon = [nfa.start]
            nfa.start = state
            nfaStates.append(state)

        # add character transition
        for i in range(n):
            fromStart = approxNFA[i].start
            toStart = approxNFA[i+1].start
            char = s[i]
            fromStart.transitions[char] = toStart

        self.states = nfaStates
        
        # approxNFA[0] is the complete NFA graph,
        # with end = end of last NFA in list
        approxNFA[0].end = approxNFA[-1].end
        # and states = all states in all NFAs in list
        approxNFA[0].states = set(nfaStates)

        return approxNFA[0]

    def pretty_states(self):
        string = "\n"
        for s in self.states:
            string += str(s) + "\n"

        return string
    
    def match(self, k, s):
        approxNFA = approximateNFA(s)
        # perform a BFS on the NFA
        # if length of path from start state to end state is <= to k, then return true
        # else return false
             
