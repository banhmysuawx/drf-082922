from django.urls import path, include
from .views import *

urlpatterns = [
    path("registers", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("users", UserView.as_view(), name="users"),
    path("logout", LogoutView.as_view(), name="logout"),
]
