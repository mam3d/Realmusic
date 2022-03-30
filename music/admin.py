from django.contrib import admin
from .models import (
    Genre,
    Song,
    Subtitle
)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["name","genre","url"]
    list_filter = ["genre","artist"]
    raw_id_fields = ('artist',)

@admin.register(Subtitle)
class SongAdmin(admin.ModelAdmin):
    list_display = ["song","language"]
    list_filter = ["song__artist","language"]