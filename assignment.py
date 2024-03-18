import pandas as pd
import numpy as np
import cProfile


def getCommonRatings(df, user1Ratings, user2):
    """
    Given two users id, returns a dataframe with the common ratings of both users
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


def getNeighboursByItem(df, user, item, allUsers, user1Ratings):
    """
    Given a user id, an item id and a number k, returns a list with the k most similar users that evaluated the given item
    """
    k = 50
    neighbours = []
    for i in allUsers:
        iRating = df[(df["userId"] == i) & (df["movieId"] == item)]
        if i != user and not iRating.empty:
            iRatingValue = iRating["rating"].values[0]
            neighbours.append(
                (i, iRatingValue, getPearsonSimilarity(df, user1Ratings, i))
            )

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

    if den == 0:
        return userMean

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
        if prediction == maxRating:
            toprated.append(movie)
        if len(toprated) == n:
            return toprated

    return toprated


def getGroupAverage(df, users, items, allUsers, k=10):
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


def getGroupLeastMisery(df, users, items, allUsers, k=10):
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


def getSumSquareDifferences(users, movies, ratings, k=10):
    """
    Given a list of users, movies, ratings, returns a list with the k movies with the smallest sum of square differences
    """

    result = []

    for movie in movies:
        ssd = 0
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                user1 = users[i]
                user2 = users[j]
                if (user1, movie) in ratings and (user2, movie) in ratings:
                    rating1 = ratings[(user1, movie)]
                    rating2 = ratings[(user2, movie)]
                    diff = (rating1 - rating2) ** 2
                    ssd += diff
        result.append((movie, ssd))

    return sorted(result, key=lambda x: x[1])[:k]


def getGroupSSD(df, users, items, allUsers, k=10):
    """
    Given a list of users and movies, creates movie ratings predictions for each user and returns the k movies with the smallest sum of square differences
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

    return getSumSquareDifferences(users, items, ratings)


def getTop10GroupRecommendations(df, groupSize=3):
    """
    Given a dataframe, create a group of users, calculate the top 10 recommendations for each user, and then return the top 10 recommendations for the group
    """

    allUsers = df["userId"].unique()
    users = [1, 16, 12]
    items = []

    for user in users:
        items += getTopNRecommendations(df, user, allUsers)

    return getGroupSSD(df, users, set(items), allUsers)


def main():
    df = pd.read_csv("ml-latest-small/ratings.csv")
    print(getTop10GroupRecommendations(df))


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
