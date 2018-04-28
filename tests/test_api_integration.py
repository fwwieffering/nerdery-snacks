import requests
import json

from snacks.db import Base, engine, Session


def setup_module():
    """
    Delete database tables then recreate
    """
    # tear down dbs if they exist
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())

    # recreate
    Base.metadata.create_all(engine)


def test_create_user_integration():
    res = requests.post(
        "http://localhost:5050/users",
        data=json.dumps({"username": "integration_user", "password": "something"})
    )

    print(res.content.decode('utf-8'))
    body = res.json()
    assert res.ok
    assert body["status"] == "ok"


def test_login_integration():
    res = requests.post(
        "http://localhost:5050/login",
        data=json.dumps({"username": "integration_user", "password": "something"})
    )

    body = res.json()
    assert res.ok
    assert body["data"]["token"]

    # try incorrect password
    res = requests.post(
        "http://localhost:5050/login",
        data=json.dumps({"username": "integration_user", "password": "bad password"})
    )

    body = res.json()
    assert res.status_code == 401
    assert body["error"] == "invalid password"

    # try bad user
    # try incorrect password
    res = requests.post(
        "http://localhost:5050/login",
        data=json.dumps({"username": "bad user", "password": "bad password"})
    )

    body = res.json()
    assert res.status_code == 401
    assert body["error"] == "user: bad user does not exist"
