import jwt
import datetime

from snacks import properties


def generate_token(user_id: int) -> str:
    """
    Generates a JWT with username encoded, encrypted with the secret key
    """
    expiration = datetime.datetime.now() + datetime.timedelta(days=7)
    encoded = jwt.encode(
        {
            "userid": user_id,
            "exp": expiration.timestamp()
        },
        properties.secret_key
    )
    return encoded.decode('utf-8')


def validate_token(token: str) -> bool:
    """
    Attempts to decode token.
    """
    try:
        decoded = jwt.decode(
            token,
            properties.secret_key,
        )
        return decoded
    except jwt.exceptions.ExpiredSignatureError:
        return False
    except jwt.exceptions.DecodeError:
        return False
