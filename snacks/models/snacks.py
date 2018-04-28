import json


class Snack(object):
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
    """

    def __init__(self, id: int, name: str, optional: bool,
                 purchaseLocations: str, purchaseCount: int,
                 lastPurchaseDate: str, votes: int = 0):
        self.id: int = id
        self.name: str = name
        self.optional: bool = optional
        self.purchaseLocations: str = purchaseLocations
        self.purchaseCount: int = purchaseCount
        self.lastPurchaseDate: str = lastPurchaseDate
        self.votes: int = votes

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "optional": self.optional,
            "purchaseLocations": self.purchaseLocations,
            "purchaseCount": self.purchaseCount,
            "lastPurchaseDate": self.lastPurchaseDate,
            "votes": self.votes
        }

    def __repr__(self):
        return json.dumps(self.__dict__())
