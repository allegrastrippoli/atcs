Move to the project directory and run:

```bash
python3 -m venv venv; . venv/bin/activate;  pip install -r requirements.txt 
```

Then:

```bash
python3 assignment.py
```

To run a specific test within a module:

```bash
pytest -v -r a test.py::testPredictMovieScores
pytest -v -r a test.py::testHowManyNeighbours
```