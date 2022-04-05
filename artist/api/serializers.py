from rest_framework import serializers
from ..models import Artist


class ArtistListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="artist-detail",lookup_field="slug")
    class Meta:
        model = Artist
        fields = ["url","name","image", "genre"]


class ArtistDetailSerializer(serializers.ModelSerializer):
    albums = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Artist
        fields = ["name","image", "albums"]
