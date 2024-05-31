import pandas as pd
import pytest
from src.user import predictMovieScores
from src.user import getNeighboursByItem

def getDf():
    return pd.read_csv("../dataset/ratings.csv")


def getData():
    df = getDf()
    user1Ratings = df[df["userId"] == 610]
    testData = []

    for i in range(len(user1Ratings)):
        row = user1Ratings.iloc[i]
        movie = row["movieId"]
        expected = row["rating"]
        testData.append((movie, expected))

    return testData


@pytest.mark.parametrize("movie, expected", getData())
def testPredictMovieScores(movie, expected):
    df = getDf()
    allUsers = df["userId"].unique()
    assert round(
        predictMovieScores(df, 610, movie, allUsers), 0
    ) == pytest.approx(expected, abs=1)


@pytest.mark.parametrize("movie, _", getData())
def testHowManyNeighbours(movie, _):
    df = getDf()
    allUsers, user1Ratings = df["userId"].unique(), df[df["userId"] == 1]
    assert (
        len(getNeighboursByItem(df, 1, movie, allUsers, user1Ratings)) == 30
    )
