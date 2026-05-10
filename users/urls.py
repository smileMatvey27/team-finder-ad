from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("list/", views.user_list, name="users_list"),
    path("<int:user_id>/", views.user_details, name="user_detail"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("edit-profile/", views.user_edit_profile, name="edit_profile"),
    path("change-password/", views.user_change_password, name="change_password"),
    path("logout/", views.user_logout, name="logout"),
]
