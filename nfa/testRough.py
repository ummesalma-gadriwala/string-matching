## @file testRough.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief Roughly test exact and approx matching 
#  @date 4/11/2019
from regex import *
from approx_regex import *

def main():
    nfa = compile("ab")
    e = nfa.match("ab")
    print("e", e)

    app = ApproximateNFA("(G|A|T|C)*GC(G|A|T|C)GC(G|A|T|C)*")
    print("a", app.match(0, "AAAAAGCAGCAAAAA"))

    app = ApproximateNFA("AC(G|A|T|C){4}GTA(A|G)C")
    print("a", app.match(0, "ACATAGGTAGC"))
    nfa = compile("AC(G|A|T|C){4}GTA(A|G)C")
    e = nfa.match("ACATAGGTAGC")
    print("e", e)

    nfa = compile("^[a-zA-Z]{4}[\d]{4}$")
    print("test", nfa.match("aaaa1111"))
          
    app = ApproximateNFA("C(G|A|T|C){4,}G")
    print("a", app.match(0, "CAAAAAGCAGCAAAAAG"))

if __name__ == '__main__':
    main()
