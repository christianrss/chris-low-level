import re,math
from collections import Counter
def tokenize(text):
    # TODO [D6-BM25-TOKENIZE]: identifiers lowercase.
    return []
class BM25:
    def __init__(self,docs):
        # TODO [D6-BM25-INDEX]: counters, df, avgdl.
        self.docs=docs
    def rank(self,query):
        # TODO [D6-BM25-SCORE]: score e ordene.
        return []
def reciprocal_rank(ranked,relevant):
    # TODO [D6-BM25-EVAL]: retorne 1/rank do primeiro relevante.
    return 0.0
