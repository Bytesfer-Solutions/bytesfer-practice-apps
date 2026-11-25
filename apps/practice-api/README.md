# Practice enrolment API

A small practice API for "API Testing with Python" by Bytesfer Solutions, to run on your own computer. It is the same enrolment API as in "Project: testing the enrolment API", served over real HTTP, so you can test it with the `requests` library exactly as you would test an API at work. All data is made up and resets whenever you ask.

## Get it
This folder is `apps/practice-api` in https://github.com/Bytesfer-Solutions/bytesfer-practice-apps. On that page choose **Code**, then **Download ZIP**, unzip it and open the `apps/practice-api` folder in a terminal (or clone the repository with Git).

## What you need
- Python 3.12 or newer (https://www.python.org/downloads/)
- The two packages in `requirements.txt` (pytest and requests)

## Set up (once)
```
python -m venv .venv
.venv\Scripts\activate          (Windows)
source .venv/bin/activate       (macOS or Linux)
pip install -r requirements.txt
```

## Run it
1. Start the API in one terminal: `python serve.py`. It prints `Practice API on http://127.0.0.1:8000 (Ctrl+C to stop)`.
2. In a second terminal (with the same `.venv` active), run the tests: `pytest -q`.
3. Stop the API with Ctrl+C when you are done.

`test_example.py` is the lesson's Example. Copy your own test files from the course into this folder: `fake_api.py` here has the same names as the workspace's, but sends real requests to the server, so your tests run unchanged. Every `fake_api.Session()` calls `POST /reset` first, so each test starts from the same data.

## The API
| Method and path | What it does |
|---|---|
| `GET /courses` | Lists the courses |
| `POST /login` | `{"username", "password"}` gives a token; wrong details give 401 |
| `GET /enrolments` | The logged-in learner's enrolments (send `Authorization: Bearer <token>`) |
| `POST /enrolments` | `{"course_id"}` enrols the logged-in learner |
| `DELETE /enrolments/<id>` | Cancels one of your enrolments |
| `POST /reset` | Puts the starting data back (for tests only) |

Practice logins: `meera` / `learn-123` and `arjun` / `learn-456` (made up). To use another port: `python serve.py 8001` and set `PRACTICE_API_URL=http://127.0.0.1:8001` before running pytest.

## Files
- `app.py`: the API's rules and data (the same file as in the lesson)
- `serve.py`: runs `app.py` as an HTTP server (standard library only)
- `fake_api.py`: the workspace's names, backed by `requests`
- `test_example.py`: example tests to start from
