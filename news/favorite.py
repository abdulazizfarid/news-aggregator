import uuid
import datetime

from news.models import Query, favorite

favs = []


def toggleFavorite(newsId, user):
    result = Query.objects.raw("SELECT id, count(*) AS row_count FROM news_favorite WHERE newsId = %s AND user = %s", (newsId, user))
    for val in result:
        if val.row_count > 0:
            temp = favorite.objects.get(newsId=newsId, user=user)
            if temp.favorite:
                temp.favorite = False
            elif not temp.favorite:
                temp.favorite = True
            temp.newsId = temp.newsId[0]
            temp.user = temp.user[0]
            temp.save()
        else:
            temp = favorite()
            temp.id = uuid.uuid4()
            temp.favorite = True
            temp.newsId = newsId
            temp.user = user
            temp.time = datetime.datetime.utcnow()
            temp.save()


def getFavorites(user, newsId=None):
    favs.clear()
    sqlQuery = ''
    if newsId is None:
        sqlQuery = f'''SELECT nn.id, nn.headline, nn.link, nn.source, nf.user, nf.favorite FROM news_news nn
                        INNER JOIN news_favorite nf ON (nn.id=nf.newsId)
                        WHERE nn.id IN
                        (SELECT newsId FROM news_favorite
                        WHERE favorite=TRUE)
                        AND nf.user='{user}'
                        ORDER BY nf.time DESC;'''
    else:
        sqlQuery = f'''SELECT nn.id, nn.headline, nn.link, nn.source, nf.user, nf.favorite FROM news_news nn
                        INNER JOIN news_favorite nf ON (nn.id=nf.newsId)
                        WHERE nn.id = '{newsId}'
                        AND nf.user = '{user}';'''
    favQuery = Query.objects.raw(sqlQuery)
    for obj in favQuery:
        favObj = favorite()
        favObj.newsId = obj.id[0]
        favObj.headline = obj.headline
        favObj.link = obj.link
        favObj.source = obj.source
        favObj.user = obj.user
        favObj.favorite = bool(obj.favorite)
        if favObj.newsId is not None:
            favs.append(favObj)
    return favs
