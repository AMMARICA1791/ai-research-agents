import re
PATTERNS = [re.compile(r"(?i)(?:api[_-]?key|token|secret)[ ]*[:=][ ]*[A-Za-z0-9_-]{8,}"), re.compile(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}")]
def redact(text):
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    for pattern in PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text
