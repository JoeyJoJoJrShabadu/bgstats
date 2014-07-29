import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from bgstatsdb.models import BoardGame, Player, PlayerScore, PlayerPlace, Location, GameInstance

class PlayerTestCase(TestCase):
    def setUp(self):
        Player.objects.create(name="Player1")
        Player.objects.create(name="Player2")
    
    def test_players_exist(self):
        msg = "Expected two players"
        self.assertIsNotNone(Player.objects.get(name="Player1"), msg)
        self.assertIsNotNone(Player.objects.get(name="Player2"), msg)
        self.assertEqual(len(Player.objects.all()), 2, msg)

                         
class BoardGameTestCase(TestCase):
    def setUp(self):
        BoardGame.objects.create(name="Game1")
        BoardGame.objects.create(name="Game2")
    
    def test_games_exist(self):
        msg = "Expected two games"
        self.assertIsNotNone(BoardGame.objects.get(name="Game1"), msg)
        self.assertIsNotNone(BoardGame.objects.get(name="Game2"), msg)
        self.assertEqual(len(BoardGame.objects.all()), 2, msg)
        
        
class LocationTestCase(TestCase):
    def setUp(self):
        Location.objects.create(name="Loc1")
        Location.objects.create(name="Loc2")
    
    def test_games_exist(self):
        msg = "Expected two games"
        self.assertIsNotNone(Location.objects.get(name="Loc1"), msg)
        self.assertIsNotNone(Location.objects.get(name="Loc2"), msg)
        self.assertEqual(len(Location.objects.all()), 2, msg)
        

class PlayerScorePlaceTestCase(TestCase):
    def setUp(self):
        self.p1 = Player.objects.create(name="p1")
        self.p2 = Player.objects.create(name="p2")
        PlayerScore.objects.create(player=self.p1, score=5)
        PlayerScore.objects.create(player=self.p2, score=10)
        PlayerScore.objects.create(player=self.p1, score=8)
        PlayerPlace.objects.create(player=self.p1, place=1)
        PlayerPlace.objects.create(player=self.p2, place=2)
    
    def test_scores(self):
        msg = "Expected 3 scores"
        self.assertEqual(len(PlayerScore.objects.all()), 3, msg)
        self.assertEqual(len(PlayerScore.objects.all().filter(player=self.p1)), 2, msg)
        
    def test_place(self):
        msg = "Expected 2 places"
        self.assertEqual(len(PlayerPlace.objects.all()), 2, msg)
        self.assertEqual(len(PlayerPlace.objects.all().filter(player=self.p1)), 1, msg)
        

class GameInstanceTest(TestCase):
    def setUp(self):
        self.p1 = Player.objects.create(name='p1')
        self.p2 = Player.objects.create(name="p2")
        self.loc = Location.objects.create(name='myplace')
        self.bg = BoardGame.objects.create(name='testgame')
        self.user = User.objects.create(username="test")
        
    def test_create_game(self):
        self.ps1 = PlayerScore.objects.create(player=self.p1, score=5)
        self.ps2 = PlayerScore.objects.create(player=self.p2, score=10)
        self.pp1 = PlayerPlace.objects.create(player=self.p1, place=1)
        self.pp2 = PlayerPlace.objects.create(player=self.p2, place=2)
        self.gi = GameInstance(location=self.loc,
                               boardgame = self.bg,
                               date=datetime.datetime.now(),
                               poster = self.user)
        self.gi.save()
        self.gi.playerscore.add(self.ps1.id, self.ps2.id)
        self.gi.playerplace.add(self.pp1.id, self.pp2.id)
        self.gi.save()
        print self.gi.playerscore
        self.assertIsInstance(self.gi, GameInstance,
                              "Must be an instance of game")