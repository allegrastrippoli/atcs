import assignment
import pandas as pd
import pytest

df = pd.read_csv("ml-latest-small/ratings.csv")
users = [1, 2]
movies = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ratings = {
    (1, 1): 4.0,  # mean > 3, diff: 0
    (2, 1): 4.0,
    (1, 2): 1.0,  # mean < 3, diff: 0
    (2, 2): 1.0,
    (1, 3): 1.0,  # mean < 3, diff: 1
    (2, 3): 0.0,
    (1, 4): 3.0,  # mean > 3, diff: 0.5
    (2, 4): 3.5,
    (1, 5): 4.0,  # mean > 3, diff: 1
    (2, 5): 5.0,
    (1, 6): 3.5,  # mean > 3, diff: 2
    (2, 6): 1.5,
    (1, 7): 5.0,  # mean > 3, diff: 0
    (2, 7): 5.0,
    (1, 8): 5.0,  # mean > 3, diff: 5
    (2, 8): 0.0,
    (1, 9): 4.0,  # mean > 3, diff: 0.8
    (2, 9): 4.8,
    (1, 10): 3.5,  # mean > 3, diff: 1.5
    (2, 10): 5.0,
}
expected = [1, 7, 4, 9, 5]


def getData():
    return [
        movieId
        for movieId, _, _ in assignment.predictDisagreement(users, movies, ratings, 5)
    ]


@pytest.mark.parametrize(
    "expected, actual",
    [(expected, getData())],
)
def testPredictDisagreement(expected, actual):

    assert expected == actual
