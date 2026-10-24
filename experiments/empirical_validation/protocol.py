"""Pre-registered empirical experiment evaluation; never conflates code tests with evidence."""
import hashlib
import json
import math
from pathlib import Path

REQUIRED = ("claim", "metric", "expected_value", "tolerance", "data_sha256", "protocol_version")

def evaluate(protocol, measurements, data):
    """Evaluate frozen numeric measurements against a pre-registered target.

    Returns a bounded comparison, NOT an assertion of scientific truth.
    """
    if not isinstance(protocol, dict) or any(k not in protocol for k in REQUIRED):
        raise ValueError("incomplete preregistration")
    if not isinstance(data, bytes) or hashlib.sha256(data).hexdigest() != protocol["data_sha256"]:
        raise ValueError("data digest mismatch")
    target, tolerance = protocol["expected_value"], protocol["tolerance"]
    if isinstance(target, bool) or isinstance(tolerance, bool) or not all(
        isinstance(v, (int, float)) and math.isfinite(v) for v in (target, tolerance)
    ) or tolerance < 0:
        raise ValueError("invalid target or tolerance")
    if not isinstance(measurements, list) or len(measurements) < 3:
        raise ValueError("at least three independent measurements required")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in measurements):
        raise ValueError("invalid measurement")
    mean = sum(measurements) / len(measurements)
    return {
        "engineering_status": "MEASUREMENTS_VALIDATED",
        "empirical_comparison": "WITHIN_PREDECLARED_TOLERANCE" if abs(mean - target) <= tolerance else "OUTSIDE_PREDECLARED_TOLERANCE",
        "scientific_validation": "NOT_ESTABLISHED_BY_THIS_COMPARISON",
        "observed_mean": mean,
        "expected_value": target,
        "absolute_difference": abs(mean - target),
        "replicates": len(measurements),
        "data_sha256": protocol["data_sha256"],
        "protocol_version": protocol["protocol_version"],
    }

def evaluate_files(protocol_path, measurements_path, data_path):
    protocol = json.loads(Path(protocol_path).read_text(encoding="utf-8"))
    measurements = json.loads(Path(measurements_path).read_text(encoding="utf-8"))
    return evaluate(protocol, measurements, Path(data_path).read_bytes())
