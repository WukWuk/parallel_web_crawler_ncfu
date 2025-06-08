import pytest
from crawler.utils import is_valid_url, normalize_url

def test_is_valid_url():
    domain = "example.com"
    assert is_valid_url("http://example.com", domain)
    assert is_valid_url("https://example.com/path", domain)
    assert not is_valid_url("ftp://example.com", domain)
    assert not is_valid_url("http://other.com", domain)
    assert not is_valid_url("invalid-url", domain)

def test_normalize_url():
    base = "http://example.com/dir/"
    assert normalize_url(base, "page.html") == "http://example.com/dir/page.html"
    assert normalize_url(base, "/page.html") == "http://example.com/page.html"
    assert normalize_url(base, "http://example.com/other") == "http://example.com/other"
