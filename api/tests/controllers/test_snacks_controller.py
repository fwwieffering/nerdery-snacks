from snacks.controllers.snacks import get_snacks_remote, get_snacks, add_snack
from snacks.errors import AuthorizationError, ApiNotAvailableException, BadRequestError
from snacks.controllers.votes import add_vote
from snacks.controllers.users import create_user
from snacks.db import Base, engine, Session

import pytest
from mock import patch, MagicMock


def setup_function():
    """
    Delete database tables then recreate
    """
    # tear down dbs if they exist
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())

    # recreate
    Base.metadata.create_all(engine)


def test_get_snacks_remote():
    with patch('requests.get') as fake_requests:
        # test auth error
        response = MagicMock()
        fake_requests.return_value = response

        response.status_code = 401

        with pytest.raises(AuthorizationError):
            res = get_snacks_remote()

        # test 500 errors

        response.status_code = 500

        with pytest.raises(ApiNotAvailableException):
            res = get_snacks_remote()

    real_snax = get_snacks_remote()
    assert isinstance(real_snax, dict)


def test_create_snack():
    # can't delete snacks from the remote api. So, if this snack exists we're
    # operating under the assumption that it came from here
    try:
        add_snack("fruit by the foot", "super america")
    except BadRequestError:
        pass

    snacks = get_snacks()

    my_snack = [x for x in snacks["suggestedCurrent"] if x["name"] == "fruit by the foot" ]
    assert len(my_snack) > 0
    assert my_snack[0]["suggestionExpiry"]


def test_get_snacks_with_votes():
    snacks = get_snacks()
    assert isinstance(snacks, dict)
    total_snacks = len(snacks["permanent"]) + len(snacks["suggestedCurrent"]) + len(snacks["suggestedExpired"])


    user = create_user('me', 'me')

    snack_id = None
    if len(snacks["suggestedCurrent"]) > 0:
        snack_id = snacks["suggestedCurrent"]["id"]
    else:
        new_snack = add_snack("fruit by the foot", "super america")
        snack_id = new_snack.id

    add_vote(user.id, snack_id)
    new_snacks = get_snacks()
    new_total_snacks = len(snacks["permanent"]) + len(snacks["suggestedCurrent"]) + len(snacks["suggestedExpired"])
    # make sure length did not change
    assert new_total_snacks == total_snacks
    # make sure our snack id has a vote count of one
    voted_snack = [x for x in new_snacks["suggestedCurrent"] if x["id"] == snack_id][0]
    assert voted_snack["votes"] == 1
