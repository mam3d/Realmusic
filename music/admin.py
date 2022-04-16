from django.contrib import admin
from .models import (
    Genre,
    Song,
    Subtitle,
    Album,
    View,
    PlayList,
)

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ["user","song"]


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ["name","user"]
    raw_id_fields = ("user","songs")


@admin.register(Genre)
class ViewAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["name","genre","download_url","total_views"]
    list_filter = ["genre","artist"]
    raw_id_fields = ("artist",)
    search_fields = ["name"]


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ["song","language"]
    list_filter = ["song__artist","language"]


class SongInline(admin.TabularInline):
    model = Song
    fields = ["name","artist","image","download_url","genre"]
    raw_id_fields = ("artist",)
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["name","artist","total_songs","genre"]
    list_filter = ["artist__name","genre"]
    inlines = [SongInline]