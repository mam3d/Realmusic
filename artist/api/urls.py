from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ArtistViewSet,
    FollowCreateView,
    FollowDeleteView,
    
)

router = DefaultRouter()
router.register("",ArtistViewSet, basename="artist")

urlpatterns = [
    path("follow/", FollowCreateView.as_view(), name="follow-create"),
    path("follow/<int:pk>/", FollowDeleteView.as_view(), name="follow-delete"), 
]
urlpatterns += router.urls