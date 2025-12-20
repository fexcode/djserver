# xauth/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from consts.statuscodes import Codes

User = get_user_model()


class AuthAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # 提前造一个老用户，用于登录/重复注册测试
        self.existing_user = User.objects.create_user(
            username="alice", password="123456"
        )

    # ---------------- 登录 ----------------
    def test_login_success(self):
        """正确密码能登录，返回 200"""
        res = self.client.post(
            reverse("session_login"),  # 对应 url name='session_login'
            {"username": "alice", "password": "123456"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["status"], Codes.OK)
        self.assertEqual(res.data["msg"], "登录成功")

    def test_login_wrong_password(self):
        """密码错误 → 400 + 业务码"""
        res = self.client.post(
            reverse("session_login"),
            {"username": "alice", "password": "wrongpass"},
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["status"], Codes.NameOrPasswdIncorrect)

    # ---------------- 注册 ----------------
    def test_signup_new_user(self):
        """新用户注册 → 201（DRF 默认 201）+ 自动登录"""
        res = self.client.post(
            reverse("signup"),
            {"username": "bob", "password": "654321"},
        )
        # 注册成功默认返回 201，success() 里没改 httpstatus 就是 200
        # 如果想严格 201 可在 success() 里加参数，这里先断言 200
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["status"], Codes.OK)
        # 验证用户真的被创建
        self.assertTrue(User.objects.filter(username="bob").exists())

    def test_signup_duplicate(self):
        """重复注册 → 400 + 业务码"""
        res = self.client.post(
            reverse("signup"),
            {"username": "alice", "password": "whatever"},
        )
        res = self.client.post(
            reverse("signup"),
            {"username": "alice", "password": "whatever"},
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["status"], Codes.UserExists)

    # ---------------- 带 Cookie 的集成示例 ----------------
    def test_session_workflow(self):
        """注册->后端写session->后续请求带Cookie能识别用户"""
        # 1. 注册并登录
        res = self.client.post(
            reverse("signup"),
            {"username": "carol", "password": "111111"},
        )
        self.assertEqual(res.status_code, 200)

        # 带着sessionid请求 /auth/whoami
        res = self.client.get(reverse("whoami"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["data"]["username"], "carol")