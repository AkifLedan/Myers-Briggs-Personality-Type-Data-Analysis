import pandas as pd
import numpy as np
import seaborn as sns
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from sklearn.model_selection import train_test_split


def flatten(big_list):
    flat = list()
    for w in big_list:
        word = re.sub(r'[^\w\s]','',w)
        word = re.sub(r'\_','',word)
        words = word.split(" ")
        flat += words
    return flat


def get_sixteen_personalities_df():
    """
    Returns a dataframe with 16 lines, each line being a personality.
    Index is the personality type in all caps: ex. "ENTJ:
    Personality type has correlating list of words, column called "complete"
    """
    df = pd.read_csv("clean_final.csv")
    # df = pd.read_csv("clean_final_new_stop_words.csv")
    sixteen_ptypes = df.groupby("type")["clean"].apply(list).to_frame()
    sixteen_ptypes["complete"] = sixteen_ptypes["clean"].apply(flatten)
    sixteen_ptypes = sixteen_ptypes.loc[:, ["complete"]]
    sixteen_ptypes["type"] = sixteen_ptypes.index
    return sixteen_ptypes    


def main():
    df = get_sixteen_personalities_df()
    # print(type(df.loc["ENTP", "complete"]))
    """
    # Test Code
    df = pd.read_csv("clean_final.csv")
    sixteen_ptypes = df.groupby("type")["clean"].apply(list).to_frame()
    sixteen_ptypes["complete"] = sixteen_ptypes["clean"].apply(flatten)
    sixteen_ptypes = sixteen_ptypes.loc[:, ["complete"]]
    sixteen_ptypes["type"] = sixteen_ptypes.index
    # sixteen_ptypes.to_csv("test.csv", index=False)
    # print(sixteen_ptypes.head())
    # sixteen_ptypes.to_csv("sixteen_ptypes.csv", index=False)
    df_new = pd.read_csv("test.csv")
    print(df_new.head())
    print(type(df_new.loc[df_new["type"] == "ENFJ", "complete"]))
    t = df_new.loc[df_new["type"] == "ENFJ", "complete"]
    t = t.tolist()
    print(type(t))
    """


if __name__ == "__main__":
    main()