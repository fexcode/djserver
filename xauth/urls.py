from django.urls import path
from .views import session_login, signup,whoami

urlpatterns = [
    path("login", session_login, name="session_login"),
    path("signup", signup, name="signup"),
    path("whoami", whoami, name="whoami")
]
