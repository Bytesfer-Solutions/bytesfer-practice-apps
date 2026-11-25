# fake_api for your own computer: the same names as the workspace's fake_api, but every call is a
# real HTTP request made with the requests library to the practice API started by serve.py.
# So the test files from "API Testing with Python" run here unchanged.
import os

import requests

BASE_URL = os.environ.get("PRACTICE_API_URL", "http://127.0.0.1:8000")
HTTPError = requests.HTTPError


class Session(requests.Session):
    # Like the workspace: each new Session starts the practice API from its starting data.
    def __init__(self):
        super().__init__()
        super().request("POST", BASE_URL + "/reset").raise_for_status()

    def request(self, method, url, *args, **kwargs):
        if url.startswith("/"):
            url = BASE_URL + url
        return super().request(method, url, *args, **kwargs)


def check_schema(data, schema, where="body"):
    # Returns a list of problems ([] means the data matches). A schema is a type such as int or str,
    # a tuple of types, {key: schema} for an object (all keys required, no extras), or [schema] for a list.
    if isinstance(schema, dict):
        if not isinstance(data, dict):
            return [f"{where}: expected an object, got {_name(type(data))}"]
        problems = []
        for key in schema:
            if key in data:
                problems += check_schema(data[key], schema[key], f"{where}.{key}")
            else:
                problems.append(f"{where}: missing key '{key}'")
        for key in data:
            if key not in schema:
                problems.append(f"{where}: unexpected key '{key}'")
        return problems
    if isinstance(schema, list):
        if not isinstance(data, list):
            return [f"{where}: expected a list, got {_name(type(data))}"]
        problems = []
        for i, item in enumerate(data):
            problems += check_schema(item, schema[0], f"{where}[{i}]")
        return problems
    types = schema if isinstance(schema, tuple) else (schema,)
    if isinstance(data, types) and not (isinstance(data, bool) and bool not in types):
        return []
    return [f"{where}: expected {' or '.join(_name(t) for t in types)}, got {_name(type(data))}"]


def _name(t):
    return {type(None): "null", dict: "object", list: "list"}.get(t, t.__name__)
