from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from bgstatsdb.models import * 
from bgstatsdb.md_serializers import *
from bgstatsdb.permissions import IsOwnerOrReadOnly

AUTOMODELS = {'player':["Player", Player, PlayerSerializer],
             'boardgame':["BoardGame", BoardGame, BoardGameSerializer],
             'location':["Location", Location, LocationSerializer],
             'playerscore':["PlayerScore", PlayerScore, PlayerScoreSerializer],
             'playerplace':["PlayerPlace", PlayerPlace, PlayerPlaceSerializer],
             'user':["User", User, UserSerializer]}


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
    permission_classes = (IsOwnerOrReadOnly)
    
    def pre_save(self, obj):
        obj.poster = self.request.user


class GameInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameInstance.objects.all()
    serializer_class = GameInstanceSerializer
    permission_classes = (IsOwnerOrReadOnly)
    
    def pre_save(self, obj):
        obj.poster = self.request.user

@api_view(['GET',])
def api_root(request, format=None):
    apis = {'users': reverse('user-list', request=request, format=format),
            'gameinstances': reverse('gameinstance-list', request=request, format=format)}
    
    for key in AUTOMODELS.keys():
        apis[key + 's'] = reverse(key + '-list', request=request, format=format)
        
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