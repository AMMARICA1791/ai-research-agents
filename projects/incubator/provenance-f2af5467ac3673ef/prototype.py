import hashlib
def snapshot(text, quotation):
    if not isinstance(text, str) or not isinstance(quotation, str):
        raise ValueError("text and quotation must be strings")
    return {"sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "quote_present": bool(quotation) and quotation in text}
def drift(previous, text, quotation):
    current = snapshot(text, quotation)
    return {"content_changed": current["sha256"] != previous["sha256"], "quote_disappeared": bool(previous["quote_present"]) and not current["quote_present"]}
