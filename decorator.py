import functools
import time

import jwt
from flask import request


def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Appel de {func.__name__} avec {args} et {kwargs}")
        res = func(*args, **kwargs)
        return res

    return wrapper


@log_decorator
def addition(a, b):
    return a + b


addition(3, 4)


def require_auth(func):
    def wrapper(user, *args, **kwargs):
        if not user.get("is_authenticated"):
            raise PermissionError("user ")
        return func(user, *args, **kwargs)

    return wrapper


@require_auth
def show_user(user):
    return "is authenticated"


show_user({"is_authenticated": True})


def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(args, kwargs)
        end = time.time()
        return res

    return wrapper


@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def verify_api_user(func):
    """
    Decorator to verify an API user is authenticated

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = identify_authenticated_user(request)

        if isinstance(user, ApiUser):
            return func(*args, **kwargs)
        raise Exception("Invalid token 403")

    return wrapper


def identify_authenticated_user(request):
    if "Authorization" not in request.headers:
        raise Exception("Authentication required 403")

    bearer_token = request.headers["Authorization"]
    if "Bearer " not in bearer_token:
        raise Exception("Malformed Bearer token 401")

    auth_type, token = bearer_token.split(None, 1)
    try:
        token_payload = jwt.decode(token, "local", algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise Exception("Expired token", 403, code="AUT_004")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token", 403, code="AUT_005")
    if token_payload["api"]:
        user = ApiUser(token_payload["sub"])

    return user


class ApiUser:
    def __init__(self, login):
        self.login = login

