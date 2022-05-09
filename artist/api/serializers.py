from rest_framework import serializers
from ..models import Artist, Follow




class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id","name","image"]


from music.api.serializers import SongListSerializer, AlbumListSerializer
class ArtistDetailSerializer(serializers.ModelSerializer):    
    albums = AlbumListSerializer(read_only=True, many=True)
    single_songs = serializers.SerializerMethodField()
    follow = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ["name", "image", "follow", "albums", "single_songs"]

    def get_single_songs(self, obj):
        serializer = SongListSerializer(obj.get_single_songs(),many=True,context=self.context)
        return serializer.data

    def get_follow(self, obj):
        # returns id of follow if the viewer user followed this artist else null
        user = self.context["request"].user
        follow = Follow.objects.filter(user=user, artist=obj)
        if follow:
            return follow[0].id 


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "artist"]
        extra_kwargs = {"id":{"read_only":True}}


    def create(self, validated_data):
        user = self.context["request"].user
        artist = validated_data["artist"]
        follow, created = Follow.objects.get_or_create(user=user, artist=artist)
        return follow


class FollowingSerializer(serializers.ModelSerializer):
    artist = ArtistListSerializer()
    class Meta:
        model = Follow
        fields = ["id", "artist"]

