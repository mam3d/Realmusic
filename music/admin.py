from django.contrib import admin
from .models import (
    Genre,
    Song,
    Subtitle,
    Album,
    View,
    PlayList,
    Like,
)

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ["user","song", "date"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["user","song"]
    exclude = ["id"]
    raw_id_fields = ["user", "song"]


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ["name","user"]
    raw_id_fields = ("user","songs")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["name", "genre", "download_url", "duration", "total_views", "total_likes"]
    list_filter = ["genre", "artists"]
    raw_id_fields = ("artists",)
    search_fields = ["name", "id"]


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ["song","language"]
    list_filter = ["song__artists","language"]


class SongInline(admin.TabularInline):
    model = Song
    fields = ["name", "artists", "image", "download_url", "duration", "genre"]
    raw_id_fields = ("artists",)
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["name","artist","total_songs","genre"]
    list_filter = ["artist__name","genre"]
    inlines = [SongInline]