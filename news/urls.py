from django.urls import path
from .views import NewsView

app_name = "news"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('news/', NewsView.as_view()),
    path('news/favorite', NewsView.as_view())
]
