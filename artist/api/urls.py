from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ArtistViewSet,
    FollowCreateView,
    FollowDeleteView,
    FollowingView,
    
)

router = DefaultRouter()
router.register("",ArtistViewSet, basename="artist")

urlpatterns = [
    path("following/", FollowingView.as_view(), name="following"),
    path("follow/", FollowCreateView.as_view(), name="follow-create"),
    path("follow/<int:pk>/", FollowDeleteView.as_view(), name="follow-delete"), 
]
urlpatterns += router.urls