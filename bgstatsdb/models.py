from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class BoardGame(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name
    

class Location(models.Model):
    name = models.CharField(max_length=511, unique=True)
    
    def __str__(self):
        return self.name
   
    
class PlayerScore(models.Model):
    player = models.ForeignKey(Player)
    score = models.IntegerField()
    
    def __str__(self):
        return "%s: %d" % (self.player, self.score)
    
    def __unicode__(self):
        return "%s: %d" % (self.player, self.score)
    

class PlayerPlace(models.Model):
    player = models.ForeignKey(Player)
    place = models.IntegerField()
    
    def __str__(self):
        return "%s: %d" % (self.player, self.place)
    
    def __unicode__(self):
        return "%s: %d" % (self.player, self.place)


class FBGame(models.Model):
    gametext = models.TextField()


class GameInstance(models.Model):
    playerscore = models.ManyToManyField(PlayerScore)
    playerplace = models.ManyToManyField(PlayerPlace)
    boardgame = models.ForeignKey(BoardGame)
    location = models.OneToOneField(Location)
    date = models.DateField('date played')
    poster = models.ForeignKey('auth.User', related_name='postedgames')
    
    