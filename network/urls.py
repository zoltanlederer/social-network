
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following/<int:id>", views.following, name="following"),

    # API
    path("edit_post/<int:id>", views.edit_post, name="edit_post"),
    path("like/<int:id>/<str:update>", views.like, name="like"),
    path("follow/<int:id>/<str:update>", views.follow, name="follow"),
]
