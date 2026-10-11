"""Known real-repository issue: GitHub host spoofing, with independent gates."""
from pathlib import Path

import pytest

from lab.real_repo_repair import (
    TARGET, SAFE_PATTERN, REGRESSION,
    _check_source, build_candidate,
)

ROOT = Path(__file__).resolve().parents[1]


def test_existing_real_repo_defect_is_red_and_targeted_patch_is_green():
    before = (ROOT / TARGET).read_text(encoding="utf-8")
    # This assertion is not a regression test on main: it proves the
    # vulnerability exists at baseline and the bounded checker detects it.
    # After a PR fixes web/app.py, the branch CI should switch to verifying
    # the generated candidate; this research test remains tied to baseline.
    if "re.search(r\"github" not in before:
        pytest.skip("The host-spoofing target has already been repaired")
    assert _check_source(before) is False
    after = build_candidate(before, f'match = re.match(r"{SAFE_PATTERN}", value)')
    assert _check_source(after) is True
    assert (ROOT / TARGET).read_text(encoding="utf-8") == before
    assert after != before


@pytest.mark.parametrize("line", [
    'match = re.search(r"github\\.com/([^/]+)/([^/]+)", value)',
    'match = re.match(r"^https://evilgithub.com/([^/]+)/([^/]+)", value)',
    'match = re.match(r"^https://github.com/([^/]+)/([^/]+)", value)',
    'match = eval("insecure")',
    'match = re.match(r"^https://github\\.com/([^/]+)/([^/]+)", value); open("x", "w")',
])
def test_unsafe_model_changes_fail_closed(line):
    before = (ROOT / TARGET).read_text(encoding="utf-8")
    if "re.search(r\"github" not in before:
        pytest.skip("Target already repaired")
    with pytest.raises((ValueError, SyntaxError)):
        build_candidate(before, line)


def test_trusted_regression_covers_spoof_hosts_and_good_urls():
    assert "evilgithub.com" in REGRESSION
    assert "github.com.evil.org" in REGRESSION
    assert "https://github.com/demo/sample" in REGRESSION
