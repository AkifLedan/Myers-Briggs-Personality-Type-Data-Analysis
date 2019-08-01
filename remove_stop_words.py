"""
Akif Ahmed (AA) and Renee Wang (AC)
CSE 163 (A)
Takes original file and removes "|||" separators
Removes links and words containing numeric values
Should remove all punctuation including apostrophes
Lowercase except for "I" by itself: "I've" would become ive
Removes stop words
"""

import pandas as pd
import re
from nltk.corpus import wordnet
from spacy.lang.en.stop_words import STOP_WORDS


def parse(csv):
    return pd.read_csv(csv)


def split_by_pipes(str):
    return str.split("|||")


def hasNumbers(input_str):
    return any(char.isdigit() for char in input_str)


def rmv_stop_words(word):
    stopws = STOP_WORDS
    """
    stopws = set()
    stopws = ["a", "an", "and", "are", "as", "at", "be", "by",
              "for", "from", "has", "he", "in", "is", "it", "its", "of",
              "on", "that", "the", "to", "was", "were", "will", "with"]
    """
    return word in stopws


def clean(strlist):
    all_words = list()
    for entry in strlist:
        words = entry.split(" ")
        for word in words:
            if "http" not in word:
                if not hasNumbers(word):  # removes numbers
                    word = re.sub(r'[^\w\s]', '', word)
                    word = re.sub(r'\_', '', word)
                    if word != 'I':
                        word = word.lower()
                    if word == 'i':
                        word = "I"
                    if word != "":  # removes empty strings in list
                        if not rmv_stop_words(word):  # removes stop words
                            if wordnet.synsets(word):
                                all_words.append(word)
    return all_words


def main():
    data = parse('mbti_1.csv')
    data["split"] = data["posts"].apply(split_by_pipes)
    data["clean"] = data["split"].apply(clean)
    new_df = data.loc[:, ["type", "clean"]]
    new_df.to_csv("clean_data_new_stop_words.csv")
    print("done")


if __name__ == "__main__":
    main()
