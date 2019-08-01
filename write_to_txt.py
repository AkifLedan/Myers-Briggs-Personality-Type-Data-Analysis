"""
Akif Ahmed (AA) and Renee Wang (AC)
CSE 163 (A)
Writes each line of the personalities data into a separate text file
so that each personality has a correlating text file of a list of words.
"""

import numpy as np
from sorting_into_personalities import get_sixteen_personalities_df


def write_file(df, ptype):
    word_list = df.loc[ptype, "complete"]
    file_name = "new_" + str(ptype) + "_word_list.txt"
    row = np.asarray(word_list)
    np.savetxt(file_name, row, fmt="%s")


def get_ptypes():
    df = get_sixteen_personalities_df()
    types = df.loc[:, "type"]
    types = types.tolist()
    return types


def main():
    df = get_sixteen_personalities_df()
    # row = df.loc["ENTP", "complete"]
    # row = np.asarray(row)
    # np.savetxt("test_2.txt", row, fmt="%s")
    # write_file(df, "ENTP")
    types = df.loc[:, "type"]
    types = types.tolist()
    for t in get_ptypes():
        write_file(df, t)


if __name__ == "__main__":
    main()
