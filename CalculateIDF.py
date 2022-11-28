import json
from math import log

# Does a final merge of all the indexes and calculates DF, maybe IDF
NUM_DOCUMENTS = 55394
idf_scores = {}
final_offset = {}


def calculate_idf_and_final_merge():
    global NUM_DOCUMENTS
    global idf_scores
    global final_offset

    set_tokens = set()
    with open('offsets.json', 'r', encoding='utf-8') as offset_file:
        offsets = json.load(offset_file)
    final_index_file = open('final_inverted_index.csv', 'a', encoding='utf-8')
    with open('index.csv', 'r', encoding='utf-8') as index_file:
        for offset_num, offset_dict in enumerate(offsets.values()):
            print(f'We are current in offset_dict: ', offset_num + 1)
            for token, offset in offset_dict.items():
                if token not in set_tokens:
                    merged_dict = {}
                    for offset_dict2 in offsets.values():
                        if token in offset_dict2:
                            index_file.seek(offset_dict2[token])
                            dict_postings = eval(index_file.readline().strip().split(' ', 1)[1])
                            merged_dict.update(dict_postings)
                    idf_scores[token] = log(NUM_DOCUMENTS / len(merged_dict))
                    final_offset[token] = final_index_file.tell()
                    final_index_file.write(f'{token} {merged_dict}\n')
                    set_tokens.add(token)
    final_index_file.close()
    dump_json()


def dump_json():
    with open('idf_scores.json', 'w', encoding='utf-8') as doc_freq_file:
        json.dump(idf_scores, doc_freq_file)
    with open('final_offset.json', 'w', encoding='utf-8') as final_offset_file:
        json.dump(final_offset, final_offset_file)
