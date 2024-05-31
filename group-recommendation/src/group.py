import pandas as pd
import numpy as np
from .user import predictMovieScores
from .user import getUserRecommendations

def getAverageAggregation(users, items, ratings, k=10):
    result = []
    for movie in items:
        n = 0
        for user in users:
            userRating = ratings[(user, movie)]
            n += userRating
        mean = n / len(users)

        result.append((movie, mean))

    return sorted(result, key=lambda x: x[1], reverse=True)[:k]


def getLeastMiseryAggregation(users, items, ratings, k=10):
    result = []
    for movie in items:
        minValue = 5
        for user in users:
            userRating = ratings[(user, movie)]
            if userRating < minValue:
                minValue = userRating
        result.append((movie, minValue))

    return sorted(result, key=lambda x: x[1], reverse=True)[:k]


def getMinDisagreementAggregation(users, movies, ratings, k=10):
    result = []

    for movie in movies:
        meanGoup = 0
        for i in range(len(users)):
            meanGoup += ratings[(users[i], movie)]
        meanGoup /= len(users)

        maxDis = 0
        for i in range(len(users)):
            candidate = abs(ratings[(users[i], movie)] - meanGoup) 
            if candidate > maxDis:
                maxDis = candidate

        if meanGoup > 3:
            result.append((movie, maxDis, meanGoup))

    return sorted(result, key=lambda x: x[1])[:k]


def getGroupRatings(df, users, items, allUsers):
    ratings = {}
    for movie in items:
        for user in users:

            userRating = df[(df["userId"] == user) & (df["movieId"] == movie)]
            if userRating.empty:
                userRatingValue = predictMovieScores(df, user, movie, allUsers)
            else:
                userRatingValue = userRating["rating"].values[0]
            ratings[(user, movie)] = userRatingValue

    return ratings


def getGroupRecommendations(df, users):
    allUsers = df["userId"].unique()
    items = []
    for user in users:
        items += getUserRecommendations(df, user, allUsers)
    ratings = getGroupRatings(df, users, set(items), allUsers)
    return getMinDisagreementAggregation(users, set(items), ratings)


