# News Aggregator

Refer to the task assigned by clicking [here](https://bitbucket.org/hamzamasroor/news-aggregator/src/master/ "News Aggregator")

## Solution

The program provides 5 main functionalities which fulfills the three parts given in the Task:

# Part 1
### i) Fetching aggregated data from NewsApi and Reddit
This is the basic functionality, where the user sends a GET request to [http://localhost:8000/api/news](http://localhost:8000/api/news "News")
<br>The program hits the [NewsApi](https://newsapi.org/v2/top-headlines?country=us "News") and fetches data from it, it then hits the [Reddit api](https://www.reddit.com/r/news/ "News") and fetches data from there.
<br>`Note: Both the APIs use a secret key for authentication which need to be defined in the environment variables in settings.py file`
<br>The output is displayed by merging and shuffling the results from both the Apis.
<br>A sample output is shown below:
> Request
    GET /api/news/
    <br>Accept: application/json
    
    > Response
    [
      {
        "status": 200,
        "message": "success",
        "news": [
          {
              "id": "e6a8061f-52fb-4b6d-a9e7-ea64e5f3f45a",
              "headline": "Rapper formerly known as Kanye West named main suspect in Los Angeles battery investigation",
              "link": "https://www.cbsnews.com/news/kanye-west-ye-suspect-battery-los-angeles/",
              "source": "reddit"
          },
          {
              "id": "e1b32d0f-e73a-4acf-89b1-c7e4022c6d16",
              "headline": "Model predicts COVID-19 in New Hampshire will rise through February, drop quickly - WMUR Manchester",
              "link": "https://www.wmur.com/article/model-prediction-covid-19-new-hampshire-cases-hospitalizations/38761252",
              "source": "newsapi"
          }
    ]
### ii) Fetching aggregated data along with a search query from APIs
This functionality extends the previous functionality to get only the data related to the search query defined by the user.
<br>It works by sending a GET request to the url with the query param `http://localhost:8000/api/news?query={SEARCHQUERY}`
<br>Example:
[http://localhost:8000/api/news?query=Fun](http://localhost:8000/api/news?query=Fun "News-Fun")
<br>Sample output:
> Request
    GET /api/news?query=Fun
    <br>Accept: application/json
    
    > Response
    [
      {
        "status": 200,
        "message": "success",
        "news": [
          {
            "id": "6bccfe83-d084-487a-a6c4-ba043433c3ce",
            "headline": "Musk, Dorsey Make Fun of Newest Internet Buzzword",
            "link": "https://www.entrepreneur.com/article/404280",
            "source": "newsapi"
          },
          {
              "id": "44ef50e9-3d86-4cd3-8a6c-d584b7d522a9",
              "headline": "It was fun while it lasted",
              "link": "https://i.redd.it/nxiaxm0lgja81.png",
              "source": "reddit"
          }
    ]
  
# Part 2:
### i) Fetching aggregated data from database
Here things start getting more interesting.
<br>To implement part 2, the program works by saving the request query to a database with an expiry of 5 minutes.
<br> For example, if the user hits `http://localhost:8000/api/news?query=Fun`, it would store `/api/news?query=Fun`
to the database.

<br>At each query request, the program hits the database to check whether the query exists in the database and is not expired. 
If it does indeed find the same query which hasn't expired, it retrieves the news saved in the database marked along with the
specific query Id (identifying the query request).

<br>If it does not find a query or if the query has expired, it re-hits the external apis to fetch and store their data in the database
along with the current query id (to identify which query the data belongs to) 

# Part 3:
### i) Marking/Unmarking a specific news item as favorite
Now that we're done with fetching the data, what if the user likes a particular news item and wishes to mark it as favorite?
<br>To do this, they simply have to send a POST request to url adding their name and the id of the news they wish to favorite in the params:
`http://localhost:8000/api/news/favorite?user={USERNAME}&id={POSTID}`
<br>Example:
[http://localhost:8000/api/news/favorite?user=AbdulAziz&id=44ef50e9-3d86-4cd3-8a6c-d584b7d522a9](http://localhost:8000/api/news/favorite?user=AbdulAziz&id=44ef50e9-3d86-4cd3-8a6c-d584b7d522a9)
<br>Output:
> Request
    POST /api/news/favorite?user=AbdulAziz&id=44ef50e9-3d86-4cd3-8a6c-d584b7d522a9
    <br>Accept: application/json
    
    > Response
    [
      {
        "status": 200,
        "message": "success",
       "data": [
            {
                "headline": "It was fun while it lasted",
                "link": "https://i.redd.it/nxiaxm0lgja81.png",
                "source": "reddit",
                "user": "AbdulAziz",
                "newsId": "44ef50e9-3d86-4cd3-8a6c-d584b7d522a9",
                "favorite": "True"
            }
       ]
    ]
<br>This works by essentially entering the username, the post id and whether or not the post is currently marked as favorite to the database in our new table `news_favorite`
<br>To unmark the post as favorite the user simply needs to run hit the same link again.
<br>For example, sending another POST request to [http://localhost:8000/api/news/favorite?user=AbdulAziz&id=44ef50e9-3d86-4cd3-8a6c-d584b7d522a9](http://localhost:8000/api/news/favorite?user=AbdulAziz&id=44ef50e9-3d86-4cd3-8a6c-d584b7d522a9)
would give the following output:
> Request
    POST /api/news/favorite?user=AbdulAziz&id=44ef50e9-3d86-4cd3-8a6c-d584b7d522a9
    <br>Accept: application/json
    
    > Response
    [
      {
        "status": 200,
        "message": "success",
       "data": [
            {
                "headline": "It was fun while it lasted",
                "link": "https://i.redd.it/nxiaxm0lgja81.png",
                "source": "reddit",
                "user": "AbdulAziz",
                "newsId": "44ef50e9-3d86-4cd3-8a6c-d584b7d522a9",
                "favorite": "False"
            }
       ]
    ]
### ii) Getting all the favorite items of a user
Finally, for our last task, we need to fetch all the favorite items of the user.
<br>This can easily be done, since we have the username in the favorites table.
<br>So we can simply fetch all the news ids of where the user is {user}, and then fetch all the news through the ids
<br>One small twist, we need to consider is the fact that we need to display the recently favorited posts first.
<br>To accomplish this, we must know when the user has marked a news item favorite.
<br>So we extend our favorites table in the database to include a time column, which would store the datetime of when
the user marked the particular item as favorite.
<br>Once we have the datetime, we can simply sort the results in descending order of our time column to get the most recent favorited posts first.

To get the results, we need to send a GET request to `http://localhost:8000/api/news/favorite?user={USERNAME}`
<br>For example, [http://localhost:8000/api/news/favorite?user=AbdulAziz](http://localhost:8000/api/news/favorite?user=AbdulAziz)
<br>would give us the following output:
> Request
    POST /api/news/favorite?user=AbdulAziz&id=44ef50e9-3d86-4cd3-8a6c-d584b7d522a9
    <br>Accept: application/json
    
    > Response
    [
      {
        "status": 200,
        "message": "success",
       "data": [
            {
                "id": "44ef50e9-3d86-4cd3-8a6c-d584b7d522a9",
                "headline": "It was fun while it lasted",
                "link": "https://i.redd.it/nxiaxm0lgja81.png",
                "source": "reddit"
            },
            {
                "id": "ff2a6c4a-e514-4e3f-bcd6-6899c9bf8e4f",
                "headline": "‘The economy cannot stay open’: Omicron’s effects ricochet across US",
                "link": "https://www.theguardian.com/us-news/2022/jan/12/us-omicron-cases-effects-schools-supply-shortage-hospitals",
                "source": "reddit"
            },
            {
                "id": "6f36a563-637c-4411-b69f-cf584d1fa72a",
                "headline": "Dow Jones Futures: Tesla, Growth Stocks Lead Market Sell-Off; JPMorgan Headlines Bank Earnings - Investor's Business Daily",
                "link": "https://www.investors.com/market-trend/stock-market-today/dow-jones-futures-tesla-roblox-growth-stocks-lead-market-sell-off-jpmorgan-headlines-bank-earnings/",
                "source": "newsapi"
            },
            {
                "id": "0d236d0d-453a-46ab-9a2a-c6298220a5ac",
                "headline": "Federal investigators say they used encrypted Signal messages to charge Oath Keepers leader",
                "link": "https://www.cnbc.com/2022/01/13/feds-say-they-used-encrypted-messages-to-charge-oath-keepers-leader.html",
                "source": "reddit"
            }
        ]
    ]
---
That's all for the solution.
For any queries feel free to contact me at `faridabdulaziz@ymail.com`



