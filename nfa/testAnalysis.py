## @file testAnalysis.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief Run analytical code to test efficiency of
#         exact and approximate matching algorithm implementations through
#         regex.py
#  @date 4/11/2019
from regex import *
import time

def main():
    # Initialize analytical variables
    numIterations = 100 # number of times to run algorithm on test case
    numLength = 100     # max length of string to create test cases out of
    
    # Create a test case with an alternating sequence of ab
    regexp = "(ab)*"    # the regular expression
    string = "ab"       # the string to perform the match against
    # Compile the regexp for exact matching (i.e. create an NFA)
    nfa = compile(regexp)
    # Create a list to store the resulting time differences for strings of varying length
    exactTimes = []
    approxTimes = []

    # Run the algorithms on increasing lengths of the string
    for i in range(numLength):
        # Extend the string
        string = string + "ab"*4 #multiplication of 4 was arbitrarily chosen

        # Create a list to store the times for this string in
        exactTimesAvg = []
        approxTimesAvg = []
        # Run the algorithms on a single test case multiple times for better computation of time difference
        for i in range(numIterations):
            # Run the exact matching algorithm
            start = time.time()
            nfa.match(string)
            end = time.time()
            exactTimesAvg = exactTimesAvg + [end-start]

            # TODO: Run the approximate matching algorithm

        # Compute average time to output
        exactTimes = exactTimes + [sum(exactTimesAvg)/numIterations]
        # TODO: approxTimes = approxTimes + [sum(approxTimeAvg)/numIterations]

    print(exactTimes)


if __name__ == '__main__':
    main()
