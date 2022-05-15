
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
        fields = ["id","name"]


class SongListSerializer(serializers.ModelSerializer):
    artists = serializers.StringRelatedField(many=True)


    class Meta:
        model = Song
        fields = ["id", "name", "artists", "image", "duration", "total_views", "total_likes", "download_url"]


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


class PlayListCreateUpdateSerializer(serializers.ModelSerializer):
    add_songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), required=False, many=True)
    remove_songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), required=False, many=True)
    clear_songs = serializers.BooleanField(write_only=True, required=False)
    class Meta:
        model = PlayList
        fields = ["id", "name", "image", "user", "add_songs", "remove_songs", "clear_songs", "songs"]
        extra_kwargs = {
            "user":{"read_only":True},
            "songs":{"read_only":True},
        }

    def create(self, validated_data):
        validated_data.pop("remove_songs", None)
        validated_data.pop("clear_songs", None)

        # playlist's songs field name is songs so changed the keyname in dictionary for creating object
        add_songs = validated_data.pop("add_songs", None)
        validated_data.update(songs=add_songs)

        validated_data.update(user=self.context["request"].user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)

        if validated_data.get("add_songs"):
            for song in validated_data.get("add_songs"):
                instance.songs.add(song)

        if validated_data.get("remove_songs"):
            for song in validated_data.get("remove_songs"):
                instance.songs.remove(song)

        if validated_data.get("clear_songs"):
            instance.songs.clear()

        instance.save()
        return instance

    def to_representation(self, instance):
        self.fields.pop("add_songs", None)
        self.fields.pop("remove_songs", None)
        return super().to_representation(instance)


class PlayListDetailSerializer(serializers.ModelSerializer):
    songs = SongListSerializer(many=True, read_only=True)
    class Meta:
        model = PlayList
        fields = ["id","name","user","songs", "image"]
        extra_kwargs = {
            "user":{"read_only":True},
        }

class PlayListListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = PlayList
        fields = ["id", "name", "user", "image"]