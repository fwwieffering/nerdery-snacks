import requests
import json
import datetime
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError

from snacks import properties
from snacks.utils import get_next_month
from snacks.errors import (
    AuthorizationError, ApiNotAvailableException, BadRequestError
    )
from snacks.db import Session
from snacks.models.vote import Vote
from snacks.models.snacks import Snack


def get_snacks_remote() -> dict:
    """
    Fetches snacks from snack service and adds to snack table
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
    final_snacks: dict = {}

    for snack in snax:
        new_snack = Snack(**snack)
        # add snacks to db.
        session = Session()
        new_snack = session.merge(new_snack)
        session.commit()
        session.refresh(new_snack)
        session.close()
        final_snacks[new_snack.id] = new_snack

    session.close()

    return final_snacks


def get_snack_remote_by_name(name: str) -> Snack:
    """
    Calls snack api and returns snack object if its name matches name
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

    named_snack = [x for x in res.json() if x["name"].lower() == name.lower()]

    if len(named_snack) > 0:
        return Snack(**named_snack[0])
    else:
        return None


def get_snacks() -> dict:
    """
    combines snacks from snack API with vote numbers. Sorts into map
    of three lists:
        - permanent: snacks that are always ordered
        - suggestedCurrent: snacks that are suggested for the current month
        - suggestedExpired: snacks whose suggestions have expired

    Raises:
    - ApiNotAvailableException if snacks API is down
    - AuthorizationError if request to snacks API fails
    """
    snax: dict = get_snacks_remote()
    snacks_permanent: list = []
    snacks_suggested_valid: list = []
    snacks_suggested_expired: list = []

    final_snacks = {
        "permanent": snacks_permanent,
        "suggestedCurrent": snacks_suggested_valid,
        "suggestedExpired": snacks_suggested_expired
    }

    # collect snack ids to query votes for
    snack_ids: list = snax.keys()
    # collect votes
    session = Session()
    rows = session.query(Vote.snack_id, func.count(Vote.id))\
        .filter(Vote.snack_id.in_(snack_ids))\
        .filter(datetime.datetime.now() < Vote.vote_expiry)\
        .group_by(Vote.snack_id)

    session.close()
    # add votes to snack objects
    for snack_id, count in rows:
        snack = snax[snack_id].to_dict()

        snack["votes"] = count

        if snack["suggestionExpiry"] > datetime.datetime.now():
            snacks_suggested_valid.append(snack)
        else:
            snacks_suggested_expired.append(snack)

        # remove from dictionary so it isn't double added
        del snax[snack_id]

    # add remaining snax (no votes) to final
    for k, v in snax.items():
        if v.optional:
            if v.suggestionExpiry  and v.suggestionExpiry > datetime.datetime.now():
                snacks_suggested_valid.append(v.to_dict())
            else:
                snacks_suggested_expired.append(v.to_dict())
        else:
            snacks_permanent.append(v.to_dict())

    return final_snacks


def add_snack(name: str, location: str) -> Snack:
    """
    Sends in a snack suggestion, to snack service
    Adds to snacks table if successful.
    returns the Snack object.
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
    elif res.status_code  == 401:
        raise BadRequestError(res.json())

    # check for service being down
    elif res.status_code >= 500:
        raise ApiNotAvailableException

    # 409 is returned when snack already exists. However, I still want to update
    # the suggestionExpiry if its null or not the current month
    elif res.status_code == 409:
        session = Session()
        currentSnack = session.query(
                Snack
            ).filter(Snack.name == name
            ).filter(Snack.suggestionExpiry > datetime.datetime.now()).first()

        # snack exists in db with a valid suggestion month, it has already been
        # suggested
        if currentSnack:
            raise BadRequestError(res.json())

        # snack exists in snack api but does not have a valid suggestion month
        # in db. Add suggestion month to db if optional snack. Otherwise raise
        # error
        else:
            extant_snack = get_snack_remote_by_name(name)
            if extant_snack.optional:
                extant_snack.suggestionExpiry = get_next_month()
                session.merge(extant_snack)
                session.commit()
                return extant_snack
            else:
                raise BadRequestError(
                    "Cannot suggest a snack that is always purchased")

    else:
        # add to db
        session = Session()

        new_snack = Snack(**res.json())
        new_snack.suggestionExpiry = get_next_month()

        session.merge(new_snack)
        session.commit()
        session.close()

        return new_snack
