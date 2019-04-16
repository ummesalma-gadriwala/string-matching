## @file testAnalysis.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief Run analytical code to test efficiency of
#         exact and approximate matching algorithm implementations through
#         regex.py
#  @date 4/11/2019
from regex import *
from approx_regex import *
import time
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

def main():
    # Initialize analytical variables
    numIterations = 5 # number of times to run algorithm on test case
    numLength = 5     # max length of string to create test cases out of
    
    # Create a test case with an alternating sequence of ab
    regexp = "(ab)*"    # the regular expression
    string = "ab"       # the string to perform the match against
    # Compile the regexp for exact matching (i.e. create an NFA)
    exact_nfa = compile(regexp)
    # Create a list to store the resulting time differences for strings of varying length
    exactTimes = []
    approxTimes = []

    # Run the algorithms on increasing lengths of the string
    for i in range(numLength):
        # Extend the string
        string = string + "ab"*4 #multiplication of 4 was arbitrarily chosen
        # Run the EXACT matching algorithm on a single test case multiple times for better computation of time difference
        start = time.time()
        for i in range(numIterations):
            # Run the exact matching algorithm
            exact_nfa.match(string)    
        end = time.time()
        # Compute average time to output
        exactTimes = exactTimes + [(end-start)/numIterations]

        # Run the APPROX matching algorithm on a single test case multiple times for better computation of time difference
        # Create the approx. NFA specific to this string
        approx_nfa = ApproximateNFA(regexp)        
        start = time.time()
        for i in range(numIterations):
            # Run the approx matching algorithm
            approx_nfa.match(0,string)    
        end = time.time()
        # Compute average time to output
        approxTimes = approxTimes + [(end-start)/numIterations]


    # Plot final results as a line graph
    plt.plot([2 + i*4 for i in range(1,numIterations+1)], exactTimes, color ='g', label = 'exact')
    plt.plot([2 + i*4 for i in range(1,numIterations+1)], approxTimes, color ='orange', label = 'approximate')
    plt.xlabel('Number of Characters String')
    plt.ylabel('Time to Run Algorithm (epoch)')
    plt.legend()
    plt.title('String Matching Efficiences for the Regular Expression "(ab)*"')
    plt.show()



if __name__ == '__main__':
    main()
