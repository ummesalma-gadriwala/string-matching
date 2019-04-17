## Exact vs. Approximate String Matching

**Goal:** Is it viable to replace existing exact regular expression with approximate matching for search?

**Our conclusion:** No, approximate matching takes twice as much time as exact matching. It is not a viable trade-off.

**Approximate String:**
A string s satifies a regular expression r with upto k errors. An error is defined as:
*  Insertion, for r = ab* and s = abc;
*  Deletion, for r = ab* and s = b;
*  and Substitution, for r = ab* and s = cb.

To run various test cases of your choice, open nfa/testRough.py, modify the regular expression and strings, and then compile and run the file. 


In general, to run the exact matching algorithm:
regexp = "regular_expression_of_your_choice"
string = "string_of_your_choice"
nfa.compile(regexp)
print(nfa.match(string))


In general, to run the approximate matching algorithm:
k = 0 # the number of errors you want to allow for
app = ApproximateNFA(regexp)
print(app.match(k, string))


# File Organization
The code for the exact matching algorithm is contained in:
regex.py
parse.py

The code for the approximate matching algorithm is contained in:
approx_regex.py
approx_parse.py

PyUnit test cases can be found in:
testRegex.py to test the exact matching algorithm
testRegexApprox.py to test the approximate matching algorithm

The code for creating bar and line graphs for analysis can be found in:
testAnalysis.py
testAnalysis_bioinformatics.py
