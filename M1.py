import os
import json
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from math import sqrt
import time


class InvertedIndex:
    def __init__(self):
        self.inverted_index = {}
        self.inverted_index_bold = {}
        self.doc_num_to_url = {}
        self.doc_lengths = {}
        self.current_doc_index = {}
        self.unique_tokens = set()
        self.snowball = SnowballStemmer(language="english")
        self.doc_number = 1
        self.partial_index_number = 1

    def create_inverted_index(self):
        path = os.getcwd()
        path += '\\DEV'
        for subdir, dirs, files in os.walk(path):
            for file in files:
                print(os.path.join(subdir, file))
                current_file = open(os.path.join(subdir, file))
                json_data = json.load(current_file)
                soup = BeautifulSoup(json_data['content'], 'lxml')
                self.index_important_words(soup)
                self.index_regular_words(soup)
                self.calculate_doc_length()
                self.doc_num_to_url[self.doc_number] = json_data['url']
                if len(self.inverted_index) >= 500000:
                    self.offload_index()
                self.doc_number += 1
        self.offload_index()
        with open('urls.json', 'w', encoding='utf-8') as urls_file:
            json.dump(self.doc_num_to_url, urls_file)
        with open('document_lengths.json', 'w', encoding='utf-8') as doc_lengths_file:
            json.dump(self.doc_lengths, doc_lengths_file)

    def index_important_words(self, soup):
        stemmed_list = set()
        for imp in soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title']):
            imp_tokens = [i for i in word_tokenize(imp.get_text())]
            for token in imp_tokens:
                stemmed = self.snowball.stem(token)
                stemmed_list.add(stemmed)
                self.unique_tokens.add(stemmed)
                if stemmed not in self.current_doc_index:
                    self.current_doc_index[stemmed] = 0
                self.current_doc_index[stemmed] += 1
                if stemmed not in self.inverted_index:
                    self.inverted_index[stemmed] = {}
                if self.doc_number not in self.inverted_index[stemmed]:
                    self.inverted_index[stemmed][self.doc_number] = 0
                self.inverted_index[stemmed][self.doc_number] += 2

    def index_regular_words(self, soup):
        stemmed_list = set()
        for data in soup(['style', 'script', '[document]', 'head', 'title', 'strong',
                          'b', 'h1', 'h2', 'h3']):
            data.extract()
        tokens = [t for t in word_tokenize(soup.get_text())]
        for t in tokens:
            stemmed = self.snowball.stem(t)
            self.unique_tokens.add(stemmed)
            stemmed_list.add(stemmed)
            if stemmed not in self.current_doc_index:
                self.current_doc_index[stemmed] = 0
            self.current_doc_index[stemmed] += 1
            if stemmed not in self.inverted_index:
                self.inverted_index[stemmed] = {}
            if self.doc_number not in self.inverted_index[stemmed]:
                self.inverted_index[stemmed][self.doc_number] = 0
            self.inverted_index[stemmed][self.doc_number] += 1

    def calculate_doc_length(self):
        normalized_length = 0
        for term in self.current_doc_index:
            normalized_length += self.current_doc_index[term] ** 2
        self.doc_lengths[self.doc_number] = sqrt(normalized_length)
        self.current_doc_index.clear()

    def offload_index(self):
        with open(f'partial_index{self.partial_index_number}.json', 'w', encoding='utf-8') as partial_index_file:
            json.dump(self.inverted_index, partial_index_file)
        self.inverted_index.clear()
        self.partial_index_number += 1

'''
def output_deliverables(time_elapsed):
    print('NUMBER OF INDEXED DOCUMENTS: ', doc_number)
    print('NUMBER OF UNIQUE TOKENS: ', len(unique_tokens))
    with open('inverted_index.json', 'w', encoding='utf-8') as inv_idx_file:
        json.dump(inverted_index, inv_idx_file)
    with open('important_index.json', 'w', encoding='utf-8') as imp_inv_idx_file:
        json.dump(inverted_index_bold, imp_inv_idx_file)
    print('TIME ELAPSED: ', time_elapsed)
'''
