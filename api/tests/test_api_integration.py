import requests
import json

from snacks.db import Base, engine, Session
from snacks import properties


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

    # test that the max votes are remaining
    res = requests.get(
        "http://localhost:5050/vote",
        headers={"Authorization": "Bearer {}".format(body["data"]["token"])}
    )
    print(res.content.decode('utf-8'))
    assert res.ok
    assert res.json()["data"]["remaining_votes"] == properties.max_votes

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


def test_create_vote_on_snack():
    res = requests.post(
        "http://localhost:5050/login",
        data=json.dumps({"username": "integration_user", "password": "something"})
    )
    token = res.json()["data"]["token"]

    # same snack from other tests
    res = requests.post(
        "http://localhost:5050/snacks",
        headers={"Authorization": "Bearer {}".format(token)},
        data=json.dumps({"name": "fruit by the foot", "location": "super america"})
    )

    #snack could already exist. If so, expect error message
    if res.status_code == 400:
        error = res.json()["error"]
        assert error == "{'message': 'The snack already exists.'}"

    else:
        assert res.status_code == 200

    # get snack id
    res = requests.get(
        "http://localhost:5050/snacks",
        headers={"Authorization": "Bearer {}".format(token)}
    )
    snacks = res.json()["data"]

    fruit_snacks = [x for x in snacks["suggestedCurrent"] if x["name"] == "fruit by the foot"][0]
    # vote for the snack
    # consume allowed votes
    for i in range(properties.max_votes):
        res = requests.post(
            "http://localhost:5050/vote",
            headers={"Authorization": "Bearer {}".format(token)},
            data=json.dumps({"snack_id": fruit_snacks["id"]})
        )
        assert res.ok
        remaining_votes = res.json()["data"]["remaining_votes"]
    # hit max votes
    bad_res = requests.post(
        "http://localhost:5050/vote",
        headers={"Authorization": "Bearer {}".format(token)},
        data=json.dumps({"snack_id": fruit_snacks["id"]})
    )
    body = bad_res.json()
    print(body)
    assert bad_res.status_code == 400
    error = body["error"]
    assert error == "Maximum votes for period exceeded"


def test_suggestions_limited():
    res = requests.post(
        "http://localhost:5050/login",
        data=json.dumps({"username": "integration_user", "password": "something"})
    )
    token = res.json()["data"]["token"]

    # user has already suggested snack, should err
    res = requests.post(
        "http://localhost:5050/snacks",
        headers={"Authorization": "Bearer {}".format(token)},
        data=json.dumps({"name": "fruit by the foot", "location": "super america"})
    )

    response = res.json()

    assert response["error"] == "can only suggest one snack per month"
