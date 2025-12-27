from django.contrib.auth import authenticate, login, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from consts.statuscodes import Codes, response, HS, success
from drf_spectacular.utils import extend_schema, OpenApiResponse

User = get_user_model()


@extend_schema(
    summary="用户登录",
    description="账号密码登录，成功返回 JSON 并写 session",
    responses={
        200: OpenApiResponse(description="登录成功"),
        400: OpenApiResponse(description="用户名或密码错误"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def session_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return success(msg="登录成功")

    return response(
        httpstatus=HS.BAD_REQUEST,
        status=Codes.NameOrPasswdIncorrect,
    )


@extend_schema(
    summary="用户注册",
    description="用户名密码注册，成功返回 JSON 并写 session",
    responses={
        200: OpenApiResponse(description="注册成功"),
        400: OpenApiResponse(description="用户名已存在"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return response(status=Codes.UserExists, httpstatus=HS.BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    login(request, user)  # 注册完直接登录
    return success(msg="注册成功")


@api_view(["GET"])
def whoami(request):
    user = request.user
    if user.is_authenticated:
        return success(data={"username": user.username})
    return response(status=Codes.UserNotExists, httpstatus=HS.BAD_REQUEST)


@api_view(["GET"])
def islogined(request):
    user = request.user
    if user.is_authenticated:
        return success(data={"islogined": True})
    return response(status=Codes.OK, data={"islogined": False})
