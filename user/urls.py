from django.urls import path

from user.views import UserView

urlpatterns = [
    path("register/", UserView.as_view(), name="register")
]