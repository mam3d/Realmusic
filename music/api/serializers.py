from rest_framework import serializers
from ..models import (
    Genre,
    Album,
    Song,
    Subtitle,
    View,
)

class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id","name"]


class AlbumDetailSerializer(serializers.ModelSerializer):
    artist = serializers.HyperlinkedRelatedField(view_name="artist-detail",
                                                read_only=True,
                                                lookup_field="slug",
                                                )
    songs = serializers.HyperlinkedRelatedField(view_name="song-detail",
                                                read_only=True,
                                                many=True,
                                                )                                               
    genre = serializers.StringRelatedField()
    class Meta:
        model = Album
        fields = ["id","name","image","artist","total_songs","genre","songs"]


class SongListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="song-detail")
    artist = serializers.HyperlinkedRelatedField(view_name="artist-detail",
                                            lookup_field="slug",
                                            read_only=True,
                                            many=True,
                                            )
    class Meta:
        model = Song
        fields = ["url","name","artist","album"]


class SongDetailSerializer(serializers.ModelSerializer):
    artist = serializers.HyperlinkedRelatedField(view_name="artist-detail",
                                        lookup_field="slug",
                                        read_only=True,
                                        many=True,
                                        )
    subtitles = serializers.HyperlinkedRelatedField(view_name="subtitle-detail",
                                    read_only=True,
                                    many=True,
                                    )
    album = serializers.StringRelatedField()
    genre = serializers.StringRelatedField()
    class Meta:
        model = Song
        fields = ["name","artist","image","album","download_url","genre","subtitles"]


class SubtitleDetailSerializer(serializers.ModelSerializer):
    song = serializers.HyperlinkedRelatedField(view_name="song-detail",read_only=True)
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
