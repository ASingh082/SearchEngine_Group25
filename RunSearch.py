import json
import time
from M2 import SearchComponent
from nltk.stem.snowball import SnowballStemmer


def run_search():
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
    run_search()