# xblogs/views_read.py
from django.http import JsonResponse, HttpRequest
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny
import json
from .models import ReadRecord


@extend_schema(
    summary="全站阅读总数",
    description="统计全站所有博客的阅读记录总数。<br>"
    "query 参数 `login_user_only=true` 时只统计「登录用户」产生的记录。",
    parameters=[
        OpenApiParameter(
            name="login_user_only",
            type=bool,
            required=False,
            default=False,
            description="true=仅统计登录用户；false=全部",
        )
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                "ReadCountGlobalResp",
                {"count": serializers.IntegerField(help_text="阅读总数")},
            ),
            description="统计成功",
        )
    },
    tags=["阅读统计"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([])
def getall_read_count_sum(request: HttpRequest):
    login_only = request.GET.get("login_user_only", "").lower() == "true"
    qs = (
        ReadRecord.objects.filter(uid__gt=0) if login_only else ReadRecord.objects.all()
    )
    return JsonResponse({"count": qs.count()})


@extend_schema(
    summary="单篇阅读数",
    description="获取指定博客的阅读记录总数。<br>"
    "body 里传 `login_user_only=true` 时只统计「登录用户」产生的记录。",
    request=inline_serializer(
        "ReadCountReq",
        {
            "blog_id": serializers.IntegerField(help_text="博客主键"),
            "login_user_only": serializers.BooleanField(
                default=False, help_text="true=仅统计登录用户", required=False
            ),
        },
    ),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                "ReadCountResp", {"count": serializers.IntegerField()}
            ),
            description="统计成功",
        ),
        400: OpenApiResponse(description="blog_id 未传或格式错误"),
    },
    tags=["阅读统计"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def get_read_count(request: HttpRequest):
    blog_id = request.POST.get("blog_id")
    if not blog_id:
        return JsonResponse({"count": 0})

    try:
        blog_id = int(blog_id)
    except ValueError:
        return JsonResponse({"count": 0}, status=400)

    login_only = request.POST.get("login_user_only", "").lower() == "true"
    qs = ReadRecord.objects.filter(blog_id=blog_id)
    if login_only:
        qs = qs.filter(uid__gt=0)

    return JsonResponse({"count": qs.count()})


@extend_schema(
    summary="新增阅读记录",
    description="为指定博客增加一条阅读记录；未登录用户 uid 记 0。",
    request=inline_serializer(
        "AddCountReq", {"blog_id": serializers.IntegerField(help_text="博客主键")}
    ),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                "AddCountResp",
                {
                    "status": serializers.ChoiceField(choices=["success"]),
                    "count": serializers.IntegerField(help_text="该博客最新阅读数"),
                },
            ),
            description="记录成功",
        ),
        400: OpenApiResponse(description="blog_id 缺失"),
    },
    tags=["阅读统计"],
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def add_count(request: HttpRequest):
    # 获取json数据
    postdata = json.loads(request.body)

    blog_id = postdata.get("blogid")
    print(dict(postdata))
    print(blog_id)
    if blog_id is None:
        return JsonResponse({"status": "error", "message": "参数错误"}, status=400)

    try:
        blog_id = int(blog_id)
    except ValueError:
        return JsonResponse(
            {"status": "error", "message": "blog_id 必须是整数"}, status=400
        )

    uid = request.user.id if request.user.is_authenticated else 0  # type: ignore
    ReadRecord.objects.create(uid=uid, blog_id=blog_id, unlogined=bool(uid == 0))

    return JsonResponse(
        {
            "status": "success",
            "count": ReadRecord.objects.filter(blog_id=blog_id).count(),
        }
    )
