from sqlalchemy import Column, Integer, ForeignKey, DateTime

from snacks.db import Base


class Vote(Base):
    """
    Votes for snacks.

    Columns:
        - user_id: int. ID on the users table
        - snack_id: ID of suggested snack. Retrieved from snack api
        - vote_expiry: Datetime when the vote is no longer valid
    """

    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    # snacks are stored in the snack api, otherwise this would be a ForeignKey
    snack_id = Column(Integer)
    vote_expiry = Column(DateTime)
