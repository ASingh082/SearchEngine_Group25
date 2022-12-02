from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import time
import json
from math import log
# temporary until json completes

'''
start = time.time()
inverted_index_file = open('inverted_index.json', 'r', encoding='utf-8')
inverted_index = json.load(inverted_index_file)
inverted_index_file.close()
urls_file = open('urls.json', 'r', encoding='utf-8')
urls = json.load(urls_file)
urls_file.close()
end = time.time()
print("Time elapsed: ", end - start)
'''


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
                    # experimental
                    split_url = self.urls[doc][8:].split('/', 1)
                    if len(split_url) > 1 and self.urls[doc][8:].split('/', 1)[1] == '':
                        if term in ''.join([self.snowball.stem(t) for t in word_tokenize(self.urls[doc])])\
                                and term != 'uci':
                            scores[doc] += 5
                    else:
                        if len(split_url) > 1 and term in split_url[1]:
                            scores[doc] += 3
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


def main():
    snowball = SnowballStemmer(language="english")
    index_file = open('inverted_index.csv', 'r', encoding='utf-8')
    offsets_file = open('offsets.json', 'r', encoding='utf-8')
    offset_dict = json.load(offsets_file)
    urls_file = open('urls.json', 'r', encoding='utf-8')
    urls_dict = json.load(urls_file)
    doc_length_file = open('document_lengths.json', 'r', encoding='utf-8')
    doc_length_dict = json.load(doc_length_file)

    search_component = SearchComponent(index_file, offset_dict, urls_dict, doc_length_dict, snowball)
    user_input = [None]
    while user_input:
        user_input = search_component.ask_user_input()
        if not user_input:
            break
        start = time.time()
        scores = search_component.cosine_score(user_input)
        search_component.print_urls(scores)
        end = time.time()
        print(f'TIME ELAPSED FOR QUERY "{" ".join(user_input)}": {end - start} secs')

    index_file.close()
    offsets_file.close()
    urls_file.close()
    doc_length_file.close()


if __name__ == '__main__':
    main()

