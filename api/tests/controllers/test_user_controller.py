from snacks.db import Session, Base, engine
from snacks.controllers.users import create_user, verify_user_password, get_user_votes, check_user_suggestion, set_user_suggestion
from snacks.models.users import User
from snacks.errors import UserAlreadyExistsException, UserNotFoundException

import pytest


def setup_function():
    """
    Delete database tables then recreate
    """
    # tear down dbs if they exist
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())

    # recreate
    Base.metadata.create_all(engine)


def test_create_user():
    create_user('test_user', 'test_password')

    session = Session()

    test_user = session.query(User).filter(User.username == 'test_user').first()

    assert test_user


def test_create_user_already_exists():
    with pytest.raises(UserAlreadyExistsException):
        create_user('test_user', 'test_password')
        create_user('test_user', 'test_password')


def test_verify_password():
    create_user('test_user', 'test_password')
    # correct pw should be true
    res = verify_user_password('test_user', 'test_password')
    assert res
    # incorrect pw should be false
    res = verify_user_password('test_user', 'wrong password')
    assert res == False
    # nonexistent user should raise exception
    with pytest.raises(UserNotFoundException):
        verify_user_password('fake_user', 'some password')


def test_get_user_votes():
    # when no user should raise exception
    with pytest.raises(UserNotFoundException):
        get_user_votes(1)

    user = create_user('test_user', 'test_password')

    vote_count = get_user_votes(user.id)
    # should be 0 since no votes added
    assert vote_count == 0


def test_user_suggestion():
    user = create_user('test_user', 'test_password')

    can_suggest = check_user_suggestion(user.id)

    assert can_suggest

    set_user_suggestion(user.id)

    cannot_suggest = check_user_suggestion(user.id)

    assert cannot_suggest == False
