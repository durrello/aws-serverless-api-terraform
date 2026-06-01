"""Lambda handler: a small CRUD API for "items" backed by DynamoDB.
Routes are dispatched from API Gateway HTTP API (payload format v2.0).
"""
import json
import os
import uuid

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "items")
_dynamodb = boto3.resource("dynamodb")


def _table():
    return _dynamodb.Table(TABLE_NAME)


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path = event.get("rawPath", "/")
    path_params = event.get("pathParameters") or {}
    item_id = path_params.get("id")

    table = _table()

    if method == "GET" and item_id:
        result = table.get_item(Key={"id": item_id})
        item = result.get("Item")
        if not item:
            return _response(404, {"error": "not found"})
        return _response(200, item)

    if method == "GET":
        items = table.scan().get("Items", [])
        return _response(200, {"items": items})

    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        new = {"id": str(uuid.uuid4()), "name": body.get("name", "")}
        table.put_item(Item=new)
        return _response(201, new)

    if method == "DELETE" and item_id:
        table.delete_item(Key={"id": item_id})
        return _response(204, {})

    return _response(405, {"error": f"method {method} not allowed on {path}"})
