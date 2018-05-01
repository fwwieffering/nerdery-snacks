from snacks.errors import VotesExceededException
from snacks.db import Session
from snacks.models.vote import Vote
from snacks.properties import max_votes, vote_expiration
from snacks.controllers import users


def add_vote(user_id: int, snack_id: int) -> int:
    """
    Adds a vote for the snack by the user

    raises:
        - VotesExceededException if the user has exceeded allotted votes
        - UserNotFoundException if the user_id is not found

    returns:
        - vote_count int
    """

    # count votes for the user that haven't expired
    user_votes: int = users.get_user_votes(user_id)

    if user_votes >= max_votes:
        raise VotesExceededException

    # create new vote
    new_vote = Vote(
        user_id=user_id,
        snack_id=snack_id,
        vote_expiry=vote_expiration()
    )

    session = Session()

    session.add(new_vote)
    session.commit()
    session.close()

    return user_votes + 1
