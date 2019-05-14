from fuzzywuzzy import fuzz

class FuzzyComparer(object):
    SUBSTRINGS = ["feat.", "feat", "featuring", "ft", "ft.", "mix", "original", "extended", 
                  "edit", "radio", "ost", "with", "album version", "explicit", "clean"]

    @staticmethod
    def fuzzComparer(resultTitle, givenTitle):
        resultList = FuzzyComparer.stringProcessor(resultTitle, givenTitle)
        ratio = fuzz.token_sort_ratio(resultList[0], resultList[1])
        print(resultTitle, " vs ", givenTitle, "=", ratio)
        if ratio > 75:
            return True
        else:
            return False

    @staticmethod
    def durationCompare(resultLength, givenLength):
        print(resultLength, " vs ", givenLength)
        print(abs(int(resultLength) - int(givenLength)))
        if abs(int(resultLength) - int(givenLength)) < 10000:
            return True
        else:
            return False

    @staticmethod
    def stringProcessor(resultTitle, givenTitle):
        resultTitle = resultTitle.replace("(", "").replace(")", "").lower()
        givenTitle = givenTitle.replace("(", "").replace(")", "").lower()
        for word in FuzzyComparer.SUBSTRINGS:
            resultTitle = resultTitle.replace(word, "")
            givenTitle = givenTitle.replace(word, "")
        print(str([resultTitle, givenTitle]))
        return [resultTitle, givenTitle]


    @staticmethod
    def queryProcessor(givenTitle):
        givenTitle = givenTitle.replace("(", "").replace(")", "").lower()
        for word in FuzzyComparer.SUBSTRINGS:
            givenTitle = givenTitle.replace(word, "")
        print(givenTitle)
        return givenTitle
