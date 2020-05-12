from django.contrib import admin

from .models import Category, Comment, Land, List, Post


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    model = Land
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    search_fields = ("name",)
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    model = Post
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    search_fields = ("text",)
    ordering = ("text",)
