import assignment
import pandas as pd


def printUserSimilarity(df, user1):
    for user2 in df["userId"].unique():
        if user2 != user1:
            similarity12 = assignment.getPearsonSimilarity(
                df, df[df["userId"] == user1], user2
            )
            lenCommonRatings12 = len(
                assignment.getCommonRatings(df, df[df["userId"] == user1], user2)
            )
            if similarity12 >= 0.5 and lenCommonRatings12 >= 10:
                print(f"looking for the 3rd of us")
                for user3 in df["userId"].unique():
                    if user3 != user1 and user3 != user2:
                        similarity13 = assignment.getPearsonSimilarity(
                            df, df[df["userId"] == user1], user3
                        )
                        lenCommonRatings13 = len(
                            assignment.getCommonRatings(
                                df, df[df["userId"] == user1], user3
                            )
                        )
                        similarity23 = assignment.getPearsonSimilarity(
                            df, df[df["userId"] == user2], user3
                        )
                        lenCommonRatings23 = len(
                            assignment.getCommonRatings(
                                df, df[df["userId"] == user2], user3
                            )
                        )
                        if (
                            similarity13 >= 0.5
                            and lenCommonRatings13 >= 10
                            and similarity23 >= 0.5
                            and lenCommonRatings23 >= 10
                        ):
                            print(
                                f"{user2}, {user1}, {user3} have a similarity of {similarity12} and {similarity13} and {similarity23}"
                            )


def findDissimilarUser(df, similarUsers, movies):

    maxLowScores = 0

    for user in df["userId"].unique():
        if user not in similarUsers:
            lowScores = []
            for movie in movies:
                if (
                    assignment.predictMovieScores(
                        df, user, movie, df["userId"].unique()
                    )
                    <= 3
                ):
                    lowScores.append(movie)

            if len(lowScores) > maxLowScores:
                print(f"user: {user}, {len(lowScores)} => {lowScores}")
                maxLowScores = len(lowScores)


def main():
    df = pd.read_csv("ml-latest-small/ratings.csv")

    # 62, 1, 494 have a similarity of 0.5116817192534651 and 0.5673498155007974 and 0.8344924959017579
    # lenCommonRatings_62_1 = 29
    # lenCommonRatings_62_494 = 12
    # lenCommonRatings_1_494 = 13

    movies62 = [1, 11, 14, 16, 17, 18, 25, 26, 28, 29]
    movies1 = [2, 10, 11, 13, 14, 15, 16, 17, 18, 21]
    movies494 = [1, 3, 6, 7, 10, 11, 13, 14, 16, 17]

    # the user id = 3 is the dissimilar user
    # he gave a score lower than 3 to 16 movies: [1, 2, 3, 6, 7, 10, 11, 13, 14, 15, 17, 18, 21, 25, 26, 29]

    # print(assignment.getUserRecommendations(df, 3, df["userId"].unique()))

    movies3 = [16, 28, 32, 47, 50, 53, 69, 70, 85, 99]

    movies = set(movies62 + movies1 + movies494 + movies3)
    users = [62, 1, 494, 3]

    userRecommendations = {}
    userRecommendations[62] = movies62
    userRecommendations[1] = movies1
    userRecommendations[494] = movies494
    userRecommendations[3] = movies3

    ratings = {
        (62, 1): 4.050449383596719,
        (1, 1): 4.0,
        (494, 1): 4.353396124931009,
        (3, 1): 2.910448803214357,
        (62, 2): 4.0,
        (1, 2): 4.096807901372292,
        (494, 2): 3.999083240542934,
        (3, 2): 2.841272753602722,
        (62, 3): 3.81293307856593,
        (1, 3): 4.0,
        (494, 3): 4.091090074614958,
        (3, 3): 1.2285694983667332,
        (62, 6): 4.5,
        (1, 6): 4.0,
        (494, 6): 4.377791391627971,
        (3, 6): 2.966007794413775,
        (62, 7): 3.681201968614595,
        (1, 7): 3.8903333607319714,
        (494, 7): 4.025569103487666,
        (3, 7): 0,
        (62, 10): 3.882622786348998,
        (1, 10): 4.237652656051437,
        (494, 10): 4.302849900751581,
        (3, 10): 2.9583415707569705,
        (62, 11): 4.201951949299892,
        (1, 11): 4.363994640164495,
        (494, 11): 4.4267665056667465,
        (3, 11): 0,
        (62, 13): 0,
        (1, 13): 4.211857061528549,
        (494, 13): 4.091677509737793,
        (3, 13): 0,
        (62, 14): 4.811839130548843,
        (1, 14): 4.975452396942521,
        (494, 14): 4.640335730021318,
        (3, 14): 0,
        (62, 15): 3.831598154630484,
        (1, 15): 4.044710107315243,
        (494, 15): 3.6132065489914638,
        (3, 15): 0,
        (62, 16): 4.772763536564118,
        (1, 16): 5,
        (494, 16): 4.7945796434951,
        (3, 16): 3.070092655149521,
        (62, 17): 4.2453440212436355,
        (1, 17): 4.5745990701672765,
        (494, 17): 4.224913537503873,
        (3, 17): 1.9279440954944662,
        (62, 18): 4.239660255267929,
        (1, 18): 4.669823239558554,
        (494, 18): 4.14179153629132,
        (3, 18): 2.61251996029969,
        (62, 21): 3.9456601045025046,
        (1, 21): 4.206993341526401,
        (494, 21): 4.313408469205171,
        (3, 21): 2.5010699230864,
        (62, 25): 4.167627476257433,
        (1, 25): 4.575330865779037,
        (494, 25): 4.200644189118834,
        (3, 25): 2.9138907967228014,
        (62, 26): 4.1479280188519985,
        (1, 26): 4.133590720807118,
        (494, 26): 4.439853296652347,
        (3, 26): 0,
        (62, 28): 4.795312365278691,
        (1, 28): 4.61392832995267,
        (494, 28): 4.795281866944986,
        (3, 28): 3.927944095494466,
        (62, 29): 4.655456925551295,
        (1, 29): 4.822441211247529,
        (494, 29): 4.370063603722921,
        (3, 29): 2.5975367186590548,
        (62, 32): 4.725253622684577,
        (1, 32): 4.7754744711175166,
        (494, 32): 4.795178452158773,
        (3, 32): 3.1865744532399285,
        (62, 47): 4.5,
        (1, 47): 5.0,
        (494, 47): 4.555980977464998,
        (3, 47): 3.3854298822248956,
        (62, 50): 4.831599705810741,
        (1, 50): 5.0,
        (494, 50): 4.966199019605817,
        (3, 50): 3.2935145116677473,
        (62, 53): 0,
        (1, 53): 0,
        (494, 53): 0,
        (3, 53): 3.927944095494466,
        (62, 69): 4.584427919864522,
        (1, 69): 4.743462405074105,
        (494, 69): 4.510780610475564,
        (3, 69): 3.555120597070128,
        (62, 70): 3.8987342686033735,
        (1, 70): 3.0,
        (494, 70): 4.218087938471874,
        (3, 70): 3.410775195375882,
        (62, 85): 5,
        (1, 85): 4.8044288577668235,
        (494, 85): 3.824287652645862,
        (3, 85): 3.927944095494466,
        (62, 99): 5,
        (1, 99): 0,
        (494, 99): 0,
        (3, 99): 3.927944095494466,
    }

    moviesRecMinDisagreementAggregationTop10 = [
        (28, 0.6051725689232375, 4.533116664417704),
        (85, 0.6108348485232122, 4.389165151476788),
        (70, 0.6318993506127826, 3.6318993506127826),
        (69, 0.7933272860509515, 4.3484478831210795),
        (10, 0.8870251577202763, 3.845366728477247),
        (2, 0.8930182202767645, 3.7342909738794865),
        (1, 0.9181247747211643, 3.828573577935521),
        (47, 0.9749228326975774, 4.360352714922473),
        (6, 0.9949420020966615, 3.9609497965104365),
        (25, 1.0504825352467249, 3.9643733319695262),
    ]
    moviesRecLeastMiseryAggregationTop10 = [
        (28, 3.927944095494466),
        (85, 3.824287652645862),
        (69, 3.555120597070128),
        (47, 3.3854298822248956),
        (50, 3.2935145116677473),
        (32, 3.1865744532399285),
        (16, 3.070092655149521),
        (70, 3.0),
        (6, 2.966007794413775),
        (10, 2.9583415707569705),
    ]
    moviesRecAverageAggregationTop10 = [
        (28, 4.533116664417704),
        (50, 4.522828309271077),
        (16, 4.409358958802184),
        (85, 4.389165151476788),
        (32, 4.370620249800199),
        (47, 4.360352714922473),
        (69, 4.3484478831210795),
        (29, 4.1113746147952),
        (25, 3.9643733319695262),
        (6, 3.9609497965104365),
    ]

    moviesRecMinDisagreementAggregationTop20 = [
        (28, 0.6051725689232375, 4.533116664417704),
        (85, 0.6108348485232122, 4.389165151476788),
        (70, 0.6318993506127826, 3.6318993506127826),
        (69, 0.7933272860509515, 4.3484478831210795),
        (10, 0.8870251577202763, 3.845366728477247),
        (2, 0.8930182202767645, 3.7342909738794865),
        (1, 0.9181247747211643, 3.828573577935521),
        (47, 0.9749228326975774, 4.360352714922473),
        (6, 0.9949420020966615, 3.9609497965104365),
        (25, 1.0504825352467249, 3.9643733319695262),
        (32, 1.1840457965602704, 4.370620249800199),
        (50, 1.2293137976033295, 4.522828309271077),
        (21, 1.2407130364937187, 3.7417829595801186),
        (18, 1.3034287875546835, 3.9159487478543733),
        (16, 1.3392663036526633, 4.409358958802184),
        (29, 1.5138378961361454, 4.1113746147952),
        (17, 1.8152560856078468, 3.743200181102313),
        (3, 2.0545786645201716, 3.283148162886905),
        (26, 3.180343009077866, 3.180343009077866),
        (11, 3.2481782737827833, 3.2481782737827833),
        (14, 3.6069068143781706, 3.6069068143781706),
    ]
    moviesRecLeastMiseryAggregationTop20 = [
        (28, 3.927944095494466),
        (85, 3.824287652645862),
        (69, 3.555120597070128),
        (47, 3.3854298822248956),
        (50, 3.2935145116677473),
        (32, 3.1865744532399285),
        (16, 3.070092655149521),
        (70, 3.0),
        (6, 2.966007794413775),
        (10, 2.9583415707569705),
        (25, 2.9138907967228014),
        (1, 2.910448803214357),
        (2, 2.841272753602722),
        (18, 2.61251996029969),
        (29, 2.5975367186590548),
        (21, 2.5010699230864),
        (17, 1.9279440954944662),
        (3, 1.2285694983667332),
        (7, 0),
        (11, 0),
        (13, 0),
        (14, 0),
        (15, 0),
        (26, 0),
        (53, 0),
    ]
    moviesRecAverageAggregationTop20 = [
        (28, 4.533116664417704),
        (50, 4.522828309271077),
        (16, 4.409358958802184),
        (85, 4.389165151476788),
        (32, 4.370620249800199),
        (47, 4.360352714922473),
        (69, 4.3484478831210795),
        (29, 4.1113746147952),
        (25, 3.9643733319695262),
        (6, 3.9609497965104365),
        (18, 3.9159487478543733),
        (10, 3.845366728477247),
        (1, 3.828573577935521),
        (17, 3.743200181102313),
        (21, 3.7417829595801186),
        (2, 3.7342909738794865),
        (70, 3.6318993506127826),
        (14, 3.6069068143781706),
        (3, 3.283148162886905),
        (11, 3.2481782737827833),
        (26, 3.180343009077866),
        (7, 2.899276108208558),
        (15, 2.8723787027342977),
        (99, 2.2319860238736164),
        (13, 2.0758836428165854),
    ]

    ideal62 = assignment.getUserIdealSat(62, ratings, movies62)
    ideal1 = assignment.getUserIdealSat(1, ratings, movies1)
    ideal494 = assignment.getUserIdealSat(494, ratings, movies494)
    ideal3 = assignment.getUserIdealSat(3, ratings, movies3)

    print(f"user: {62} has an ideal satisfaction score of {ideal62}")
    print(f"user: {1} has an ideal satisfaction score of {ideal1}")
    print(f"user: {494} has an ideal satisfaction score of {ideal494}")
    print(f"user: {3} has an ideal satisfaction score of {ideal3}")

    moviesRec = [x for x, _, _ in moviesRecMinDisagreementAggregationTop20][:10]

    print("Min Disagreement Aggregation")

    print(
        f"user: {62} has a current satisfaction score of {assignment.getUserCurrentSat(62, ratings, moviesRec)/ideal62}"
    )
    print(
        f"user: {1} has a current satisfaction score of {assignment.getUserCurrentSat(1, ratings, moviesRec)/ideal1}"
    )
    print(
        f"user: {494} has a current satisfaction score of {assignment.getUserCurrentSat(494, ratings, moviesRec)/ideal494}"
    )
    print(
        f"user: {3} has a current satisfaction score of {assignment.getUserCurrentSat(3, ratings, moviesRec)/ideal3}"
    )

    moviesRec = [x for x, _ in moviesRecLeastMiseryAggregationTop20][:10]

    print("Least Misery Aggregation")

    print(
        f"user: {62} has a current satisfaction score of {assignment.getUserCurrentSat(62, ratings, moviesRec)/ideal62}"
    )
    print(
        f"user: {1} has a current satisfaction score of {assignment.getUserCurrentSat(1, ratings, moviesRec)/ideal1}"
    )
    print(
        f"user: {494} has a current satisfaction score of {assignment.getUserCurrentSat(494, ratings, moviesRec)/ideal494}"
    )
    print(
        f"user: {3} has a current satisfaction score of {assignment.getUserCurrentSat(3, ratings, moviesRec)/ideal3}"
    )

    moviesRec = [x for x, _ in moviesRecAverageAggregationTop20][:10]

    print("Average Aggregation")

    print(
        f"user: {62} has a current satisfaction score of {assignment.getUserCurrentSat(62, ratings, moviesRec)/ideal62}"
    )
    print(
        f"user: {1} has a current satisfaction score of {assignment.getUserCurrentSat(1, ratings, moviesRec)/ideal1}"
    )
    print(
        f"user: {494} has a current satisfaction score of {assignment.getUserCurrentSat(494, ratings, moviesRec)/ideal494}"
    )
    print(
        f"user: {3} has a current satisfaction score of {assignment.getUserCurrentSat(3, ratings, moviesRec)/ideal3}"
    )


if __name__ == "__main__":
    main()
