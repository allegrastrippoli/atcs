import pandas as pd
import numpy as np
import cProfile


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
            print({user}, {movie}, {prediction})
            toprated.append(movie)
        if len(toprated) == n:
            break

    return toprated


############################################################################################################


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

    for user in users:
        items += getUserRecommendations(df, user, allUsers)

    ratings = getGroupRatings(df, users, set(items), allUsers)

    # return getAverageAggregation(df, users, items, ratings, allUsers)
    # return getLeastMiseryAggregation(df, users, items, ratings, allUsers)
    return getMinDisagreementAggregation(df, users, set(items), ratings, allUsers)


############################################################################################################


def getUserIdealSat(user, ratings, recommendedForUser):
    preferenceScore = 0

    for item in recommendedForUser:
        preferenceScore += ratings[(user, item)]

    return preferenceScore


def getUserCurrentSat(user, ratings, recommendedForGroup):
    preferenceScore = 0
    for item in recommendedForGroup:
        preferenceScore += ratings[(user, item)]

    return preferenceScore


def getHybridAggregation(users, items, ratings, groupSat, k=10):
    result = []
    for movie in items:

        score = 0

        for user in users:

            score += (1 / groupSat[user]) * ratings[(user, movie)]

        result.append((movie, score))

    return [x[0] for x in sorted(result, key=lambda x: x[1], reverse=True)][:k]


def getHybridAggregationRanking(users, items, ratings, groupSat, k=10):
    result = []

    sortedGroupSat = sorted(groupSat.items(), key=lambda x: x[1])

    for movie in items:

        score = 0

        for i in range(len(sortedGroupSat)):

            score += (1 / (i + 1)) * ratings[(sortedGroupSat[i][0], movie)]

        result.append((movie, score))

    return [x[0] for x in sorted(result, key=lambda x: x[1], reverse=True)][:k]


def getSequentialRecommendations(
    df, users, items, userRecommendations, ratings, rounds=5
):

    groupSat = {user: 1 for user in users}
    idealGroupSat = {}

    for user in users:
        idealGroupSat[user] = getUserIdealSat(user, ratings, userRecommendations[user])

    for i in range(rounds):

        groupRecommendations = getHybridAggregationRanking(
            users, items, ratings, groupSat
        )

        for user in users:
            userC = getUserCurrentSat(user, ratings, groupRecommendations)
            groupSat[user] = userC / idealGroupSat[user]

    return groupRecommendations


def main():
    df = pd.read_csv("ml-latest-small/ratings.csv")
    # print(getUserRecommendations(df, 1, df["userId"].unique()))


if __name__ == "__main__":
    # cProfile.run("main()")
    main()
