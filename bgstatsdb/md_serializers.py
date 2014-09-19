from django.contrib.auth.models import User
from rest_framework import serializers
from bgstatsdb.models import Player, BoardGame, Location, GameInstance, PlayerScore, PlayerPlace

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password',)
        
    def restore_object(self, attrs, intance=None):
        # call set_password on user object. Without this password is stored in plain text
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user

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
    playerorder = serializers.RelatedField(many=True)
    photo = serializers.ImageField()
    boardgame = serializers.RelatedField()
    location = serializers.RelatedField()
    #poster = serializers.Field(source='poster.username')
    
    class Meta:
        model = GameInstance
        fields = ('playerscore', 'playerplace', 'playerorder', 'photo', 'boardgame', 'location', 'date')
        

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

class PlayerOrderSerializer(serializers.ModelSerializer):
    player = serializers.RelatedField()
    
    class Meta:
        model = PlayerPlace
        fields = ('player', 'order')