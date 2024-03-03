from flask import jsonify
from ratelimit import limits, RateLimitException


@limits(calls=100, period=60)
def rate_limit(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RateLimitException as e:
            return jsonify({"success": False, "message": "Too many requests, please try again later"}), 429
    return wrapper
