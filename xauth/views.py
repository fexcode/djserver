from django.contrib.auth import authenticate, login, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from consts.statuscodes import Codes, response, HS, success

User = get_user_model()


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
