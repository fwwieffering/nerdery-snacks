from snacks.db import Session, Base, engine
from snacks.controllers.users import get_user_votes, create_user
from snacks.controllers.votes import add_vote
from snacks.models.users import User
from snacks.models.vote import Vote
from snacks.properties import max_votes
from snacks.errors import VotesExceededException

import pytest
import datetime
from mock import patch


def setup_function():
    """
    Delete database tables then recreate
    """
    # tear down dbs if they exist
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())

    # recreate
    Base.metadata.create_all(engine)


def test_voting():
    my_user: User = create_user('test_user', 'test_password')
    vote_count: int = get_user_votes(my_user.id)
    assert vote_count == 0

    for i in range(max_votes):
        # add votes
        add_vote(my_user.id, 123)
        vote_count: int = get_user_votes(my_user.id)
        assert vote_count == i + 1

    with pytest.raises(VotesExceededException):
        add_vote(my_user.id, 123)


def test_vote_expire():
    my_user: User = create_user('test_user', 'test_password')
    vote_count: int = get_user_votes(my_user.id)
    assert vote_count == 0

    # add votes that expired before now
    session = Session()
    vote = Vote(
        user_id = my_user.id,
        snack_id = 234,
        vote_expiry = datetime.datetime.now() - datetime.timedelta(days=1)
    )
    # assert that the vote count is still 0 with expired votes
    vote_count: int = get_user_votes(my_user.id)
    assert vote_count == 0
