## @file testAnalysis.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief Run analytical code to test efficiency of
#         exact and approximate matching algorithm implementations through
#         regex.py
#  @date 4/11/2019
from regex import *
import time
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

def main():
    # Initialize analytical variables
    numIterations = 5 # number of times to run algorithm on test case
    
    # Create a test case with an alternating sequence of ab

    #BcGI
        #"CGA(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)TGC"
    #AbaSI is a DNA modification-dependent endonuclease and it is an EpiMark® validated product. AbaSI recognizes 5-glucosylhydroxymethylcytosine (5ghmC) in double stranded DNA. It also recognizes 5-hydroxymethylcytocine (5hmC) but at a lower efficiency. It does not recognize DNA with 5-methylcytosin or un-modified cytosine. AbaSI selectively cleaves DNA that contains the modified bases, 5ghmC or 5hmC on one or both strands and introduces a double-stranded DNA break on the 3´ side away from the modified cytosine producing a 2-base or 3-base 3´-overhang. Sites with two 5ghmC on opposite strands are cleaved most efficiently; sites with one 5ghmC and another C or 5mC are cleaved less efficiently.
        #CNNNNNNNNNNN/NNNNNNNNNG
    #BaEI
        #ACNNNNGTAYC
        #ACNNNNGTA(A|G)C

    #"CGA(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)TGC"
    #CNNNNNNNNNNN/NNNNNNNNNG
    #ACNNNNGTA(A|G)C
    
             #[random test case, BcgI restriction site (cleaves or methylates)]
    # reference info: https://www.neb.com/products/restriction-endonucleases/restriction-endonucleases/types-of-restriction-endonucleases
    # reference: https://www.neb.com/tools-and-resources/selection-charts/alphabetized-list-of-recognition-specificities
    regexp = ["(ab)*", "CGA(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)TGC"]    # the regular expression
    strings = ["ab", "CGAAAAAAATGC"]       # the string to perform the match against
    # Create a list to store the resulting time differences for strings of varying length
    exactTimes = []
    approxTimes = []

    for i in range(len(regexp)):
        # Compile the regexp for exact matching (i.e. create an NFA)
        exact_nfa = compile(regexp[i])
        string = strings[i]
        
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
##    plt.plot([2 + i*4 for i in range(1,numIterations+1)], exactTimes, color ='g', label = 'exact')
##    plt.plot([2 + i*4 for i in range(1,numIterations+1)], approxTimes, color ='orange', label = 'approximate')
##    plt.xlabel('Legnth of String')
##    plt.ylabel('Time to Run Algorithm')
##    plt.legend()
##    plt.title('String Matching Efficiences for the Regular Expression "(ab)*"')
##    plt.show()



if __name__ == '__main__':
    main()
