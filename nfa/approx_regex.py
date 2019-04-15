from approx_parse import *
import math

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
                        # does char already exist in transitions?
                        #if char in fromState.transitions.keys():
                          #  fromState.transitions[char].append(toState)
                        #else: fromState.transitions[char] = [toState]
        
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
    
    def match(self, k, s):
        app = self.approximateNFA(s)
        dictionary = self.nfaTOdictionary(app)
        # perform a BFS on the NFA
        parent, lengthOfPath = breadth_first_search(dictionary, app.start)
        # create path
        path = []
        endState = app.end
        startState = app.start
        path.append(endState)
        state = endState
        while state != startState:
            path = [parent[state]] + path
            state = parent[state]
            
        
        maxScore = self.cost(path)

        # length of path from start state to end state
        endStatePathLength = lengthOfPath[endState]
        print("Path Length:",endStatePathLength)
        
        # if length of path from start state to end state is <= to k, then return true
        if (endStatePathLength - maxScore <= k):
            return True
        return False

    def cost(self, path):
        p = len(path)
        c = [-math.inf, 0]
        v0 = State("boundary")
        path = [v0] + path
        for k in range(1, p+1):
            j = 0

            vk = path[k]
            if len(vk.transitions) != 0:
                vk_name = list(vk.transitions.keys())[0][1]
            else:
                vk_name = "epsilon"
            for i in range(1, k-1):
                vi = path[i]
                if len(vi.transitions) != 0:
                    vi_name = list(vi.transitions.keys())[0][1]
                else:
                    vi_name = "epsilon"
                
                if vi_name == vk_name:
                    j = i

            costs = []
            for i in range(j+1, k-1+1):
                vi = path[i]
                for transition in vi.transitions:
                    if vi[transition] == vk:
                        cost = 0
                        if transition[0] == transition[1]: cost = 1
                        costs.append(c[i] + cost)
                    if vk in vi.epsilon: costs.append(c[i])

            print(c[j], costs)
            c.append(max(c[j], max(costs)))

        return c[-1]

            

    def dijkstra(self, graph, root):
        
        numberOfNodes = len(graph.keys())
        distances = {}
        for state in graph:
            distances[state] = math.inf
        distances[root] = 0
        visited = []
        
        while len(visited) != numberOfNodes:
            # Pick the unvisited node with the smallest value in distances
            current = self.nextNode(distances, visited)
            # Add the node to visited
            visited.append(current)
            # Find the character transitions of the node
            char, epsilon = graph[current]
            # Find the shortest distance
            for neighbour in char:
                if  (neighbour not in visited) \
                    and (distances[neighbour] > (distances[current]+1)):
                    distances[neighbour] = (distances[current]+1)
            for neighbour in epsilon:
                if  (neighbour not in visited) \
                    and (distances[neighbour] > distances[current]):
                    distances[neighbour] = distances[current]
                    
        print("distances",distances)
        return distances

    def nextNode(self, distances, visited):
        minimum = math.inf
        for state in distances:
            if distances[state] < minimum and \
               (state not in visited):
                minimum = distances[state]
                node = state
        return node
            
    def nfaTOdictionary(self, nfa):
        dictionary = {}

        for state in self.states:
            #for each state make an empty dictionary where states are the keys as they are unique
            dictionary[state] = []
            #for all neighbouring states
            transit = list(state.transitions.values())

            # also add epsilon transitions
            dictionary[state] =  transit + state.epsilon

        return dictionary
        
def breadth_first_search(graph, root):
    distances = {}; path = []
    parent = {}
    marked = []
    queue = set()
    for state in graph:
        distances[state] = math.inf
        parent[state] = root
    distances[root] = 0
    
    queue.add(root)
    while len(queue) != 0:
        current = queue.pop()
        marked.append(current)
        neighbours = graph[current]
        for neighbour in neighbours:
            if distances[neighbour] > (distances[current]+1):
                distances[neighbour] = (distances[current]+1)
                parent[neighbour] = current
            if neighbour not in marked:
                queue.add(neighbour)
    return parent, distances


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

print(compile("(a|b)a*"))
    
app = ApproximateNFA("(a|b)a*")
nfa = app.approximateNFA("ba")
graph = app.nfaTOdictionary(nfa)
parent, d = breadth_first_search(graph, nfa.start)
app.match(0, "ba")
#for i in parent:
  #  print(parent[i].name, i.name, i.is_end)
