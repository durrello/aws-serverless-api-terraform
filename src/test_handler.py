"""Unit tests for the Lambda handler, with DynamoDB mocked so they run free + offline."""
import json
from unittest.mock import MagicMock, patch

import handler


def _event(method, path="/items", item_id=None, body=None):
    return {
        "rawPath": path,
        "requestContext": {"http": {"method": method}},
        "pathParameters": {"id": item_id} if item_id else None,
        "body": json.dumps(body) if body is not None else None,
    }


def test_list_items():
    table = MagicMock()
    table.scan.return_value = {"Items": [{"id": "1", "name": "a"}]}
    with patch.object(handler, "_table", return_value=table):
        resp = handler.handler(_event("GET"), None)
    assert resp["statusCode"] == 200
    assert json.loads(resp["body"])["items"][0]["name"] == "a"


def test_get_missing_item_404():
    table = MagicMock()
    table.get_item.return_value = {}
    with patch.object(handler, "_table", return_value=table):
        resp = handler.handler(_event("GET", item_id="nope"), None)
    assert resp["statusCode"] == 404


def test_create_item():
    table = MagicMock()
    with patch.object(handler, "_table", return_value=table):
        resp = handler.handler(_event("POST", body={"name": "widget"}), None)
    assert resp["statusCode"] == 201
    assert json.loads(resp["body"])["name"] == "widget"
    table.put_item.assert_called_once()


def test_delete_item():
    table = MagicMock()
    with patch.object(handler, "_table", return_value=table):
        resp = handler.handler(_event("DELETE", item_id="1"), None)
    assert resp["statusCode"] == 204
    table.delete_item.assert_called_once()


def test_method_not_allowed():
    table = MagicMock()
    with patch.object(handler, "_table", return_value=table):
        resp = handler.handler(_event("PUT"), None)
    assert resp["statusCode"] == 405
