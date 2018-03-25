from .models import User, Season, Tournament, Set, Game, FileUpload
from rest_framework import serializers


class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = FileUpload
        fields = ('created', 'datafile', 'owner')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'real_name', 'tag', 'join_date', 'profile_picture', 'icon_url')


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = ('pk', 'name', 'start_date', 'end_date')


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = ('pk', 'name', 'date', 'season')


class SetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Set
        fields = ('pk', 'victor', 'child_set', 'player_one', 'player_two', 'tournament')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('pk', 'set', 'round_number', 'victor')
