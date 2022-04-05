from rest_framework import serializers
from music.api.serializers import SongListSerializer
from ..models import Artist


class ArtistListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="artist-detail",lookup_field="slug")
    genre = serializers.StringRelatedField()
    class Meta:
        model = Artist
        fields = ["url","name","image", "genre"]


class ArtistDetailSerializer(serializers.ModelSerializer):
    albums = serializers.HyperlinkedRelatedField(view_name="album-detail",
                                                    many=True,
                                                    read_only=True
                                                    )
    single_songs = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ["name","image", "albums", "single_songs"]

    def get_single_songs(self, obj):
        serializer = SongListSerializer(obj.get_single_songs(),many=True,context=self.context)
        return serializer.data