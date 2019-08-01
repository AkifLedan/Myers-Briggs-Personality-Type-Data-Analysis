# Akif Ahmed (AA) and Renee Wang (AC)
# CSE 163 (A)
# This program conducts analysis on text entries from users
# of a forum of various Myers-Briggs personalities


import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


def flatten(big_list):
    """
    Takes a list of words and removes certain special characters from them
    in order to make them useful for data analysis. Those versions of
    the words are then added to a list, which is returned.
    """
    flat = list()
    for w in big_list:
        word = re.sub(r'[^\w\s]', '', w)
        word = re.sub(r'\_', '', word)
        words = word.split(" ")
        flat += words
    return flat


def get_ml_df():
    """
    Returns a dataframe that is in a formate to be used for classification
    through machine learning
    """
    df = pd.read_csv("clean_final_new_stop_words.csv")
    df['text'] = df['clean'].apply(split_by_comma)
    df['text'] = df['text'].apply(flatten)
    df['text'] = df['text'].apply(clean_list)
    df['text'] = df['text'].apply(list_to_string)
    df = df.loc[:, ['type', 'text']]
    return df


def list_to_string(list):
    """
    Takes a list of strings and returns a list where all the strings are
    concatenated together.
    """
    str = ''
    for word in list:
        str += word + ' '
    return str


def clean_list(list):
    """
    Takes a list of strings and returns a list where empty elements are removed
    and strings are stripped
    """
    return [word.strip() for word in list if word != '']


def split_by_comma(str):
    """
    Takes a string and returns a list that is the given string, str, split
    by commas
    """
    return str.split(",")


def predict(data):
    """
    Trains a machine learning model that can predict a personality type
    based on text; data is a dataframe.
    """
    X_train, X_test, y_train, y_test = train_test_split(data['text'],
                                                        data['type'],
                                                        test_size=0.2,
                                                        random_state=0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    model = MultinomialNB().fit(X_train_tfidf, y_train)
    y_test_pred = []
    for val in X_test:
        y_test_pred.append(model.predict(count_vect.transform([val])))
    count = 0
    count2 = 0
    for val in y_test_pred:
        if val == ['INFP']:
            count += 1
        else:
            count2 += 1
    print(y_test)
    count3 = 0
    for val in y_test:
        if val == 'INFP':
            count3 += 1
    print('INFP Actual: ' + str(count3))
    print('INFP Predicted: ' + str(count) + ' Other type predicted: '
          + str(count2))


def get_sixteen_personalities_df():
    """
    Returns a dataframe with 16 lines, each line being a personality.
    Index is the personality type in all caps: ex. "ENTJ:
    Personality type has correlating list of words, column called "complete"
    """
    df = pd.read_csv("clean_final_new_stop_words.csv")
    sixteen_ptypes = df.groupby("type")["clean"].apply(list).to_frame()
    sixteen_ptypes["complete"] = sixteen_ptypes["clean"].apply(flatten)
    sixteen_ptypes = sixteen_ptypes.loc[:, ["complete"]]
    sixteen_ptypes["type"] = sixteen_ptypes.index
    return sixteen_ptypes


def get_two_personalities_df():
    """
    Returns a dataframe with 2 lines, one for introverts and one for
    extroverts. Each has a correlating list of words, column called
    called "complete".
    """
    df = pd.read_csv("clean_final_new_stop_words.csv")
    df['type'] = df['type'].apply(i_or_e)
    two_ptypes = df.groupby("type")["clean"].apply(list).to_frame()
    two_ptypes["complete"] = two_ptypes["clean"].apply(flatten)
    two_ptypes = two_ptypes.loc[:, ["complete"]]
    two_ptypes["type"] = two_ptypes.index
    return two_ptypes


def i_or_e(str):
    """
    Takes a string and returns 'I' or 'E' depending on if the first
    letter of the string is 'I' or 'E'.
    """
    return str[0]


def calculate_word_counts(list):
    """
    Takes a list of words and returns a dictionary containing the words and
    their respective counts in the list
    """
    counts = {}
    for word in list:
        if word not in counts:
            counts[word] = 0
        counts[word] += 1
    return counts


def calculate_mode_words(dict):
    """
    Takes a dictionary and returns a list of tuples of the key-value
    pairs of the 3 highest values in the dictionary. Common words and
    stop words are excluded from the calculations. The worlds "think",
    "people", and "know" are also excluded because they are the 3 most
    common words among all 16 personality types.
    """
    max1 = -1
    max1_key = ''
    max2 = -1
    max2_key = ''
    max3 = -1
    max3_key = ''
    stopws = ["a", "an", "and", "are", "as", "at", "be", "by",
              "for", "from", "has", "he", "in", "is", "it", "its", "of",
              "on", "that", "the", "to", "was", "were", "will", "with", "I",
              "you", "but", "have", "me", "she", "my", "like", "not", "so",
              "or", "just", "do", "really", "one", "know", "think", "people"]
    for key in dict.keys():
        if key not in stopws:
            old_max3 = max3
            old_max2 = max2
            old_max1 = max1
            max3 = max(dict[key], max3)
            if max3 != old_max3:
                max3_key = key
            max2 = max(max3, max2)
            if max2 != old_max2:
                max3 = old_max2
                max3_key = max2_key
                max2_key = key
            max1 = max(max2, max1)
            if max1 != old_max1:
                max2 = old_max1
                max2_key = max1_key
                max1_key = key
    return [(max1, max1_key), (max2, max2_key), (max3, max3_key)]


def most_common_words(data):
    """
    Takes a dataframe and returns the same data with 2 additional columns.
    One new column contains a dictionary containing the counts of all the words
    in each row of the dataframe. The second new column contains a list of
    tuples with the keys in the count with the three highest values.
    """
    data["counts"] = data["complete"].apply(calculate_word_counts)
    data["mode_words"] = data["counts"].apply(calculate_mode_words)
    return data


def main():
    source = get_sixteen_personalities_df()
    df = most_common_words(source)
    print(df)

    source2 = get_two_personalities_df()
    df2 = most_common_words(source2)
    print(df2)

    df3 = get_ml_df()
    print(df3)
    predict(df3)


if __name__ == "__main__":
    main()
