
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("user.api.urls")),
    path('api/artist/', include("artist.api.urls")),
    path('api/music/', include("music.api.urls")),
]
