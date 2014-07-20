from django.contrib.auth.models import User
from rest_framework import serializers
from bgstatsdb.models import Player, BoardGame, Location, GameInstance, PlayerScore, PlayerPlace

class UserSerializer(serializers.ModelSerializer):
    postedgames = serializers.PrimaryKeyRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ('id', 'user', 'postedgames')

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')


class BoardGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardGame
        fields = ('id', 'name')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name')

    
class GameInstanceSerializer(serializers.ModelSerializer):
    playerscore = serializers.RelatedField(many=True)
    playerplace = serializers.RelatedField(many=True)
    boardgame = serializers.RelatedField()
    location = serializers.RelatedField()
    poster = serializers.Field(source='poster.username')
    
    class Meta:
        model = GameInstance
        fields = ('playerscore', 'playerplace', 'boardgame', 'location', 'date', 'poster')
        

class PlayerScoreSerializer(serializers.ModelSerializer):
    player = serializers.RelatedField()
    
    class Meta:
        model = PlayerScore
        fields = ('player', 'score')
        

class PlayerPlaceSerializer(serializers.ModelSerializer):
    player = serializers.RelatedField()
    
    class Meta:
        model = PlayerPlace
        fields = ('player', 'place')