import pandas as pd
import numpy as np
import cProfile


def getCommonRatings(df, user1Ratings, user2):
    """
    Given two users id, returns a dataframe with the common ratings of both users.
    Due to performance reasons istead of user 1 id, user1Ratings is pre-calculated
    """
    user2Ratings = df[df["userId"] == user2]
    commonRatings = pd.merge(user1Ratings, user2Ratings, on="movieId")
    return commonRatings


def getEuclideanSimilarity(df, user1Ratings, user2):
    """
    Given two users id, returns the euclidean similarity between them
    """
    commonRatings = getCommonRatings(df, user1Ratings, user2)
    n = len(commonRatings)
    if n == 0:
        return 0
    else:
        return 1 / (
            1
            + np.sqrt(sum((commonRatings["rating_x"] - commonRatings["rating_y"]) ** 2))
        )


def getPearsonSimilarity(df, user1Ratings, user2):
    """
    Given two users id, returns the pearson similarity between them
    """
    commonRatings = getCommonRatings(df, user1Ratings, user2)
    n = len(commonRatings)
    if n == 0:
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
    """
    Given a user id, an item id and a number k, returns a list with the k most similar users that evaluated the given item
    """
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
    """
    Given a user id and a movie id, returns the predicted score for the movie
    """
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


def getTopNRecommendations(df, user, allUsers, n=10):
    """
    Given a user id and a number n, returns a list with the n top rated movies that the user has not seen
    """

    maxRating = df["rating"].max()
    toprated = []

    userMovies = df[df["userId"] == user]["movieId"].unique()
    allMovies = df["movieId"].unique()
    notSeenMovies = np.setdiff1d(allMovies, userMovies)

    for movie in notSeenMovies:
        prediction = predictMovieScores(df, user, movie, allUsers)
        if prediction > maxRating - 1:
            toprated.append(movie)
        if len(toprated) == n:
            break

    return sorted(toprated, reverse=True)[:n]


def getAverageAggregation(df, users, items, allUsers, k=10):
    """
    Given a list of users and a list of items, returns a list with the k top rated items by the group, using the average approach
    """
    result = []
    for movie in items:
        n = 0
        for user in users:
            userRating = df[(df["userId"] == user) & (df["movieId"] == movie)]
            if userRating.empty:
                userRatingValue = predictMovieScores(df, user, movie, allUsers)
            else:
                userRatingValue = userRating["rating"].values[0]
            n += userRatingValue
        mean = n / len(users)

        result.append((movie, mean))

    return sorted(result, key=lambda x: x[1], reverse=True)[:k]


def getLeastMiseryAggregation(df, users, items, allUsers, k=10):
    """
    Given a list of users and a list of items, returns a list with the k top rated items by the group, using the least misery approach
    """
    result = []
    for movie in items:
        minValue = 5
        for user in users:
            userRating = df[(df["userId"] == user) & (df["movieId"] == movie)]
            if userRating.empty:
                userRatingValue = predictMovieScores(df, user, movie, allUsers)
            else:
                userRatingValue = userRating["rating"].values[0]
            if userRatingValue < minValue:
                minValue = userRatingValue
        result.append((movie, minValue))

    return sorted(result, key=lambda x: x[1], reverse=True)[:k]


def calculateDisagreement(users, movies, ratings, k=10):

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

        result.append((movie, maxDis))
    return sorted(result, key=lambda x: x[1])[:k]


def getMinDisagreementAggregation(df, users, items, allUsers, k=10):
    """
    Given a list of users and movies, creates movie ratings predictions for each user and returns the k movies with the lowest disagreement
    """

    ratings = {}
    for movie in items:
        for user in users:

            userRating = df[(df["userId"] == user) & (df["movieId"] == movie)]
            if userRating.empty:
                userRatingValue = predictMovieScores(df, user, movie, allUsers)
            else:
                userRatingValue = userRating["rating"].values[0]
            ratings[(user, movie)] = userRatingValue

    return calculateDisagreement(users, items, ratings)


def getGroupRecommendations(df, groupSize=3):
    """
    Given a dataframe, create a group of users, calculate the top 10 recommendations for each user, and then return the top 10 recommendations for the group
    """

    allUsers = df["userId"].unique()
    users = [1, 16, 12]
    items = []

    for user in users:
        items += getTopNRecommendations(df, user, allUsers)

    print(items)

    return getMinDisagreementAggregation(df, users, set(items), allUsers)


def main():
    df = pd.read_csv("ml-latest-small/ratings.csv")
    # print(getTopNRecommendations(df, 1, df["userId"].unique()))
    print(getGroupRecommendations(df))


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
