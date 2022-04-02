from django.contrib import admin
from .models import (
    Genre,
    Song,
    Subtitle,
    Album,
)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["name","genre","url"]
    list_filter = ["genre","artist"]
    raw_id_fields = ("artist",)


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ["song","language"]
    list_filter = ["song__artist","language"]


class SongInline(admin.TabularInline):
    model = Song
    fields = ["name","artist","image","url","genre"]
    raw_id_fields = ("artist",)
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["name","artist","total_songs","genre"]
    list_filter = ["artist__name","genre"]
    inlines = [SongInline]