from django.contrib import admin
from .models import Artist

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name","genre"]
    list_filter = ["genre"]
    prepopulated_fields = {"slug":("name",)}