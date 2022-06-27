
from rest_framework import serializers

from ..models import (
    Genre,
    Album,
    Song,
    Subtitle,
    View,
    PlayList,
    Like,
)


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "image"]


class SongListSerializer(serializers.ModelSerializer):
    artists = serializers.StringRelatedField(many=True)
    total_views = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields = ["id", "name", "artists", "image", "duration", "total_views", "total_likes", "download_url"]

    def get_total_views(self, obj):
        return obj.views_count if hasattr(obj, "views_count") else obj.total_views

from artist.api.serializers import ArtistListSerializer
class SongDetailSerializer(serializers.ModelSerializer):
    artists = ArtistListSerializer(many=True, read_only=True)
    album = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    like_id = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields = ["id", "name", "artists", "image", 
            "album", "download_url", "duration", "genre", 
            "subtitles", "total_views", "total_likes", "like_id",
            ]

    def get_like_id(self, obj):
        # returns id of follow if the viewer user followed this artist else null
        user = self.context["request"].user
        like = Like.objects.filter(user=user, song=obj)
        if like:
            return like[0].id 

class AlbumDetailSerializer(serializers.ModelSerializer):
    songs =  SongListSerializer(many=True, read_only=True)                                              
    genre = serializers.StringRelatedField()
    artist = serializers.StringRelatedField()
    class Meta:
        model = Album
        fields = ["id","name","image","artist","total_songs","genre","songs"]

class AlbumListSerializer(serializers.ModelSerializer):                                           
    genre = serializers.StringRelatedField()
    class Meta:
        model = Album
        fields = ["id", "name", "image", "genre"]


class SubtitleDetailSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source="get_language_display")

    class Meta:
        model = Subtitle
        fields = ["id","song","language","text"]


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ["id", "song"]

    def create(self, validated_data):
        user = self.context["request"].user
        song = validated_data["song"]
        view, created = View.objects.get_or_create(user=user, song=song)
        return view


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "song"]
        extra_kwargs = {"id":{"read_only":True}}

    def create(self, validated_data):
        user = self.context["request"].user
        song = validated_data["song"]
        like, created = Like.objects.get_or_create(user=user, song=song)
        return like

class LikeListSerializer(serializers.ModelSerializer):
    song = SongListSerializer()
    class Meta:
        model = Like
        fields = ["song"]

class PlayListUpdateSerializer(serializers.ModelSerializer):
    add_songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), required=False, many=True)
    remove_songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), required=False, many=True)
    clear_songs = serializers.BooleanField(write_only=True, required=False)
    class Meta:
        model = PlayList
        fields = ["name","image", "add_songs", "remove_songs", "clear_songs"]
        extra_kwargs = {
            "name":{"required":False}
        }

    def update(self, instance, validated_data):
        name = validated_data.get("name")
        image = validated_data.get("image")
        add_songs = validated_data.get("add_songs")
        remove_songs = validated_data.get("remove_songs")
        clear_songs = validated_data.get("clear_songs")

        if add_songs:
            for song in add_songs:
                instance.songs.add(song)

        if remove_songs:
            for song in validated_data.get("remove_songs"):
                instance.songs.remove(song)

        if clear_songs:
            instance.songs.clear()

        instance.name = instance.name if name is None else name
        instance.image = instance.image if image is None else image
        instance.save()
        return instance
    
    def to_representation(self, instance):
        self.fields.pop("add_songs", None)
        self.fields.pop("remove_songs", None)
        return super().to_representation(instance)

class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ["id", "name", "image", "user", "songs"]
        extra_kwargs = {
            "user":{"read_only":True},
        }



class PlayListDetailSerializer(serializers.ModelSerializer):
    songs = SongListSerializer(many=True, read_only=True)
    class Meta:
        model = PlayList
        fields = ["id","name","user","songs", "image"]
        extra_kwargs = {
            "user":{"read_only":True},
        }

class PlayListListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ["id", "name", "image"]