"""Regression tests: only canonical HTTPS GitHub URLs may be parsed."""
import pytest
from web.app import _parse_github_url

@pytest.mark.parametrize("url,expected", [
    ("https://github.com/demo/sample", {"owner":"demo","repo":"sample"}),
    ("https://github.com/demo/sample.git", {"owner":"demo","repo":"sample"}),
    ("https://github.com/demo/sample?ref=main", {"owner":"demo","repo":"sample"}),
])
def test_valid_github_urls(url, expected):
    assert _parse_github_url(url) == expected

@pytest.mark.parametrize("url", [
    "https://evilgithub.com/demo/sample",
    "https://example.org/x/github.com/demo/sample",
    "https://github.com.evil.org/demo/sample",
    "https://github.com@evil.org/demo/sample",
    "http://github.com/demo/sample",
])
def test_reject_noncanonical_host_or_scheme(url):
    with pytest.raises(ValueError):
        _parse_github_url(url)
