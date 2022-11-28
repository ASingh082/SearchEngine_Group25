import json


def merge_indexes():
    i = 1
    word_count = 1
    num_partial_indexes = 5
    offsets = {}
    with open('index.csv', 'a', encoding='utf-8') as index_file:
        while i <= num_partial_indexes:
            offsets[f'offsets{i}'] = {}
            current_offset = offsets[f'offsets{i}']
            with open(f'partial_index{i}.json', 'r', encoding='utf-8') as partial_index_file:
                data = json.load(partial_index_file)
                for key in data:
                    print(f'WORD COUNT: {word_count}')
                    word_count += 1
                    current_offset[key] = index_file.tell()
                    index_file.write(f'{key} {data[key]}\n')
            i += 1
    with open('offsets.json', 'w') as offset_file:
        json.dump(offsets, offset_file)
