import json
import os
from math import log

# Does a final merge of all the indexes and calculates DF, maybe IDF
NUM_DOCUMENTS = 55393
idf_scores = {}
final_offset = {}


def calculate_idf_and_final_merge():
    global NUM_DOCUMENTS
    global idf_scores
    global final_offset

    set_terms = set()
    with open('temp_offsets.json', 'r', encoding='utf-8') as offset_file:
        offsets = json.load(offset_file)
    final_index_file = open('inverted_index.csv', 'a', encoding='utf-8')
    with open('temp_index.csv', 'r', encoding='utf-8') as index_file:
        for offset_num, offset_dict in enumerate(offsets.values()):
            print(f'We are current in offset_dict: ', offset_num + 1)
            for term, offset in offset_dict.items():
                if term not in set_terms:
                    merged_dict = {}
                    for offset_dict2 in offsets.values():
                        if term in offset_dict2:
                            index_file.seek(offset_dict2[term])
                            #dict_postings = eval(index_file.readline().strip().split(' ', 1)[1])
                            dict_postings = json.loads(index_file.readline().strip().split(' ', 1)[1])
                            merged_dict.update(dict_postings)
                    idf_scores[term] = log(NUM_DOCUMENTS / len(merged_dict))
                    final_offset[term] = final_index_file.tell()
                    final_index_file.write(term + ' ' + str(idf_scores[term]) + ' ')
                    json.dump(merged_dict, final_index_file)
                    final_index_file.write('\n')
                    #final_index_file.write(f'{term} {merged_dict}\n')
                    set_terms.add(term)
    final_index_file.close()
    dump_json()


def dump_json():
    #if os.path.isfile('temp_offsets.json'):
    #    os.remove('temp_offsets.json')
    #if os.path.isfile('temp_index.csv'):
    #    os.remove('temp_index.csv')
    with open('idf_scores.json', 'w', encoding='utf-8') as doc_freq_file:
        json.dump(idf_scores, doc_freq_file)
    with open('offsets.json', 'w', encoding='utf-8') as final_offset_file:
        json.dump(final_offset, final_offset_file)
