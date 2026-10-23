"""Offline reference authorization gate; never executes actions."""
from dataclasses import dataclass
from typing import FrozenSet

CONSEQUENTIAL = frozenset({"post", "delete", "transfer", "purchase", "send", "write"})
KNOWN = CONSEQUENTIAL | {"read", "search"}

@dataclass(frozen=True)
class Request:
    action: str
    origin: str
    target: str
    authorized_actions: FrozenSet[str]
    authorized_targets: FrozenSet[str]
    explicit_approval: bool = False

def decide(req: Request) -> str:
    """Return ALLOW, DENY, or REVIEW. Fail closed on unknown actions."""
    if req.action not in KNOWN:
        return "DENY"
    if req.origin != "user":
        return "DENY"
    if req.action not in req.authorized_actions or req.target not in req.authorized_targets:
        return "DENY"
    if req.action in CONSEQUENTIAL and not req.explicit_approval:
        return "REVIEW"
    return "ALLOW"
