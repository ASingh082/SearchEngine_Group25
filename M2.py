from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import time
import json
#temporary until json completes

start = time.time()
snowball = SnowballStemmer(language="english")
inverted_index_file = open('inverted_index.json', 'r', encoding='utf-8')
inverted_index = json.load(inverted_index_file)
inverted_index_file.close()
urls_file = open('urls.json', 'r', encoding='utf-8')
urls = json.load(urls_file)
urls_file.close()
end = time.time()
print("Time elapsed: ", end - start)


def ask_user_input():
    global snowball
    user_input = word_tokenize(input("Enter query: "))
    return [snowball.stem(t) for t in user_input]


# Rankings are currently based on frequency, tf-idf scoring will be implemented later
def intersect(p1, p2):
    global inverted_index
    if p1 == p2:
        if p1 in inverted_index:
            return inverted_index[p1]
    similar_postings = {}
    p1_postings = {}
    p2_postings = {}
    if p1 in inverted_index:
        p1_postings = inverted_index[p1]
    if p2 in inverted_index:
        p2_postings = inverted_index[p2]
    for k, v in p1_postings.items():
        if k in p2_postings:
            similar_postings[k] = v + p2_postings[k]
    return similar_postings


if __name__ == '__main__':
    ui = ask_user_input()
    while len(ui) > 0:
        start = time.time()
        idx = 0
        postings = {}
        print(ui)
        if len(ui) == 1:
            postings = intersect(ui[0], ui[0])
        while idx + 1 < len(ui):
            temp_postings = intersect(ui[idx], ui[idx + 1])
            for posting, frequency in temp_postings.items():
                if posting not in postings:
                    postings[posting] = frequency
                else:
                    postings[posting] += frequency
            idx += 1
        postings = {k: v for k, v in sorted(postings.items(), key=lambda item: -item[1])}
        url_num = 0
        for k in postings:
            print(urls[k])
            if url_num > 4:
                break
            url_num += 1
        end = time.time()
        print(end - start)
        ui = ask_user_input()