"""Minimal runnable proof-of-concept for an anticipated need."""
def evaluate(value):
    if not isinstance(value, dict):
        return False
    return bool(value.get("explicit_approval") is True and
                value.get("trusted_origin") == "user")
