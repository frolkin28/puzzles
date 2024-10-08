from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt

from puzzles.account.exc import UserAlreadyExists
from pydantic import ValidationError

from puzzles.utils.api import parse_json
from puzzles.account.lib import register_user, EmailBackend
from puzzles.account.schemas import RegisterModel, LoginModel


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request: HttpRequest) -> JsonResponse:
    request_json = parse_json(request)
    if request_json is None:
        return JsonResponse({"errors": {"message": "Invalid JSON"}}, status=400)

    try:
        payload = RegisterModel(**request_json)
    except ValidationError as e:
        return JsonResponse({"errors": e.errors()}, status=400)

    try:
        craeted_user = register_user(payload)
    except UserAlreadyExists:
        return JsonResponse(
            {"errors": {"email": "This email is already in use"}}, status=400
        )

    login(request=request, user=craeted_user, backend=EmailBackend)

    return JsonResponse({"success": True}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request: HttpRequest) -> JsonResponse:
    request_json = parse_json(request)
    if request_json is None:
        return JsonResponse({"errors": {"message": "Invalid JSON"}}, status=400)

    try:
        payload = LoginModel(**request_json)
    except ValidationError as e:
        return JsonResponse({"errors": e.errors()}, status=400)

    user = authenticate(request, email=payload.email, password=payload.password)

    if user is None:
        return JsonResponse({}, status=401)

    login(request=request, user=user, backend=EmailBackend)

    return JsonResponse({"success": True}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request: HttpRequest) -> JsonResponse:
    logout(request)
    return JsonResponse({"success": True}, status=200)
