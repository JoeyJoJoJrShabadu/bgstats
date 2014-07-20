from django.contrib import admin
from bgstatsdb.models import Player, BoardGame, PlayerScore, PlayerPlace, Location, GameInstance

admin.site.register([Player, BoardGame, PlayerScore, PlayerPlace, Location, GameInstance])