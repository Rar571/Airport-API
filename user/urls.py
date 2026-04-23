from django.urls import path

from user.views import UserView, LoginUserView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", UserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage_user")
]
