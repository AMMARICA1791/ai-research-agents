ALLOWED = {"read_page": {"url"}, "summarize": {"text"}}
def validate(action):
    if not isinstance(action, dict) or set(action) != {"type", "params"}:
        return False
    kind, params = action["type"], action["params"]
    return kind in ALLOWED and isinstance(params, dict) and set(params) == ALLOWED[kind] and all(isinstance(v, str) and bool(v.strip()) for v in params.values())
