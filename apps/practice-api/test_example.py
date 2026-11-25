import pytest

import fake_api

# Plan
# GET /courses: list matches the schema
# POST /login: right password gives a token; wrong password and unknown user give 401
# POST /enrolments: no token gives 401; enrolling takes a seat
# Still to do (Challenge): duplicates, full batch, last seat, other learners, cancel, journey

COURSE = {"id": int, "title": str, "fee": int, "seats_left": int}


@pytest.fixture
def client():
    return fake_api.Session()


@pytest.fixture
def meera(client):
    response = client.post("/login", json={"username": "meera", "password": "learn-123"})
    client.headers["Authorization"] = "Bearer " + response.json()["token"]
    return client


def seats_left(client, course_id):
    for course in client.get("/courses").json():
        if course["id"] == course_id:
            return course["seats_left"]


def test_courses_match_the_schema(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert fake_api.check_schema(response.json(), [COURSE]) == []


@pytest.mark.parametrize("username, password, status", [
    ("meera", "learn-123", 200),
    ("meera", "wrong", 401),
    ("nobody", "learn-123", 401),
], ids=["right-password", "wrong-password", "unknown-user"])
def test_login(client, username, password, status):
    response = client.post("/login", json={"username": username, "password": password})
    assert response.status_code == status


def test_enrol_needs_login(client):
    response = client.post("/enrolments", json={"course_id": 3})
    assert response.status_code == 401
    assert response.json()["error"] == "Log in first."


def test_enrol_takes_a_seat(meera):
    response = meera.post("/enrolments", json={"course_id": 3})
    assert response.status_code == 201
    assert response.json()["course_id"] == 3
    assert seats_left(meera, 3) == 29
