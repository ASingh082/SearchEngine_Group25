import os
import json
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import time

inverted_index = {}
inverted_index_bold = {}
doc_num_to_url = {}
unique_tokens = set()
snowball = SnowballStemmer(language="english")
doc_number = 1


def create_inverted_index():
    global inverted_index
    global inverted_index_bold
    global doc_num_to_url
    global unique_tokens
    global snowball
    global doc_number
    start = time.time()
    path = os.getcwd()
    path += '\DEV'
    for subdir, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(subdir, file))
            current_file = open(os.path.join(subdir, file))
            json_data = json.load(current_file)
            soup = BeautifulSoup(json_data['content'], 'lxml')
            len_imp = create_important_index(soup)
            create_text_index(soup, len_imp)
            doc_num_to_url[doc_number] = json_data['url']
            doc_number += 1
    end = time.time()
    output_deliverables(end - start)


def create_important_index(soup):
    length_imp = 0
    stemmed_list = set()
    for imp in soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        imp_tokens = [i for i in word_tokenize(imp.get_text())]
        length_imp += len(imp_tokens)
        for token in imp_tokens:
            stemmed = snowball.stem(token)
            stemmed_list.add(stemmed)
            unique_tokens.add(stemmed)
            if stemmed not in inverted_index_bold:
                inverted_index_bold[stemmed] = {}
            if doc_number not in inverted_index_bold[stemmed]:
                inverted_index_bold[stemmed][doc_number] = 0
            inverted_index_bold[stemmed][doc_number] += 1
    for data in soup(['style', 'script', '[document]', 'head', 'title', 'strong',
                      'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        data.extract()
    tokens = [t for t in word_tokenize(soup.get_text())]
    #for stemmed in stemmed_list:
    #    inverted_index_bold[stemmed][doc_number] /= len(tokens) + length_imp
    return length_imp


def create_text_index(soup, len_imp):
    stemmed_list = set()
    for data in soup(['style', 'script', '[document]', 'head', 'title', 'strong',
                      'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        data.extract()
    tokens = [t for t in word_tokenize(soup.get_text())]
    for t in tokens:
        token = snowball.stem(t)
        unique_tokens.add(token)
        stemmed_list.add(token)
        if token not in inverted_index:
            inverted_index[token] = {}  # doc_number : count
        if doc_number not in inverted_index[token]:
            inverted_index[token][doc_number] = 0
        inverted_index[token][doc_number] += 1
    #for stemmed in stemmed_list:
    #    inverted_index[stemmed][doc_number] /= len(tokens) + len_imp


def output_deliverables(time_elapsed):
    print('NUMBER OF INDEXED DOCUMENTS: ', doc_number)
    print('NUMBER OF UNIQUE TOKENS: ', len(unique_tokens))
    with open('inverted_index.json', 'w', encoding='utf-8') as inv_idx_file:
        json.dump(inverted_index, inv_idx_file)
    with open('important_index.json', 'w', encoding='utf-8') as imp_inv_idx_file:
        json.dump(inverted_index_bold, imp_inv_idx_file)
    with open('urls.json', 'w', encoding='utf-8') as urls:
        json.dump(doc_num_to_url, urls)
    print('TIME ELAPSED: ', time_elapsed)


if __name__ == '__main__':
    create_inverted_index()
