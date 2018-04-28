from snacks.auth import generate_token, validate_token
from snacks import properties

import pytest
import jwt
import datetime


def test_round_trip_token():
    token = generate_token('test_user')
    print(token)
    decoded_token = validate_token(token)
    assert decoded_token == "test_user"


def test_bad_token():
    fake_token = 'plookjojijijjij'

    decoded_token = validate_token(fake_token)

    assert not decoded_token

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    expired_token = jwt.encode(
        {
            "username": "test_user",
            "exp": yesterday.timestamp()
        },
        properties.secret_key
        )

    decoded_token = validate_token(expired_token)

    assert not decoded_token
