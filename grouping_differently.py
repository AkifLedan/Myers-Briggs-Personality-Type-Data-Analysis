# Akif Ahmed (AA) and Renee Wang (AC)
# CSE 163 (A)
# Groups pandas dataframes in unique ways by personality type

import os
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import fileinput


def extrovert_introvert():
    extrovert = ["ENFJ", "ENFP", "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ",
                 "ESTP"]
    introvert = ["INFJ", "INFP", "INTJ", "INTP", "ISFJ", "ISFP", "ISTJ",
                 "ISTP"]
    extrovert = [x + str("_word_list.txt") for x in extrovert]
    introvert = [x + str("_word_list.txt") for x in introvert]
    combine_text_files(extrovert, "extrovert_words.txt")
    combine_text_files(introvert, "introvert_words.txt")
    wordclouds("extrovert_words.txt")
    wordclouds("introvert_words.txt")


def roles():
    analyst = ["ENTP", "ENTJ", "INTP", "INTJ"]
    diplomat = ["ENFP", "INFP", "ENFJ", "INFJ"]
    sentinel = ["ESTJ", "ESFJ", "ISTJ", "ISFJ"]
    explorer = ["ESTP", "ESFP", "ISTP", "ISFP"]
    analyst = [x + str("_word_list.txt") for x in analyst]
    diplomat = [x + str("_word_list.txt") for x in diplomat]
    sentinel = [x + str("_word_list.txt") for x in sentinel]
    explorer = [x + str("_word_list.txt") for x in explorer]
    combine_text_files(analyst, "analyst_words.txt")
    combine_text_files(diplomat, "diplomat_words.txt")
    combine_text_files(sentinel, "sentinel_words.txt")
    combine_text_files(explorer, "explorer_words.txt")
    wordclouds("analyst_words.txt")
    wordclouds("diplomat_words.txt")
    wordclouds("sentinel_words.txt")
    wordclouds("explorer_words.txt")


def combine_text_files(list_files, file_name):
    with open(file_name, "w") as file:
        input_lines = fileinput.input(list_files)
        file.writelines(input_lines)


def wordclouds(text_file):
    pic_file = str(text_file)[0:5] + ".png"
    t = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text = open(path.join(t, text_file)).read()
    wordcloud = WordCloud(background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(pic_file)


def main():
    extrovert_introvert()
    roles()


if __name__ == "__main__":
    main()
