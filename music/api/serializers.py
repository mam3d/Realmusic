from rest_framework import serializers

from ..models import (
    Genre,
    Album,
    Song,
    Subtitle,
    View,
    PlayList,
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
        fields = ["url","name","artist","album", "image"]


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


class PlayListCreateUpdateSerializer(serializers.ModelSerializer):
    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True)
    add_song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(),required=False)
    remove_song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(),required=False)
    class Meta:
        model = PlayList
        fields = ["id","name","user","songs","add_song","remove_song","image"]
        extra_kwargs = {
            "user":{"read_only":True},
        }

    def create(self, validated_data):

        if validated_data.get("add_song"):
            validated_data.pop("add_song")

        if validated_data.get("remove_song"):
            validated_data.pop("remove_song")

        validated_data.update(user=self.context["request"].user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)

        if validated_data.get("add_song"):
            instance.songs.add(validated_data.get("add_song"))
        if validated_data.get("remove_song"):
            instance.songs.remove(validated_data.get("remove_song"))
        
        instance.save()
        return instance


class PlayListSerializer(serializers.ModelSerializer):
    songs = SongListSerializer(many=True, read_only=True)
    class Meta:
        model = PlayList
        fields = ["id","name","user","songs", "image"]
        extra_kwargs = {
            "user":{"read_only":True},
        }