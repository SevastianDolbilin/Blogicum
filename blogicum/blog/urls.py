from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path(
        "category/<slug:category_slug>/",
        views.category_posts,
        name="category_posts",
    ),
    path("posts/create/", views.create_post, name="create_post"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path(
        "registration/<str:username>/password_change_form/",
        views.change_password,
        name="change_password",
    ),
    path(
        "edit_profile/<str:username>/", views.edit_profile, name="edit_profile"
    ),
    path("posts/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path(
        'posts/<int:post_id>/comment/', views.add_comment, name='add_comment'
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment"
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment"
    )

]
