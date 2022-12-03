from M1 import InvertedIndex
from MergeIndexes import merge_indexes
from CalculateIDF import calculate_idf_and_final_merge


def create_index():
    inverted_index_creator = InvertedIndex()
    inverted_index_creator.create_inverted_index()
    merge_indexes()
    calculate_idf_and_final_merge()


if __name__ == '__main__':
    create_index()
