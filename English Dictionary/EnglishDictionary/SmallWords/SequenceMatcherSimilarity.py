from difflib import SequenceMatcher


def SimilarityRate(sourceWord, targetWord):
    return SequenceMatcher(None, sourceWord, targetWord).ratio()
