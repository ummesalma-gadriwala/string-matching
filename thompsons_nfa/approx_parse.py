from parse import *

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
        app = self.approximateNFA(s)
        dictionary = self.nfaTOdictionary(app)
        # perform a BFS on the NFA
        lengthOfPath = breadth_first_search(dictionary, app.start)
        endState = app.end
        print(endState)
        # length of path from start state to end state
        endStatePathLength = lengthOfPath[endState]
        print("Path Length:",endStatePathLength)
        
        # if length of path from start state to end state is <= to k, then return true
        if (endStatePathLength <= k):
            return True
        return False
        
    def nfaTOdictionary(self, nfa):
        dictionary = {}

        for state in self.states:
            #for each state make an empty dictionary where states are the keys as they are unique
            dictionary[state] = []

            #for all neighbouring states
            for neighbour in state.transitions:
                neighbour_state = state.transitions[neighbour]
                dictionary[state] = dictionary[state] + neighbour_state

            # also add epsilon transitions
            dictionary[state] = dictionary[state] + state.epsilon
        
        return dictionary
        
def breadth_first_search(graph, root):
    import math
    distances = {}
    marked = []
    queue = set()
    for state in graph:
        distances[state] = math.inf
    distances[root] = 0
    queue.add(root)
    while len(queue) != 0:
        current = queue.pop()
        marked.append(current)
        neighbours = graph[current]
        for neighbour in neighbours:
            if distances[neighbour] > (distances[current]+1):
                distances[neighbour] = (distances[current]+1)
            if neighbour not in marked:
                queue.add(neighbour)
    return distances
