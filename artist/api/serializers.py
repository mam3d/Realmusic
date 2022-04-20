from rest_framework import serializers
from ..models import Artist, Follow


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

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "artist"]
        extra_kwargs = {"id":{"read_only":True}}

    def validate(self, validated_data):
        user = self.context["request"].user
        artist = validated_data["artist"]
        try:
            Follow.objects.get(user=user, artist=artist)
        except Follow.DoesNotExist:
            return validated_data   
        raise serializers.ValidationError("follow with this user and artist exists")

    def create(self, validated_data):
        validated_data.update(user=self.context["request"].user)
        return super().create(validated_data)