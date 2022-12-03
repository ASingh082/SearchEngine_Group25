from nltk import word_tokenize
import json
from math import log


# ltc.lnc
class SearchComponent:
    def __init__(self, index, offsets, urls, doc_lengths, snowball):
        self.inverted_index = index
        self.offsets = offsets
        self.urls = urls
        self.doc_lengths = doc_lengths
        self.snowball = snowball

    def ask_user_input(self):
        user_input = word_tokenize(input("Enter query: "))
        return [self.snowball.stem(t) for t in user_input]

    def cosine_score(self, query):
        scores = {}
        for term in query:
            try:
                self.inverted_index.seek(self.offsets[term])
                term_info = self.inverted_index.readline().strip().split(' ', 2)
                query_weight = (1 + log(query.count(term))) * float(term_info[1])
                postings = json.loads(term_info[2])
                for doc, tf in postings.items():
                    doc_weight = 1 + log(tf)
                    if doc not in scores:
                        scores[doc] = 0
                    split_url = self.urls[doc][8:].split('/', 1)
                    if len(split_url) > 1 and self.urls[doc][8:].split('/', 1)[1] == '':
                        if term in ''.join([self.snowball.stem(t) for t in word_tokenize(self.urls[doc])])\
                                and term != 'uci':
                            scores[doc] += 5.5
                    else:
                        if len(split_url) > 1 and term in split_url[1] and \
                                term not in ['ic', 'informat', 'stat', 'cs', 'uci']:
                            scores[doc] += 6
                    scores[doc] += query_weight * doc_weight
            except KeyError:
                print("Term was not found in index")
        for doc in scores:
            scores[doc] /= self.doc_lengths[doc]
        return [doc for doc, _ in sorted(scores.items(), key=lambda item: -item[1])
                if self.doc_lengths[doc] > 35][:10]

    def print_urls(self, doc_scores):
        for doc in doc_scores:
            print(self.urls[doc])
