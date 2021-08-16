# import requests
# from json import JSONDecodeError
# import secret_data
import pandas as pd


def get_words(column):
    words = []
    for word in column:
        words.extend(word.split())
    return words


def get_words_count(word_list, spam=None):
    if spam is None:
        spam = "& , ( )"

    words_count = {}
    for word in word_list:
        if word in spam:
            continue
        if word in words_count:
            words_count[word] += 1
        else:
            words_count[word] = 1
    return words_count


def sort_dict(x, reverse=True):
    return {k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=reverse)}


def create_csv_file(file_name, dictionary, element_count=30):
    with open(file_name, 'w') as f:
        for key in list(dictionary.keys())[:element_count]:
            f.write("%s,%s\n" % (key, dictionary[key]))


def main():
    file_name = "word_counter/sample_input_counter.xlsx"
    xlsx_file = pd.read_excel(file_name)
    phrases = xlsx_file["phrase"]
    create_csv_file("word_counter/sample_output_counter.csv", sort_dict(get_words_count(get_words(phrases))))


if __name__ == "__main__":
    main()
