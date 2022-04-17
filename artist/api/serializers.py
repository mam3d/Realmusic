from rest_framework import serializers
from ..models import Artist


class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id","name","image"]


from music.api.serializers import SongListSerializer
class ArtistDetailSerializer(serializers.ModelSerializer):
    
    albums = serializers.SerializerMethodField()
    single_songs = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ["name","image", "albums", "single_songs"]

    def get_single_songs(self, obj):
        serializer = SongListSerializer(obj.get_single_songs(),many=True,context=self.context)
        return serializer.data

    def get_albums(self, obj):
        data = []
        for album in obj.get_albums():
            data.append({
                "id":album.id,
                "name":album.name,
                "image":self.context['request'].build_absolute_uri(obj.image.url),
                })
        return data