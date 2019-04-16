## @file testAnalysis.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief Run analytical code to test efficiency of
#         exact and approximate matching algorithm implementations through
#         regex.py and approx_regex.py
#  @date 4/11/2019
from regex import *
from approx_regex import *
import time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Initialize analytical variables
    numIterations = 100 # number of times to run algorithm on test case
    
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
    #regexp = ["(ab)*", "CGA(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)TGC"]    # the regular expression
    #strings = ["ab", "CGAAAAAAATGC"]       # the string to perform the match against


    #BcGI restriction enzyme
    r1 = "CGA(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)TGC"
    #BaEI restriction enzyme
    r2 = "AC(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)GTA(A|G)C"
    #AbaSI endonuclease
    r3 = "(A|G|C|T)*C(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)(A|G|C|T)G(A|G|C|T)*"
    
    s1 = "CGAAGCTATTGC"
    s2 = "ACAAAAGTAGC"
    s3 = "AAACAAAAAGTTTT"
    s33 = "TCGCTCGCTCGCTCGCTAAACAAAAAGTTTTTCGTCGTCGCTCG"

    regexp = [r1,r2,r3,r3]
    strings = [s1,s2,s3,s33]

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


    for i in range(len(exactTimes)):
        print("e", exactTimes[i])

    
    for i in range(len(exactTimes)):
        print("a", approxTimes[i])

        
    # Plot final results as a bar graph
    objects = ("[r1,s1]","[r2,s2]","[r3,s3]","[r3,s33]")
##    y_pos = np.arange(len(objects))
##    performance = exactTimes
##     
##    plt.bar(y_pos, performance, align='center', alpha=0.5)
##    plt.xticks(y_pos, objects)
##    plt.ylabel('Time (epoch)')
##    plt.title('Test Cases')
##     
##    plt.show()


if __name__ == '__main__':
    main()
