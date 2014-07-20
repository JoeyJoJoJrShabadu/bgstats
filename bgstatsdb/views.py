from django.http import Http404
import sys
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics

from bgstatsdb.models import Player, BoardGame, Location, GameInstance, PlayerScore, PlayerPlace
from bgstats.md_serializers import PlayerSerializer, BoardGameSerializer, LocationSerializer, PlayerScoreSerializer, PlayerPlaceSerializer, GameInstanceSerializer

ALLMODELS = {'player':["Player", Player, PlayerSerializer],
             'boardgame':["BoardGame", BoardGame, BoardGameSerializer],
             'gameinstance':["GameInstance", GameInstance, GameInstanceSerializer],
             'location':["Location", Location, LocationSerializer],
             'playerscore':["PlayerScore", PlayerScore, PlayerScoreSerializer],
             'playerplace':["PlayerPlace", PlayerPlace, PlayerPlaceSerializer]}


def get_models(modeltype):
        if not modeltype in ALLMODELS.keys():
            raise Http404
        
        return ALLMODELS[modeltype]
    
def ClassFactory(name, qs, sc, BaseClass=generics.RetrieveUpdateDestroyAPIView):
    def __init__(self, **kwargs):
        setattr(self, 'queryset', qs.objects.all())
        setattr(self, 'serializer_class', sc)
        
        BaseClass.__init__(self)
    
    newclass = type(name, (BaseClass,),{"__init__":__init__})
    return newclass

for vals in ALLMODELS.values():
    vars()[vals[0] + "List"] = ClassFactory(vals[0] + "List", vals[1], vals[2], BaseClass=generics.ListCreateAPIView)
    vars()[vals[0] + "Detail"] = ClassFactory(vals[0] + "List", vals[1], vals[2], BaseClass=generics.RetrieveUpdateDestroyAPIView)
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