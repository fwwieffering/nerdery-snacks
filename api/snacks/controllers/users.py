from sqlalchemy.exc import IntegrityError
import datetime

from snacks.errors import UserAlreadyExistsException, UserNotFoundException
from snacks.db import Session
from snacks.models.users import User
from snacks.models.vote import Vote


def create_user(username: str, password: str) -> User:
    """
    adds user to database

    :param username: str username
    :param password: str password
    :return: User
    """
    session = Session()
    # TODO: hash password
    new_user: User = User(username=username, password_hash=password)
    # TODO: handle generic sql errors
    try:
        session.add(new_user)
        session.commit()
        # gets id
        session.refresh(new_user)
        session.close()
        return new_user
    except IntegrityError as e:
        session.rollback()
        session.close()
        raise UserAlreadyExistsException


def verify_user_password(username: str, password: str) -> bool:
    """
    verifies whether the user password is correct

    raises:
        - UserNotFoundException if user does not exist

    returns:
        - bool of whether pw is valid
    """
    session = Session()
    user: User = session.query(User).filter(User.username == username).first()

    # TODO: hash password
    if user and user.password_hash == password:
        session.refresh(user)
        return user.id

    session.close()

    if not user:
        raise UserNotFoundException

    return False


def get_user_by_id(user_id: int) -> User:
    """
    Looks up user by id.

    Raises:
        - UserNotFoundException if user id does not exist

    Returns:
        User
    """
    session = Session()

    # verify user_id exists
    vote_user: User = session.query(User).filter(User.id == user_id).first()
    session.close()

    if not vote_user:
        raise UserNotFoundException

    return vote_user


def get_user_votes(user_id: int) -> int:
    """
    Gets the number of votes for the user in the current time period

    Raises:
        - UserNotFoundException if user id does not exist

    Returns:
        - int: count of votes
    """
    session = Session()

    # get user by id to ensure user exists
    get_user_by_id(user_id)
    # count votes for the user that haven't expired
    user_votes: int = session.query(Vote)\
        .filter(Vote.user_id == user_id)\
        .filter(Vote.vote_expiry > datetime.datetime.now()).count()

    session.close()

    return user_votes
