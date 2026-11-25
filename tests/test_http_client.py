from unittest.mock import MagicMock

import pytest
import requests

from src.http_client import ApiClient


def _resp(json_data, status=200):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_data
    r.raise_for_status.side_effect = None if status < 400 else requests.HTTPError(f"{status}")
    return r


def test_get_json_success():
    c = ApiClient("https://x.test")
    c.session.request = MagicMock(return_value=_resp({"ok": True}))
    assert c.get_json("a") == {"ok": True}
    assert c.session.request.call_args.kwargs["timeout"] == 10  # timeout always set


def test_http_error_raises():
    c = ApiClient("https://x.test")
    c.session.request = MagicMock(return_value=_resp({}, status=404))
    with pytest.raises(requests.HTTPError):
        c.get_json("missing")


def test_paginate_stops_on_empty_page():
    c = ApiClient("https://x.test")
    c.session.request = MagicMock(side_effect=[_resp([1, 2]), _resp([3]), _resp([])])
    assert list(c.paginate("items")) == [1, 2, 3]
