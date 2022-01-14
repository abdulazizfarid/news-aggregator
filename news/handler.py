import datetime
import random
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView
from .externalApis import getApiData
from .dbManager import getNewsFromDb
from .favorite import getFavorites, toggleFavorite
from .models import Query
from .serializers import NewsSerializer, FavSerializer

news = []
favs = []


def getQuery(queryRequest):
    queryRequest = str(queryRequest)
    start = queryRequest.find('\'') + 1
    end = queryRequest.find('\'', start)
    return queryRequest[start:end]


def queryExists(query_check):
    res = Query.objects.raw("SELECT id, count(*) AS row_count FROM news_query WHERE query = %s AND expiry > %s", (query_check, str(datetime.datetime.utcnow())))
    for val in res:
        if val.row_count > 0:
            return val.id
        elif val.row_count == 0:
            return False


def getResponse(request, query):
    news.clear()
    favs.clear()
    response = {}
    queryRequest = Query()
    queryRequest.id = str(uuid.uuid4())
    queryRequest.query = getQuery(request)
    if queryRequest.query.__contains__('favorite') and queryRequest.query.__contains__('user'):
        if queryRequest.query.__contains__('id'):
            response['status'] = 405
            response['message'] = 'Please ensure you\'re sending a POST request to toggle favorite'
            return response
        favs.clear()
        user = request.GET.get('user')
        favs.extend(getFavorites(user))
        serializer = NewsSerializer(favs, many=True)
        response['status'] = 200
        response['message'] = 'success'
        response['data'] = serializer.data
        return response

    queryRequest.expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    qId = queryExists(queryRequest.query)
    if queryExists(queryRequest.query):
        news.extend(getNewsFromDb(qId[0]))
    else:
        news.extend(getApiData(query, queryRequest.id))
        queryRequest.save()
    random.shuffle(news)
    serializer = NewsSerializer(news, many=True)
    response['status'] = 200
    response['message'] = 'success'
    response['news'] = serializer.data
    return response


def postResponse(request):
    favs.clear()
    response = {}
    user = request.GET.get('user')
    newsId = request.GET.get('id')
    if user is None or newsId is None:
        response['status'] = 404
        response['message'] = 'user or newsId not specified'
        response['data'] = 'Error'
        return response
    toggleFavorite(newsId, user)
    favs.extend(getFavorites(user, newsId))
    serializer = FavSerializer(favs, many=True)
    response['status'] = 200
    response['message'] = 'success'
    response['data'] = serializer.data
    return response
