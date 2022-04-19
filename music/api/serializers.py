from rest_framework import serializers
from artist.api.serializers import ArtistListSerializer
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
        fields = ["id","name","artists", "image", "total_views"]


class SongDetailSerializer(serializers.ModelSerializer):
    artists = ArtistListSerializer(many=True, read_only=True)
    album = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    class Meta:
        model = Song
        fields = ["name","artists","image","album","download_url","genre","subtitles"]


class AlbumDetailSerializer(serializers.ModelSerializer):
    songs =  SongListSerializer(many=True, read_only=True)                                              
    genre = serializers.StringRelatedField()
    artist = serializers.StringRelatedField()
    class Meta:
        model = Album
        fields = ["id","name","image","artist","total_songs","genre","songs"]


class SubtitleDetailSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source="get_language_display")

    class Meta:
        model = Subtitle
        fields = ["id","song","language","text"]


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ["user","song"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'song'),
                message=(f"view with this user and song already exists")
            )
        ]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["user","song"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'song'),
                message=(f"like with this user and song already exists")
            )
        ]


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

class PlayListSerializer(serializers.ModelSerializer):
    songs = SongListSerializer(many=True, read_only=True)
    class Meta:
        model = PlayList
        fields = ["id","name","user","songs", "image"]
        extra_kwargs = {
            "user":{"read_only":True},
        }