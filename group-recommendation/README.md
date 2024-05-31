## Fairness in Group Recommendation
The goal is to design a user-based recommendation mechanism for movies.
Three scenarios are shown:
* Ten movies are recommended to an individual user.
* Ten movies are recommended to a group.
* A group receives sequential recommendations.

## SSD
The sequence diagram describes the flow of operations to return the top N recommended movies to a user.

![Alt text](report/Untitled%20Diagram.drawio.png)

## Run

```bash
python3 -m venv venv; . venv/bin/activate;  pip install -r requirements.txt 
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

To run a specific test within a module:

```bash
pytest -v -r a testUser.py::testPredictMovieScores
pytest -v -r a testGroup.py::testPredictDisagreement
```

## Warning
The results are considered satisfactory for educational purposes, but the code has not been rigorously tested and many aspects have been simplified.

