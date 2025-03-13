from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title", "description", "slug", "is_published", "created_at"
    ]
    search_fields = ["title", "description", "slug"]
    list_filter = ["is_published", "created_at"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "is_published", "created_at"]
    search_fields = ["name"]
    list_filter = ["is_published", "created_at"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "pub_date",
        "is_published",
        "created_at",
        "location",
    ]
    search_fields = ["title", "text", "author__username", "location__name"]
    list_filter = [
        "pub_date", "category", "location", "is_published", "created_at"
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "text", "created_at"]
    search_fields = ["post__title", "author__username", "text"]
    list_filter = ["created_at"]
