import pandas as pd
import numpy as np
from user import getUserRecommendations
from group import getGroupRatings
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


def getAggregationRanking(items, ratings, groupSat, k=10):
    result = []
    sortedGroupSat = sorted(groupSat.items(), key=lambda x: x[1])
    for movie in items:
        score = 0
        for i in range(len(sortedGroupSat)):
            score += (1 / (i + 1)) * ratings[(sortedGroupSat[i][0], movie)]
        result.append((movie, score))
    return [x[0] for x in sorted(result, key=lambda x: x[1], reverse=True)][:k]


def getRecommendations(users, items, userRecommendations, ratings, rounds=5):
    groupSat = {user: 1 for user in users}
    idealGroupSat = {}
    for user in users:
        idealGroupSat[user] = getUserIdealSat(user, ratings, userRecommendations[user])
    for i in range(rounds):
        seqRecommendations = getAggregationRanking(items, ratings, groupSat
        )
        for user in users:
            userC = getUserCurrentSat(user, ratings, seqRecommendations)
            groupSat[user] = userC / idealGroupSat[user]
    return seqRecommendations

def getSequentialRecommendations(df, users):
    allUsers = df["userId"].unique()
    items = []
    userRecommendation = {}
    for user in users:
        items += getUserRecommendations(df, user, allUsers)
        userRecommendation[user] = items
    ratings = getGroupRatings(df, users, set(items), allUsers)
    return getRecommendations(users, set(items), userRecommendation, ratings)


