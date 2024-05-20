import pandas as pd
from user import getUserRecommendations
from group import getGroupRecommendations
from sequential import getSequentialRecommendations

def main():
    df = pd.read_csv("../dataset/ratings.csv")
    print('get user recommendations!')
    # print(getUserRecommendations(df, 1, df["userId"].unique()))
    print('get group recommendations!')
    # print(getGroupRecommendations(df, [1, 9]))
    print('get sequential recommendations!')
    # print(getSequentialRecommendations(df, [1, 9]))


if __name__ == "__main__":
    main()
