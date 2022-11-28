import M1
from MergeIndexes import merge_indexes
from CalculateIDF import calculate_idf_and_final_merge


def main():
    M1.create_inverted_index()
    merge_indexes()
    calculate_idf_and_final_merge()


if __name__ == '__main__':
    main()