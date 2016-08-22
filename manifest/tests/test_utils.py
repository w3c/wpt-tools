import pytest

from ..utils import is_blacklisted


@pytest.mark.parametrize("url", [
    "/foo",
    "/tools/foo",
    "/common/foo",
    "/conformance-checkers/foo",
    "/_certs/foo",
    "/css21/archive/foo",
    "/work-in-progress/foo",
    "/resources/foo",
    "/support/foo",
    "/foo/resources/bar",
    "/foo/support/bar"
])
def test_is_blacklisted(url):
    assert is_blacklisted(url) is True


@pytest.mark.parametrize("url", [
    "/foo/tools/bar",
    "/foo/common/bar",
    "/foo/conformance-checkers/bar",
    "/foo/_certs/bar",
    "/foo/css21/archive/bar",
    "/foo/work-in-progress/bar"
])
def test_not_is_blacklisted(url):
    assert is_blacklisted(url) is False
