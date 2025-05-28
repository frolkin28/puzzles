import json
from django.http import HttpRequest


def parse_json(request: HttpRequest) -> dict | None:
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None
