from parse import *
from collections import deque

class ApproximateNFA:
    def __init__(self, regex):
        self.regex = regex
        
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
                    # is it an epsilon transition?
                    fromState.epsilon.append(toState)
                    print("adding deletion edge")
                    
        # add substitution edges
        for i in range(1,n+1):
            currentStates = nfaStates[i]
            previousStates = nfaStates[i-1]
            for j in range(len(currentStates)):
                toState = currentStates[j]
                if len(toState.transitions) != 0: 
                    fromStates = previousStates[j].parent
                    char = s[i-1] #??
                    for fromState in fromStates:
                        # is it a char transition?
                        # does char already exist in transitions?
                        if char in fromState.transitions.keys():
                            fromState.transitions[char].append(toState)
                        else: fromState.transitions[char] = [toState]
                        print("adding substitution edge", char, fromState.name, toState.name)

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
            fromStart.transitions[char] = [toStart]

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
        
    def nfaTOdictionary(self, nfa):
        dictionary = {}

        for state in self.states:
            #print("Parent:"+state.name)
            #for each state make an empty dictionary where states are the keys as they are unique
            dictionary[state] = []

            #for all neighbouring states
            for neighbour in state.transitions:
                neighbour_state = state.transitions[neighbour]
                for ns in range(0,len(neighbour_state)):
                    #add it to the value for the parent as its key
                    dictionary[state].append(neighbour_state[ns])
                    #print("children:",neighbour_state[ns].name)

                # also add epsilon transitions
                #print("EpsilonList:",state.epsilon)
                dictionary[state].append(state.epsilon)

        #print(dictionary)
        return dictionary
        #for key in dictionary:
        #    print("Parent:"+key)
         #   print("child:"+dictionary[key])
		 
		 
def breadth_first_search(graph, root):
    distances = {}
    distances[root] = 0
    q = deque([root])
    while q:
        # The oldest seen (but not yet visited) node will be the left most one.
        current = q.popleft() #state
        #print("current:",current)
        for neighbor in graph[current]:
            if (isinstance(neighbor, list)):
                #neighbour is a list of states
                for state in range(0, len(neighbor)):
                    if neighbor[state] not in distances:
                        distances[neighbor[state]] = distances[current] + 1
                        # When we see a new node, we add it to the right side of the queue.
                        q.append(neighbor[state])
            
             #   print("neighbour:",neighbor[state]) 
            else:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                # When we see a new node, we add it to the right side of the queue.
                    q.append(neighbor)

    for state in distances:
        print("state: ("+ state.name + "), Distance:" + str(distances[state]))
    return distances
