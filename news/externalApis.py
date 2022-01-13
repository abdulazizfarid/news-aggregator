import requests

from projectFiles.settings import NEWSAPI_KEY, REDDIT_CLIENT_ID, REDDIT_SECRET_KEY
from news.dbManager import saveNewsToDb

news = []


def getNewsApi(query, queryId):
    if query is not None:
        r = requests.get(f'https://newsapi.org/v2/everything?apiKey={NEWSAPI_KEY}&q={query}')
    else:
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}')
    r_status = r.status_code
    # If it is a success
    if r_status == 200:
        data = r.json()
        articles = data.get("articles")
        news.extend(saveNewsToDb(articles, 'newsapi', queryId))


def getRedditApi(query, queryId):
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET_KEY)
    headers = {'User-Agent': 'MyBot/0.0.1'}

    r = requests.post('https://www.reddit.com/api/v1/access_token?grant_type=client_credentials', auth=auth,
                      headers=headers)
    TOKEN = r.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    if query is not None:
        r = requests.get('https://oauth.reddit.com/r/news/search/?q=' + query, headers=headers)
    else:
        r = requests.get('https://oauth.reddit.com/r/news/hot', headers=headers)

    r_status = r.status_code
    # If it is a success
    if r_status == 200:
        data = r.json()['data']['children']
        trueData = []
        for object in data:
            trueData.append(object.get("data"))
        news.extend(saveNewsToDb(trueData, 'reddit', queryId))


def getApiData(query, queryId):
    news.clear()
    getNewsApi(query, queryId)
    getRedditApi(query, queryId)
    return news
