## @file testRegex.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief A testing file to test EXACT matching in:
#         regex.py
#  @date 4/09/2019

import unittest
from regex import *

## @brief A class to test EXACT matching as part of the regular expression matching project
class testRegex(unittest.TestCase):

    ''' Testing regex with spaces'''
    
    ## @brief Test to show that spaces count as characters
    #  @details The string will have a space, whereas the regexp will not. A match should not be found.
    def test_space1(self):
        r = "ab"
        s = "a b"
        nfa = compile(r)
        self.assertFalse(nfa.match(s))

    ## @brief Test to show that spaces count as characters
    #  @details The string will consit of a space only, whereas the regexp will not contain any spaces. A match should not be found.
    def test_space2(self):
        r = "ab"
        s = " "
        nfa = compile(r)
        self.assertFalse(nfa.match(s))

    ## @brief Test to show that spaces count as characters
    #  @details The string will consit of a space only, whereas the regexp will contain one character with a star.
    def test_space3(self):
        r = "a*"
        s = " "
        nfa = compile(r)
        self.assertFalse(nfa.match(s))

    ''' -------------------------------------------------- '''
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
    #  @details The regexp and string consist of the same alphabet but in a different ordering
    def test_alphabet3(self):
        r = "ab"
        s = "ba"
        nfa = compile(r)
        self.assertFalse(nfa.match(s))

    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details The regexp and string consist of the same alphabet but of different legnths
    #           In this case, len(regexp) > len(s)
    def test_alphabet4(self):
        r = "ab"
        s = "a"
        nfa = compile(r)
        self.assertFalse(nfa.match(s))
        
    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details The regexp and string consist of the same alphabet but of different legnths
    #           In this case, len(regexp) < len(s)
    def test_alphabet5(self):
        r = "ab"
        s = "aba"
        nfa = compile(r)
        self.assertFalse(nfa.match(s))
        

    ''' -------------------------------------------------- '''
    ''' Testing regex with the * symbol'''
    
    ## @brief Test a regexp with the * symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a * only and the string matches the first half only
    def test_star1(self):
        r = "a*b"
        s = "a"
        nfa = compile(r)
        self.assertFalse(nfa.match(s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a * only and the string matches the second half only
    def test_star2(self):
        r = "a*b"
        s = "b"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a * only and the string matches the entire regexp
    def test_star3(self):
        r = "a*b"
        s = "aaaaaaab"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))


    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "many" case
    #  @details Both characters contain a * symbol and the string matches the first half only
    def test_star4(self):
        r = "a*b*"
        s = "aaaaaaa"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "many" case
    #  @details Both characters contain a * symbol and the string matches the second half only
    def test_star5(self):
        r = "a*b*"
        s = "bbbbbb"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "one of" case
    #  @details Both characters contain a * symbol and the string matches the first half only
    def test_star6(self):
        r = "a*b*"
        s = "a"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "one of" case
    #  @details Both characters contain a * symbol and the string matches the second half only
    def test_star7(self):
        r = "a*b*"
        s = "b"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))
    
    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "no-value" case
    #  @details Both characters contain a * symbol and the string is empty
    def test_star8(self):
        r = "a*b*"
        s = ""
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    
    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet: "many" case
    #  @details Alternating sequence of characters each with a * symbol, and the string matches exactly
    def test_star9(self):
        r = "a*b*a*b*"
        s = "aabbaaabbb"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet: "one-of" and "none-of" case
    #  @details Alternating sequence of characters each with a * symbol, and the string matches partly
    def test_star10(self):
        r = "a*b*a*b*"
        s = "a"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet
    #  @details Some characters have the * symbol and some do not. The string does not match.
    def test_star11(self):
        r = "ba*b"
        s = "aaaaa"
        nfa = compile(r)
        self.assertFalse(nfa.match(s))

    
    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet
    #  @details The star symbol surrounds a sequence of characters.
    def test_star12(self):
        r = "(ba*b)*"
        s = "baaaaabbabbb"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ''' -------------------------------------------------- '''
    ''' Testing regex with the | symbol'''
    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A simple choice between two different characters
    def test_or1(self):
        r = "a|b"
        s = "a"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A simple choice between two different characters
    def test_or2(self):
        r = "a|b"
        s = "b"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A choice between two of the same characters
    def test_or3(self):
        r = "a|a"
        s = "a"
        nfa = compile(r)
        self.assertTrue(nfa.match(s))

        
    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A test with an empty string
    def test_or4(self):
        r = "a|b"
        s = ""
        nfa = compile(r)
        self.assertFalse(nfa.match(s))
    
    

if __name__ == '__main__':
    unittest.main()
