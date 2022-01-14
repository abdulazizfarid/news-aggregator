import datetime
import random
import uuid

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .externalApis import getApiData
from .dbManager import getNewsFromDb
from .favorite import getFavorites, toggleFavorite
from .handler import getResponse, postResponse
from .models import Query
from .serializers import NewsSerializer, FavSerializer

news = []
favs = []


class NewsView(APIView):
    def get(self, request):
        news.clear()
        favs.clear()
        response = {}
        query = self.request.query_params.get('query')
        response.update(getResponse(request, query))
        res = Response(response, response['status'])
        return res

    def post(self, request):
        news.clear()
        favs.clear()
        response = {}
        response.update(postResponse(request))
        return Response(response)
