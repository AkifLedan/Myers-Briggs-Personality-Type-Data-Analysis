"""
Takes original file and removes "|||" separators
Removes links and words containing numeric values
Should remove all punctuation including apostrophes
Lowercase except for "I" by itself: "I've" would become ive
"""

import pandas as pd
import re


def parse(csv):
    return pd.read_csv(csv)


def split_by_pipes(str):
    return str.split("|||")


def hasNumbers(input_str):
    return any(char.isdigit() for char in input_str)


def clean(strlist):
    all_words = list()
    for entry in strlist:
        words = entry.split(" ")
        for word in words:
            if "http" not in word: # removes links
                if not hasNumbers(word): # removes numbers
                    word = re.sub(r'[^\w\s]','',word)
                    word = re.sub(r'\_','',word) 
                    if word != 'I':
                        word = word.lower()
                    if word == 'i':
                        word = "I"
                    if word != "": # removes empty strings in list
                        all_words.append(word)
    return all_words


def main():
    data = parse('mbti_1.csv')
    data["split"] = data["posts"].apply(split_by_pipes)
    data["clean"] = data["split"].apply(clean)
    new_df = data.loc[:, ["type", "clean"]]
    new_df.to_csv("clean_data.csv")



if __name__ == "__main__":
    main()
