from django.contrib import admin
from .models import Artist, Follow

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name","genre"]
    list_filter = ["genre"]

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["user","artist"]
    raw_id_fields = ["user", "artist"]