"""Independent AI R&D laboratory.

Keep standard-library tools importable without optional HTTP/model clients.
LabOrchestrator is lazy-loaded to retain the public import API.
"""
from __future__ import annotations

__all__ = ["LabOrchestrator"]


def __getattr__(name: str):
    if name == "LabOrchestrator":
        from .pipeline import LabOrchestrator
        return LabOrchestrator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
