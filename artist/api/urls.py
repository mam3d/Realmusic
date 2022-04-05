from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet

router = DefaultRouter()
router.register("",ArtistViewSet, basename="artist")

urlpatterns = [    
]
urlpatterns += router.urls