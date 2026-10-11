"""Preserve the historical attack as a controlled regression fixture.

Never skip tests merely because the real GitHub URL parser has been fixed.
"""
from pathlib import Path

import pytest

from lab.real_repo_repair import TARGET, SAFE_PATTERN, REGRESSION, _check_source, build_candidate

ROOT = Path(__file__).resolve().parents[1]
SAFE_LINE = "match = re.match(r'^https://github\\.com/([^/]+)/([^/]+)', value)"
HISTORICAL_LINE = 'match = re.search(r"github\\.com/([^/]+)/([^/]+)", value)'


@pytest.fixture
def historical_vulnerable_source():
    repaired = (ROOT / TARGET).read_text(encoding="utf-8")
    assert SAFE_LINE in repaired, "The production GitHub host fix has regressed"
    assert HISTORICAL_LINE not in repaired, "Unsafe search reintroduced in production"
    return repaired.replace(SAFE_LINE, HISTORICAL_LINE, 1)


def test_real_source_is_safe_and_original_attack_remains_reproducible(historical_vulnerable_source):
    actual = (ROOT / TARGET).read_text(encoding="utf-8")
    assert _check_source(actual) is True
    assert _check_source(historical_vulnerable_source) is False
    patch = build_candidate(
        historical_vulnerable_source,
        f'match = re.match(r"{SAFE_PATTERN}", value)',
    )
    assert _check_source(patch) is True
    assert patch != historical_vulnerable_source


@pytest.mark.parametrize("line", [
    'match = re.search(r"github\\.com/([^/]+)/([^/]+)", value)',
    'match = re.match(r"^https://evilgithub.com/([^/]+)/([^/]+)", value)',
    'match = re.match(r"^https://github.com/([^/]+)/([^/]+)", value)',
    'match = eval("insecure")',
    'match = re.match(r"^https://github\\.com/([^/]+)/([^/]+)", value); open("x", "w")',
])
def test_unsafe_model_changes_fail_closed(historical_vulnerable_source, line):
    with pytest.raises((ValueError, SyntaxError)):
        build_candidate(historical_vulnerable_source, line)


def test_trusted_regression_covers_spoof_hosts_and_good_urls():
    assert "evilgithub.com" in REGRESSION
    assert "github.com.evil.org" in REGRESSION
    assert "https://github.com/demo/sample" in REGRESSION
