from config import settings
import jwt
from datetime import datetime, timedelta


def jwt_encode(email):
    """
       param: payload - String to be encoded.
       return: Encoded string

       This function encodes given string using the SECRET_KEY.
       """
    return jwt.encode({"exp": datetime.now() + timedelta(minutes=2), "payload": email}, key=settings.SECRET_KEY)


def jwt_decode(email):
    """
    param: email
    return: Decoded data

    This function decodes the given payload using SECRET_KEY and algorithm.
    """
    return jwt.decode(email, key=settings.SECRET_KEY, algorithms=['HS256'])
