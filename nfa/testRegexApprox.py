## @file testRegex.py
#  @author Rumsha Siddiqui, siddiqur
#  @brief A testing file to test APPROXIMATE matching in:
#         regex.py
#  @date 4/09/2019

import unittest
from regex import *

## @brief A class to test APPROXIMATE matching as part of the regular expression matching project
class testRegex(unittest.TestCase):

    ''' Testing regex with spaces'''
    
    ## @brief Test to show that spaces count as characters
    #  @details The string will have a space, whereas the regexp will not. A match should not be found.
    def test_space1(self):
        r = "ab"
        s = "a b"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test to show that spaces count as characters
    #  @details The string will consit of a space only, whereas the regexp will not contain any spaces. A match should not be found.
    def test_space2(self):
        r = "ab"
        s = " "
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test to show that spaces count as characters
    #  @details The string will consit of a space only, whereas the regexp will contain one character with a star.
    def test_space3(self):
        r = "a*"
        s = " "
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ''' -------------------------------------------------- '''
    ''' Testing regex with two letters in alphabet: a and b'''
    
    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details This is the most straightforward case where the string matches the regexp exactly.
    def test_alphabet1(self):
        r = "ab"
        s = "ab"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))
    
    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details This is a straightforward case where the string contains a different alphabet.
    def test_alphabet2(self):
        r = "ab"
        s = "c"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details The regexp and string consist of the same alphabet but in a different ordering
    def test_alphabet3(self):
        r = "ab"
        s = "ba"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details The regexp and string consist of the same alphabet but of different legnths
    #           In this case, len(regexp) > len(s)
    def test_alphabet4(self):
        r = "ab"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))
        
    ## @brief Test a basic regexp with no symbols (only the alphabet)
    #  @details The regexp and string consist of the same alphabet but of different legnths
    #           In this case, len(regexp) < len(s)
    def test_alphabet5(self):
        r = "ab"
        s = "aba"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))
        

    ''' -------------------------------------------------- '''
    ''' Testing regex with the * symbol'''
    
    ## @brief Test a regexp with the * symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a * only and the string matches the first half only
    def test_star1(self):
        r = "a*b"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a * only and the string matches the second half only
    def test_star2(self):
        r = "a*b"
        s = "b"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a * only and the string matches the entire regexp
    def test_star3(self):
        r = "a*b"
        s = "aaaaaaab"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))


    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "many" case
    #  @details Both characters contain a * symbol and the string matches the first half only
    def test_star4(self):
        r = "a*b*"
        s = "aaaaaaa"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "many" case
    #  @details Both characters contain a * symbol and the string matches the second half only
    def test_star5(self):
        r = "a*b*"
        s = "bbbbbb"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "one of" case
    #  @details Both characters contain a * symbol and the string matches the first half only
    def test_star6(self):
        r = "a*b*"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "one of" case
    #  @details Both characters contain a * symbol and the string matches the second half only
    def test_star7(self):
        r = "a*b*"
        s = "b"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))
    
    ## @brief Test a regexp with the * symbol and a 2-letter alphabet: "no-value" case
    #  @details Both characters contain a * symbol and the string is empty
    def test_star8(self):
        r = "a*b*"
        s = ""
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    
    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet: "many" case
    #  @details Alternating sequence of characters each with a * symbol, and the string matches exactly
    def test_star9(self):
        r = "a*b*a*b*"
        s = "aabbaaabbb"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet: "one-of" and "none-of" case
    #  @details Alternating sequence of characters each with a * symbol, and the string matches partly
    def test_star10(self):
        r = "a*b*a*b*"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet
    #  @details Some characters have the * symbol and some do not. The string does not match.
    def test_star11(self):
        r = "ba*b"
        s = "aaaaa"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    
    ## @brief Test a more complex regexp with the * symbol and a 2-letter alphabet
    #  @details The star symbol surrounds a sequence of characters.
    def test_star12(self):
        r = "(ba*b)*"
        s = "baaaaabbabbb"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ''' -------------------------------------------------- '''
    ''' Testing regex with the | symbol'''
    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A simple choice between two different characters
    def test_or1(self):
        r = "a|b"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A simple choice between two different characters
    def test_or2(self):
        r = "a|b"
        s = "b"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A choice between two of the same characters
    def test_or3(self):
        r = "a|a"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

        
    ## @brief Test a regexp with the | symbol and a 2-letter alphabet
    #  @details A test with an empty string
    def test_or4(self):
        r = "a|b"
        s = ""
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

        
    ## @brief Test a more complex regexp with the | symbol and a 2-letter alphabet
    #  @details A test with multiple options starting with the same character
    def test_or5(self):
        r = "a|b|bab|bb"
        s = "bb"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

        
    ## @brief Test a more complex regexp with the | symbol, a 2-letter alphabet and a space
    #  @details A test with multiple options starting with the same character, with a string that is a space only
    def test_or6(self):
        r = "a|b|bab|bb"
        s = " "
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ''' -------------------------------------------------- '''
    ''' Testing regex with the + symbol '''
    
    ## @brief Test a regexp with the + symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a + only and the string matches the first half only
    def test_plus1(self):
        r = "a+b"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a regexp with the + symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a + only and the string matches the second half only
    def test_plus2(self):
        r = "a+b"
        s = "b"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a regexp with the + symbol and a 2-letter alphabet
    #  @details The first character in the regexp contains a + only and the string matches the entire regexp
    def test_plus3(self):
        r = "a+b"
        s = "aaaaaaab"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))


    ## @brief Test a regexp with the + symbol and a 2-letter alphabet: "many" case
    #  @details Both characters contain a + symbol and the string matches the first half only
    def test_plus4(self):
        r = "a+b+"
        s = "aaaaaaa"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a regexp with the + symbol and a 2-letter alphabet: "many" case
    #  @details Both characters contain a + symbol and the string matches the second half only
    def test_plus5(self):
        r = "a+b+"
        s = "bbbbbb"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a regexp with the + symbol and a 2-letter alphabet: "one of" case
    #  @details Both characters contain a + symbol and the string matches the first half only
    def test_plus6(self):
        r = "a+b+"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a regexp with the + symbol and a 2-letter alphabet: "one of" case
    #  @details Both characters contain a + symbol and the string matches the second half only
    def test_plus7(self):
        r = "a+b+"
        s = "b"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))
    
    ## @brief Test a regexp with the + symbol and a 2-letter alphabet: "no-value" case
    #  @details Both characters contain a + symbol and the string is empty
    def test_plus8(self):
        r = "a+b+"
        s = ""
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    
    ## @brief Test a more complex regexp with the + symbol and a 2-letter alphabet: "many" case
    #  @details Alternating sequence of characters each with a + symbol, and the string matches exactly
    def test_plus9(self):
        r = "a+b+a+b+"
        s = "aabbaaabbb"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a more complex regexp with the + symbol and a 2-letter alphabet: "one-of" and "none-of" case
    #  @details Alternating sequence of characters each with a + symbol, and the string matches partly
    def test_plus10(self):
        r = "a+b+a+b+"
        s = "a"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ## @brief Test a more complex regexp with the + symbol and a 2-letter alphabet
    #  @details Some characters have the + symbol and some do not. The string does not match.
    def test_plus11(self):
        r = "ba+b"
        s = "aaaaa"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    
    ## @brief Test a more complex regexp with the + symbol and a 2-letter alphabet
    #  @details The plus symbol surrounds a sequence of characters.
    def test_plus12(self):
        r = "(ba+b)+"
        s = "baaaaabbabbb"
        nfa = ApproximateNFA(r)
        self.assertFalse(nfa.match(0, s))

    ''' -------------------------------------------------- '''
    ''' Testing regex with the ? symbol '''
    ## @brief Test a regexp with the ? symbol and a 2-letter alphabet
    #  @details The optional symbol associates with one character and the string includes it
    def test_optional1(self):
        r = "aa?b"
        s = "aab"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))
        
    ## @brief Test a regexp with the ? symbol and a 2-letter alphabet
    #  @details The optional symbol associates with one character and the string does not include it
    def test_optional2(self):
        r = "aa?b"
        s = "ab"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))
        
    ## @brief Test a more complex regexp with the ? symbol and a 2-letter alphabet
    #  @details The plus symbol surrounds a sequence of characters and the string includes it
    def test_optional3(self):
        r = "a(ab)?b"
        s = "aabb"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

    ## @brief Test a more complex regexp with the ? symbol and a 2-letter alphabet
    #  @details The plus symbol surrounds a sequence of characters and the string does not include it
    def test_optional4(self):
        r = "a(ab)?b"
        s = "ab"
        nfa = ApproximateNFA(r)
        self.assertTrue(nfa.match(0, s))

if __name__ == '__main__':
    unittest.main()
