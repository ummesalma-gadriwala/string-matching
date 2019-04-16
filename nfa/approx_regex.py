## @file approx_regex.py
#  @brief Creates an NFA out of regular expression
#  @date 4/15/2019

from approx_parse import *
import math

class ApproximateNFA:
    ##@brief Initialize NFA for approximate algorithm with the regular expression
    def __init__(self, regex):
        self.regex = regex

    ##@brief Creates an NFA out of regular expression
    def makeNFA(self):
        lexer = Lexer(self.regex)
        parser = Parser(lexer)
        tokens = parser.parse()
        handler = Handler()
        nfa_stack = []
    
        for t in tokens:
            handler.handlers[t.name](t, nfa_stack)
    
        assert len(nfa_stack) == 1
        return nfa_stack.pop() 

    ##@brief Creates an approximate NFA out of given string
    # @details Creates n+1 (where n = len(string)) instances of thompsons NFA,
    #          connects the instances by adding insertion, deletion and substitution edges
    def approximateNFA(self, s):
        n = len(s)
        
        approxNFA = []
        nfaStates = []
        for i in range(n+1):
            new = self.makeNFA()
            approxNFA.append(new)
            # Sort in some order to ensure newStates list is in the same order for all nfas
            newStates = sorted(new.states, key=lambda state: state.name) 
            nfaStates.append(newStates)
        
        # add deletion edges
        for i in range(1,n+1):
            state = nfaStates[i]
            for t in range(len(state)):
                toState = state[t]
                if (not toState.is_end) and toState.epsilon == []:
                    fromState = nfaStates[i-1][t]
                    char = s[i-1] 
                    fromState.transitions[(char, "epsilon")] = toState
                    
                    
        # add substitution edges
        for i in range(1,n+1):
            currentStates = nfaStates[i]
            previousStates = nfaStates[i-1]
            for j in range(len(currentStates)):
                toState = currentStates[j]
                if len(toState.transitions) != 0: 
                    fromStates = previousStates[j].parent
                    char = s[i-1]
                    for fromState in fromStates:
                        sub = list(toState.transitions.keys())
                        sub = sub[0][1]
                        fromState.transitions[(char, sub)] = toState
                        
        
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
            #fromState.epsilon.append(toStart)
            fromStart.transitions[("epsilon", "epsilon")] = toStart

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

    ##@brief Add states
    # @details Add state and recursively add epsilon transitions   
    def addstate(self, state, state_set): 
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)

    ##@brief If len(s) - count <= k return true
    # @details Count is the number of correct alignments when traversing the NFA
    def match(self, k, s):
        app = self.approximateNFA(s)
        current_states = set()
        self.addstate(app.start, current_states)
        count = 0
        
        for x in current_states:
            for t in x.transitions:
                if t[0] == t[1] and t[0] == "epsilon": count += 1
        
        for c in s:
            next_states = set()
            for state in current_states:
                for i in state.transitions.keys():

                        trans_state = state.transitions[i]
                        self.addstate(trans_state, next_states)

            current_states = next_states
            for x in current_states:
                for t in x.transitions:
                    if t[0] == t[1] and t[0] == "epsilon": count += 1

        
        for x in current_states:
            for t in x.transitions:
                if t[0] == t[1] and t[0] == "epsilon": count += 1
        for x in current_states:
            if x.is_end:
                if len(s) - count <= k:
                    return True
        return False
    
    
