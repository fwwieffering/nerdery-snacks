from sqlalchemy import Column, Integer, String, DateTime, Boolean

from snacks.db import Base


class Snack(Base):
    """
    Snacks model. Deserialized from JSON object of format
    {
        "id":1000,
        "name":"Ramen",
        "optional":false,
        "purchaseLocations":"Whole Foods",
        "purchaseCount":1,
        "lastPurchaseDate":"3/22/2018"
    }

    Its dumb that I'm storing the entire thing in the DB but there are
    a couple values not provided by the snack service and easier to
    just store the whole snack
    """
    __tablename__ = 'snacks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    optional = Column(Boolean)
    purchaseLocations = Column(String)
    purchaseCount = Column(Integer)
    lastPurchaseDate = Column(String)
    # not provided by snack service. Suggestions only valid
    # for the current month
    suggestionExpiry = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "optional": self.optional,
            "purchaseLocations": self.purchaseLocations,
            "purchaseCount": self.purchaseCount,
            "lastPurchaseDate": self.lastPurchaseDate,
            "suggestionExpiry": self.suggestionExpiry
        }
