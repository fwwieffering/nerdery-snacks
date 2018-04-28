import requests
import json
import datetime
from sqlalchemy import func

from snacks import properties
from snacks.errors import (
    AuthorizationError, ApiNotAvailableException, BadRequestError
    )
from snacks.db import Session
from snacks.models.vote import Vote
from snacks.models.snacks import Snack


def get_snacks_remote() -> dict:
    """
    Returns map of snack_id -> snack

    Raises:
    - ApiNotAvailableException if snacks API is down
    - AuthorizationError if request to snacks API fails
    """
    res: requests.Response = requests.get(
        properties.snacks_api_url,
        headers={
            "Authorization": "ApiKey {}".format(properties.snacks_api_key)
        }
    )
    # check for auth errors
    if res.status_code == 401:
        raise AuthorizationError(
            json.dumps({"error": "Unable to authorize to snacks api"}))

    # check for service being down
    if res.status_code >= 500:
        raise ApiNotAvailableException

    snax: list = res.json()

    final_snacks: dict = {x["id"]: x for x in snax}

    return final_snacks


def get_snacks() -> list:
    """
    combines snacks from snack API with vote numbers

    Raises:
    - ApiNotAvailableException if snacks API is down
    - AuthorizationError if request to snacks API fails
    """
    snax: dict = get_snacks_remote()
    final_snacks: list = []

    # collect snack ids to query votes for
    snack_ids: list = snax.keys()
    # collect votes
    session = Session()
    rows = session.query(Vote.snack_id, func.count(Vote.id))\
        .filter(Vote.snack_id.in_(snack_ids))\
        .filter(datetime.datetime.now() < Vote.vote_expiry)\
        .group_by(Vote.snack_id)

    # add votes to snack objects
    for snack_id, count in rows:
        snack = snax[snack_id]
        snack["votes"] = count

        # remove from dictionary so it isn't double added
        del snax[snack_id]
        final_snacks.append(Snack(**snack))

    # add remaining snax (no votes) to final
    for k, v in snax.items():
        final_snacks.append(Snack(**v))

    return final_snacks


def add_snack(name: str, location: str) -> Snack:
    """
    Sends in a snack suggestion, and returns the Snack object.
    Note:
        - create snack api supports latitude and longitude parameters but they
        aren't anywhere in the output so I'm not including the input

    Raises:
        - AuthorizationError if request to snacks API fails
        - BadRequestError if the snack already exists

    """
    res: requests.Response = requests.post(
        properties.snacks_api_url,
        headers={
            "Authorization": "ApiKey {}".format(properties.snacks_api_key),
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "name": name,
            "location": location
        })
    )
    # check for auth errors
    if res.status_code == 401:
        raise AuthorizationError(
            {"error": "Unable to authorize to snacks api"}
        )

    # check for conflicts
    if res.status_code in [409, 401]:
        raise BadRequestError(res.json())

    return Snack(**res.json())
