from itertools import chain
import json

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from bgstatsdb.models import * 
from bgstatsdb.md_serializers import *
from bgstatsdb.permissions import IsOwnerOrReadOnly

AUTOMODELS = {'players':["Player", Player, PlayerSerializer],
             'boardgames':["BoardGame", BoardGame, BoardGameSerializer],
             'locations':["Location", Location, LocationSerializer],
             'playerscores':["PlayerScore", PlayerScore, PlayerScoreSerializer],
             'playerplaces':["PlayerPlace", PlayerPlace, PlayerPlaceSerializer],
             'users':["User", User, UserSerializer]}


def ClassFactory(name, qs, sc, BaseClass=generics.RetrieveUpdateDestroyAPIView):
    def __init__(self, **kwargs):
        setattr(self, 'queryset', qs.objects.all())
        setattr(self, 'serializer_class', sc)
        BaseClass.__init__(self)
    
    newclass = type(name, (BaseClass,),{"__init__":__init__})
    return newclass


for key, vals in AUTOMODELS.items():
    vars()[vals[0] + "List"] = ClassFactory(vals[0] + "List", vals[1], vals[2], BaseClass=generics.ListCreateAPIView)
    if "user" == key:
        vars()[vals[0] + "Detail"] = ClassFactory(vals[0] + "List", vals[1], vals[2], BaseClass=generics.RetrieveAPIView)
        continue
    vars()[vals[0] + "Detail"] = ClassFactory(vals[0] + "List", vals[1], vals[2], BaseClass=generics.RetrieveUpdateDestroyAPIView)


class GameInstanceList(generics.ListCreateAPIView):
    queryset = GameInstance.objects.all()
    serializer_class = GameInstanceSerializer
    #permission_classes = (IsOwnerOrReadOnly)
    
    def get_queryset(self):
        queryset = GameInstance.objects.all()
        
        boardgame = self.request.QUERY_PARAMS.get('boardgame', None)
        location = self.request.QUERY_PARAMS.get('location', None)
        player = self.request.QUERY_PARAMS.get('player', None)
        
        if boardgame is not None:
            queryset = queryset.filter(boardgame__name=boardgame)
        
        if location is not None:
            queryset = queryset.filter(location__name=location)
        
        if player is not None:
            ps = queryset.filter(playerscore__player__name=player)
            pp = queryset.filter(playerplace__player__name=player)
            po = queryset.filter(playerorder__player__name=player)
            queryset = list(chain(pp, ps))

        return queryset
         
    def create(self, request, *args, **kwargs):
        data = json.loads(request.DATA['gi'])
        file = request.data['FILE']
        boardgame, _ = BoardGame.objects.get_or_create(name=data['boardgame'])
        location, _ = Location.objects.get_or_create(name=data['location'])
        
        gi, _ = GameInstance.objects.get_or_create(boardgame=boardgame,
                                           location=location,
                                           date=data['date'])
        
        if data.has_key('photo'):
            gi.photo = data['photo']
            
        for playerscore in data['playerscore']:
            newPlayer, _ = Player.objects.get_or_create(name=playerscore['player']['name'])
            createdPS, _ = PlayerScore.objects.get_or_create(player=newPlayer,
                                                          score=int(playerscore['score']))
            gi.playerscore.add(createdPS)
            
        for playerplace in data['playerplace']:
            newPlayer, _ = Player.objects.get_or_create(name=playerplace['player']['name'])
            createdPP, _ = PlayerPlace.objects.get_or_create(player=newPlayer,
                                                          place=int(playerplace['place']))
            gi.playerplace.add(createdPP)
        
        for playerorder in data['playerorder']:
            newPlayer, _ = Player.objects.get_or_create(name=playerplace['player']['name'])
            createdPO, _ = PlayerOrder.objects.get_or_create(player=newPlayer,
                                                          order=int(playerorder['order']))
            gi.playerorder.add(createdPO)
        
        serializer = GameInstanceSerializer(gi)
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
                        
         
    #def pre_save(self, obj):
    #    obj.poster = self.request.user


class GameInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameInstance.objects.all()
    serializer_class = GameInstanceSerializer
    #permission_classes = (IsOwnerOrReadOnly)
    
    #def pre_save(self, obj):
    #    obj.poster = self.request.user

@api_view(['GET',])
def api_root(request, format=None):
    apis = {'users': reverse('user-list', request=request, format=format),
            'gameinstances': reverse('gameinstance-list', request=request, format=format)}
    
    for key in AUTOMODELS.keys():
        apis[key] = reverse(key + '-list', request=request, format=format)
        
    return Response(apis)


"""     
class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    

class GenericList(APIView):
    def get(self, request, modeltype, format=None):
        genmodel, sermodel = get_models(modeltype)
        
        item = genmodel.objects.all()
        serializer = sermodel(item, many=True)
        return Response(serializer.data)
    
    def post(self, request, modeltype, format=None):
        _, sermodel = get_models(modeltype)
        
        data = JSONParser().parse(request)
        serializer = sermodel(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class GenericDetail(APIView):
    
    def get_object(self, genmodel, pk):
        try:
            return genmodel.objects.get(pk=pk)
        except genmodel.DoesNotExist:
            raise Http404
        
        
    def get(self, request, modeltype, pk, format=None):
        genmodel, sermodel = get_models(modeltype)
        
        item = self.get_object(genmodel, pk)
        serializer = sermodel(item)
        return Response(serializer.data)
    
    
    def put(self, request, modeltype, pk, format=None):
        genmodel, sermodel = get_models(modeltype)
        
        item = self.get_object(genmodel, pk)
        serializer = sermodel(item, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, modeltype, pk, format=None):
        genmodel, sermodel = get_models(modeltype)
        item = self.get_object(genmodel, pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def generic_detail(request, modeltype, pk, format=None):
    
    if not modeltype in ALLMODELS.keys():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    genmodel, sermodel = ALLMODELS[modeltype]
    
    try:
        item = genmodel.objects.get(pk=pk)
    except genmodel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = sermodel(item)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = sermodel(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genmodel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
""" 