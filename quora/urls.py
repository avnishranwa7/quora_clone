from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("post-login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("post-question/", views.post_question, name="post-question"),
    path("post-comment/<int:question_id>/", views.post_comment, name="post-comment"),
    path("post-upvote/", views.post_upvote, name="post-upvote"),
    path("delete-comment/", views.delete_comment, name="delete-comment")
]