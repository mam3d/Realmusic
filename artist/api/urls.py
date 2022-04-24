from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ArtistViewSet,
    FollowView,
    FollowDeleteView,
    
)

router = DefaultRouter()
router.register("",ArtistViewSet, basename="artist")

urlpatterns = [
    path("follow/", FollowView.as_view(), name="follow"),
    path("follow/<int:pk>/", FollowDeleteView.as_view(), name="follow-delete"), 
]
urlpatterns += router.urls