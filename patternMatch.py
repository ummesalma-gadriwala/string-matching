def patternMatch(pattern, text):
    patLen = len(pattern)
    text = text.split(" ")
    letter = 0
    for word in text:
        match = ""
        wordLen = len(word)
        if (patLen > wordLen):
            print(word + " does not match "+ pattern)
        for letter in range(0,wordLen-patLen):
            char = 0
            while char < patLen and word[char+letter] == pattern[char]:
                char += 1
            if char == patLen:
                for i in range(0,char):
                    match += word[i]
                print(match + " in "+ word + " matches "+ pattern)
        print(word + " does not match "+ pattern)

