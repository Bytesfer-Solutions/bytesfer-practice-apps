# Practice enrolment API (made up; course titles and fees are real)
USERS = {
    "meera": {"password": "learn-123", "token": "test-token-meera"},
    "arjun": {"password": "learn-456", "token": "test-token-arjun"},
}
COURSES = []
ENROLMENTS = []


def reset():
    COURSES.clear()
    COURSES.append({"id": 1, "title": "pytest for Testers", "fee": 999, "seats_left": 0})
    COURSES.append({"id": 2, "title": "API Testing with Python", "fee": 999, "seats_left": 1})
    COURSES.append({"id": 3, "title": "Python for Beginners", "fee": 0, "seats_left": 30})
    ENROLMENTS.clear()
    ENROLMENTS.append({"id": 1, "learner": "arjun", "course_id": 1})


def logged_in_learner(headers):
    for name in USERS:
        if headers.get("Authorization") == "Bearer " + USERS[name]["token"]:
            return name
    return None


def handle(method, path, query, body, headers):
    body = body or {}
    if method == "GET" and path == "/courses":
        return 200, COURSES
    if method == "POST" and path == "/login":
        user = USERS.get(body.get("username"))
        if user is None or user["password"] != body.get("password"):
            return 401, {"error": "Wrong username or password."}
        return 200, {"token": user["token"]}
    learner = logged_in_learner(headers)
    if learner is None:
        return 401, {"error": "Log in first."}
    if method == "GET" and path == "/enrolments":
        mine = []
        for enrolment in ENROLMENTS:
            if enrolment["learner"] == learner:
                mine.append(enrolment)
        return 200, mine
    if method == "POST" and path == "/enrolments":
        course = None
        for c in COURSES:
            if c["id"] == body.get("course_id"):
                course = c
        if course is None:
            return 404, {"error": "Course not found."}
        for enrolment in ENROLMENTS:
            if enrolment["learner"] == learner and enrolment["course_id"] == course["id"]:
                return 409, {"error": "Already enrolled in this course."}
        if course["seats_left"] <= 0:
            return 422, {"error": "This batch is full."}
        course["seats_left"] = course["seats_left"] - 1
        enrolment = {"id": ENROLMENTS[-1]["id"] + 1, "learner": learner, "course_id": course["id"]}
        ENROLMENTS.append(enrolment)
        return 201, enrolment
    if method == "DELETE" and path.startswith("/enrolments/"):
        for enrolment in ENROLMENTS:
            if path == f"/enrolments/{enrolment['id']}" and enrolment["learner"] == learner:
                ENROLMENTS.remove(enrolment)
                return 204, None
        return 404, {"error": "Enrolment not found."}
    return 404, {"error": "No such endpoint."}
