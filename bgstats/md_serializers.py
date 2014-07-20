from django.forms import widgets
from rest_framework import serializers
from bgstatsdb.models import Player, BoardGame, Location, GameInstance, PlayerScore, PlayerPlace


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
    player_score = serializers.RelatedField(many=True)
    player_place = serializers.RelatedField(many=True)
    boardgame = serializers.RelatedField()
    location = serializers.RelatedField()
    
    class Meta:
        model = GameInstance
        fields = ('player_score', 'player_place', 'boardgame', 'location', 'date')
        

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