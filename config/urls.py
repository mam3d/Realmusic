from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/user/', include("user.api.urls")),
   path('api/artist/', include("artist.api.urls")),
   path('api/music/', include("music.api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG == True:
   schema_view = get_schema_view(
   openapi.Info(
      title="Realmusic",
      default_version='v1',
   ),
   public=True,
   permission_classes=(AllowAny,),
   )

   urlpatterns += [
      path('__debug__/', include('debug_toolbar.urls')),
      path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   ]
