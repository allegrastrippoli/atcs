import pandas as pd
import numpy as np

def getCommonRatings(df, user1Ratings, user2):
    user2Ratings = df[df["userId"] == user2]
    commonRatings = pd.merge(user1Ratings, user2Ratings, on="movieId")
    return commonRatings


def getEuclideanSimilarity(df, user1Ratings, user2):
    commonRatings = getCommonRatings(df, user1Ratings, user2)
    n = len(commonRatings)
    if n <= 5:
        return 0
    else:
        return 1 / (
            1
            + np.sqrt(sum((commonRatings["rating_x"] - commonRatings["rating_y"]) ** 2))
        )


def getPearsonSimilarity(df, user1Ratings, user2):
    commonRatings = getCommonRatings(df, user1Ratings, user2)
    n = len(commonRatings)
    if n <= 5:
        return 0
    else:
        user1Mean = commonRatings["rating_x"].mean()
        user2Mean = commonRatings["rating_y"].mean()

        diff1 = commonRatings["rating_x"] - user1Mean
        diff2 = commonRatings["rating_y"] - user2Mean

        num = sum(diff1 * diff2)
        den = np.sqrt(sum((diff1) ** 2)) * np.sqrt(sum((diff2) ** 2))
        if den == 0:
            return 0
        return num / den


def getNeighboursByItem(df, user, item, allUsers, user1Ratings, k=30):
    neighbours = []
    for i in allUsers:
        iRating = df[(df["userId"] == i) & (df["movieId"] == item)]
        if i != user and not iRating.empty:
            iRatingValue = iRating["rating"].values[0]
            similarity = getPearsonSimilarity(df, user1Ratings, i)
            if similarity > 0.3:
                neighbours.append((i, iRatingValue, similarity))
            if len(neighbours) == k:
                break

    return sorted(neighbours, key=lambda x: x[2], reverse=True)[:k]


def predictMovieScores(df, user, movieId, allUsers):
    userRatings = df[df["userId"] == user]
    userMean = userRatings["rating"].mean()
    num = 0
    den = 0

    for neighbour, rating, similarity in getNeighboursByItem(
        df, user, movieId, allUsers, userRatings
    ):
        nMean = df[df["userId"] == neighbour]["rating"].mean()
        num += similarity * (rating - nMean)
        den += similarity

    if den == 0 or num == 0:
        return 0

    prediction = userMean + num / den
    return min(5, max(0, prediction))


def getUserRecommendations(df, user, allUsers, n=10):
    maxRating = df["rating"].max()
    toprated = []

    userMovies = df[df["userId"] == user]["movieId"].unique()
    allMovies = df["movieId"].unique()
    notSeenMovies = np.setdiff1d(allMovies, userMovies)

    for movie in notSeenMovies:
        prediction = predictMovieScores(df, user, movie, allUsers)
        if prediction > maxRating - 1:
            # print({user}, {movie}, {prediction})
            toprated.append(movie)
        if len(toprated) == n:
            break

    return toprated

