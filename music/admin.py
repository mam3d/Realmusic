from django.contrib import admin
from .models import (
    Genre,
    Song,
)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["name","genre","url"]
    list_filter = ["genre","artist"]