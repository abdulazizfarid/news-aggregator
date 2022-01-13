import uuid

from news.models import News, Query

news = []


def saveNewsToDb(data, source, queryId):
    news.clear()
    for obj in data:
        newsObj = News()
        newsObj.id = str(uuid.uuid4())
        newsObj.headline = obj.get("title")
        newsObj.link = obj.get("url")
        newsObj.source = source
        newsObj.queryId = queryId
        if newsObj.headline is not None:
            news.append(newsObj)
            newsObj.save()
    return news


def getNewsFromDb(queryId):
    news.clear()
    sqlQuery = Query.objects.raw("SELECT * FROM news_news WHERE queryId = %s", [queryId])
    for obj in sqlQuery:
        newsObj = News()
        newsObj.id = obj.id[0]
        newsObj.headline = obj.headline
        newsObj.link = obj.link
        newsObj.source = obj.source
        newsObj.queryId = obj.queryId
        if newsObj.headline is not None:
            news.append(newsObj)
    return news
