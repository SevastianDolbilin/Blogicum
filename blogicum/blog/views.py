from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import CommentForm, PostCreateForm, UserEditForm
from .models import Category, Comment, Post
from .utils import get_paginated_posts, redirect_to_post_detail


def profile(request, username):
    """View - функция страницы профиля"""
    user = get_object_or_404(User, username=username)

    include_draft = request.user == user

    page_obj = get_paginated_posts(
        request,
        {"author": user},
        include_draft=include_draft
    )

    context = {
        "profile": user,
        "page_obj": page_obj,
    }
    return render(request, "blog/profile.html", context)


def index(request):
    """View - функция главной страницы"""
    filter_kwargs = {}
    page_obj = get_paginated_posts(request, filter_kwargs, include_draft=False)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "blog/index.html", context)


def post_detail(request, post_id):
    """View - функция страницы поста"""
    post = get_object_or_404(Post, id=post_id)
    now = timezone.now()
    if request.user != post.author:
        if not post.category.is_published:
            raise Http404()
        if post.pub_date > now:
            raise Http404()
        if not post.is_published:
            raise Http404()
    comments = post.comments.all()
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form
    }
    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):
    """View - функция страницы категорий"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    page_obj = get_paginated_posts(
        request,
        {"category": category},
        include_draft=False
    )
    context = {
        "category": category,
        "page_obj": page_obj
    }
    return render(request, "blog/category.html", context)


@login_required
def edit_profile(request, username):
    """View - функция страницы редактирования профиля"""
    user = get_object_or_404(User, username=username)

    if request.user != user:
        return redirect(reverse("blog:profile", args=[user.username]))

    form = UserEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect(reverse("blog:profile", args=[user.username]))

    return render(
        request,
        "blog/edit_profile.html",
        {"form": form, "user": user}
    )


@login_required
def create_post(request):
    """View - функция страницы создания поста"""
    form = PostCreateForm(
        request.POST or None,
        request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user

        now = timezone.now()
        post.is_scheduled = post.pub_date > now

        post.save()
        return redirect(reverse("blog:profile", args=[request.user.username]))

    return render(request, "posts/create.html", {"form": form})


@login_required
def delete_post(request, post_id):
    """View - функция страницы удаления поста"""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect(reverse("blog:create_post"))
    context = {"post": post}
    return render(request, "posts/create.html", context)


@login_required
def edit_post(request, post_id):
    """View - функция страницы редактирования поста"""
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect_to_post_detail(post_id)
    form = PostCreateForm(
        request.POST or None,
        request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect_to_post_detail(post_id)
    context = {"form": form}
    return render(request, "posts/create.html", context)


@login_required
def add_comment(request, post_id):
    """View - функция страницы добавления комментария"""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect_to_post_detail(post_id)
    context = {"form": form}
    return render(request, "includes/comments.html", context)


@login_required
def edit_comment(request, post_id, comment_id):
    """View - функция  страницы редактирования комментария"""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect_to_post_detail(post_id)

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect_to_post_detail(post_id)

    context = {
        "form": form,
        "comment": comment,
        "post_id": post_id,
    }
    return render(request, "blog/comment.html", context)


@login_required
def delete_comment(request, post_id, comment_id):
    """View - функция страницы удаления комментария"""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        comment.text
        comment.delete()
        return redirect(reverse("blog:post_detail", args=[post_id]))
    return render(request, "blog/comment.html")


@login_required
def change_password(request, username):
    """View - функция страницы смены пароля"""
    if request.user.username != username:
        return redirect("blog:profile", username=username)

    form = PasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect("blog:profile", username=request.user.username)
    context = {"form": form}
    return render(request, "registration/password_change_form.html", context)
