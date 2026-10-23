def evaluate(value):
    return isinstance(value, dict) and value.get("explicit_approval") is True and value.get("trusted_origin") == "user"
