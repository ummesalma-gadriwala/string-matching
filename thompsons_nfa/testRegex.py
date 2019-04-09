## @file testRegex.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief A testing file to test EXACT matching in:
#         regex.py
#  @date 4/09/2019

import unittest
from regex import *

## @brief A class to test EXACT matching as part of the regular expression matching project
class testRegex(unittest.TestCase):

    ''' Testing regex with two letters in alphabet: a and b'''
    
    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details This is the most straightforward case where the string matches the regexp exactly.
    def test_alphabet1(self):
        r = "ab"
        s = "ab"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))
    
    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details This is a straightforward case where the string contains a different alphabet.
    def test_alphabet2(self):
        r = "ab"
        s = "c"
        nfa = compile(r)
        self.assertFalse(nfa.match(s))

    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details This is the most straightforward case where the string matches the regexp exactly.
    def test_alphabet3(self):
        r = "ab"
        s = "ab"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))


        

if __name__ == '__main__':
    unittest.main()
