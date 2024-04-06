## Fairness in Group Recommendation

Three scenarios are considered:
* Ten movies are recommended to an individual user.
* Ten movies are recommended to a group.
* A group receives sequential recommendations.
The goal is to design a recommendation mechanism that is fair, efficient, and has a high accuracy rate. All tests are repeatable, and random elements in the code have been removed.

## SSD

The sequence diagram describes the flow of operations to return the top N recommended movies to a user.

![Alt text](report/Untitled%20Diagram.drawio.png)

## Results

The experiments demonstrated promising results in terms of prediction accuracy and user satisfaction. The average accuracy score for predicting movie ratings was approximately 85%, with certain users achieving high accuracy rates. In group recommendations, the method presented in this paper, which minimizes disagreement among users, showed comparable results to other methods such as average and least misery. Indeed, although the algorithm performs well, it does not completely solve the fairness problem. In sequential recommendation, the most disadvantaged user improved his satisfaction from 39% to 94%. 

## Run

Move to the src folder and run:

```bash
python3 -m venv venv; . venv/bin/activate;  pip install -r requirements.txt 
```

Then:

```bash
python3 assignment.py
```

To run a specific test within a module:

```bash
pytest -v -r a testUser.py::testPredictMovieScores
pytest -v -r a testUser.py::testHowManyNeighbours
pytest -v -r a testGroup.py::testPredictDisagreement
```
## Warning

The results are considered satisfactory for educational purposes, but the code has not been rigorously tested and many aspects have been simplified. 
