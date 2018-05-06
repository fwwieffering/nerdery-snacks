import falcon
import json

from snacks.controllers.users import (
    create_user,
    verify_user_password,
    get_user_votes,
    check_user_suggestion,
    set_user_suggestion
)
from snacks.controllers.snacks import get_snacks, add_snack
from snacks.controllers.votes import add_vote
from snacks.models.snacks import Snack
from snacks.errors import (
    UserAlreadyExistsException,
    BadRequestError,
    AuthorizationError,
    UserNotFoundException,
    ApiNotAvailableException,
    VotesExceededException
)
from snacks import properties, DateTimeEncoder
from snacks.auth import validate_token, generate_token


class CORSMiddleware(object):
    """
    adds cors headers so this api can be accessed from a browser
    """
    def process_resource(self, req, resp, resource, params):
        resp.append_header(
            name="Access-Control-Allow-Origin",
            value="*"
        )
        resp.append_header(
            name="Access-Control-Allow-Headers",
            value="authorization,content-type"
        )


class AuthMiddleware(object):
    """
    Checks if JWT bearer token is valid
    """
    blacklist_auth = [
        "/users",
        "/login"
    ]

    def process_resource(self, req, resp, resource, params):
        if req.path not in self.blacklist_auth and req.method != "OPTIONS":
            if req.auth:
                token = req.auth.split("Bearer ")[-1]
                valid = validate_token(token)

                if not valid:
                    raise falcon.HTTPForbidden({
                        "status": "error",
                        "error": "Invalid bearer token"
                    })

            else:
                raise falcon.HTTPUnauthorized(json.dumps({
                    "status": "error",
                    "error": "Authorization header missing"
                }))


class UserResource(object):
    """
    Handles creation of users
    """

    def on_post(self, req, resp):
        """
        Creates user
        """
        user = req.media

        if not user or (not user.get("username") or not user.get("password")):
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                "status": "error",
                "error": "must provide 'username' and 'password' in json body"
            })
            return

        try:
            create_user(user["username"], user["password"])
            resp.body = json.dumps({"status": "ok"})

        except UserAlreadyExistsException:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                "status": "error",
                "error": "user {} already exists".format(user["username"])
            })


class LoginResource(object):
    """
    Handles verifying password. Returns JWT for auth
    """

    def on_post(self, req, resp):
        """
        Validates PW and returns JWT
        """
        user = req.media

        if not user or (not user.get("username") or not user.get("password")):
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                "status": "error",
                "error": "must provide 'username' and 'password' in json body"
            })
            return

        try:
            valid = verify_user_password(user["username"], user["password"])

            if not valid:
                resp.status = falcon.HTTP_401
                resp.body = json.dumps({
                    "status": "error",
                    "error": "invalid password"
                })
                return

            token = generate_token(valid)
            resp.body = json.dumps({"status": "ok", "data": {"token": token}})

        except UserNotFoundException:
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({
                "status": "error",
                "error": "user: {} does not exist".format(user["username"])
            })


class SnacksResource(object):
    """
    Handles creation and retrieval of snacks
    """

    def on_get(self, req, resp):
        """
        Retrieves list of snacks
        """
        try:
            snacks = get_snacks()
            resp.body = json.dumps({
                "status": "ok",
                "data": snacks
            }, cls=DateTimeEncoder)
        except ApiNotAvailableException:
            resp.status = falcon.HTTP_503
            resp.body = json.dumps({
                "status": "error",
                "error": "Snacks API is unavailable. Try again later"
            })

        except AuthorizationError:
            resp.status = falcon.HTTP_503
            resp.body = json.dumps({
                "status": "error",
                "error": [
                    "Cannot authenticate with snacks API."
                    "API key may have expired"
                ]
            })

    def on_post(self, req, resp):
        """
        Creates new snack if user has not already suggested a snack
        """
        snack = req.media
        token = req.auth.split("Bearer ")[-1]

        if not snack or (not snack.get("name") or not snack.get("location")):
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                "status": "error",
                "error": "json body containing 'name' and 'location' required"
            })
            return

        try:
            user_info = validate_token(token)
            can_suggest = check_user_suggestion(user_info["userid"])

            if can_suggest:
                # set snack expiration
                set_user_suggestion(user_info["userid"])
                new_snack: Snack = add_snack(snack["name"], snack["location"])
                resp.body = json.dumps({
                    "status": "ok",
                    "data": new_snack.to_dict()
                }, cls=DateTimeEncoder)

            else:
                resp.body = json.dumps({
                    "status": "error",
                    "error": "can only suggest one snack per month"
                })
                resp.status = falcon.HTTP_400

        except AuthorizationError:
            resp.status = falcon.HTTP_503
            resp.body = json.dumps({
                "status": "error",
                "error": [
                    "Cannot authenticate with snacks API."
                    "API key may have expired"
                ]
            })

        except BadRequestError as e:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                "status": "error",
                "error": str(e)
            })

        except UserNotFoundException:
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({
                "status": "error",
                "error": "token not tied to user"
            })

class VoteResource(object):
    """
    Handles addition of votes
    """

    def on_get(self, req, resp):
        """
        returns remaining votes for user
        """
        token = req.auth.split("Bearer ")[-1]
        try:
            user_info = validate_token(token)
            total_votes = get_user_votes(user_info["userid"])
            remaining_votes = properties.max_votes - total_votes

            resp.body = json.dumps({
                "status": "ok",
                "data": {"remaining_votes": remaining_votes}
            })
        except UserNotFoundException:
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({
                "status": "error",
                "error": "token not tied to user"
            })

    def on_post(self, req, resp):
        """
        creates vote
        """
        vote = req.media

        if not vote or not vote.get("snack_id"):
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                "status": "error",
                "error": "json body containing 'snack_id' is required"
            })

        try:
            # get user id from token
            token = req.auth.split("Bearer ")[-1]
            user_info = validate_token(token)

            total_votes = add_vote(user_info["userid"], vote["snack_id"])
            remaining_votes = properties.max_votes - total_votes

            resp.body = json.dumps({
                "status": "ok",
                "data": {
                    "remaining_votes": remaining_votes
                }
            })

        except UserNotFoundException:
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({
                "status": "error",
                "error": "token not tied to user"
            })

        except VotesExceededException:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({
                "status": "error",
                "error": "Maximum votes for period exceeded"
            })


class UpPageResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"status": "ok"})


app = falcon.API(middleware=[
    CORSMiddleware(),
    AuthMiddleware()
])

app.add_route("/users", UserResource())
app.add_route("/login", LoginResource())
app.add_route("/snacks", SnacksResource())
app.add_route("/vote", VoteResource())
