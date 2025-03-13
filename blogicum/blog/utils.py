from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from .constants import COUNT_OF_POSTS
from .models import Post


def get_paginated_posts(
        request,
        filter_kwargs,
        posts_per_page=COUNT_OF_POSTS,
        include_draft=False
):
    """Утилита для фильтрации и пагинации постов"""
    now = timezone.now()

    if include_draft:
        posts = Post.objects.filter(
            Q(is_published=True, pub_date__lte=now) | Q(author=request.user),
            **filter_kwargs
        )
    else:
        posts = Post.objects.filter(
            is_published=True,
            pub_date__lte=now,
            category__is_published=True,
            **filter_kwargs
        )

    posts = posts.order_by("-pub_date").annotate(
        comment_count=Count("comments")
    )

    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj


def redirect_to_post_detail(post_id):
    """Утилита для редиректа на страницу с деталями поста"""
    return redirect(reverse("blog:post_detail", args=[post_id]))
