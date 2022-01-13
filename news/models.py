import uuid

from django.db import models


# Create your models here.


class News(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    headline = models.TextField()
    link = models.TextField()
    source = models.TextField()
    queryId = models.CharField(max_length=36)

    def __init__(self, id=str(uuid.uuid4()), headline=None, link=None, source=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id,
        self.headline = headline,
        self.link = link,
        self.source = source

    def __repr__(self):
        return "headline: %s\n link: %s\n source: %s\n" % (self.headline, self.link, self.source)

    def __str__(self):
        return '%s' % self.headline


class Query(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    query = models.TextField()
    expiry = models.DateTimeField()

    def __init__(self, id=str(uuid.uuid4()), query=None, expiry=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id,
        self.query = query,
        self.expiry = expiry

    def __str__(self):
        return '%s' % self.query


class favorite(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    newsId = models.CharField(max_length=36)
    user = models.TextField()
    favorite = models.BooleanField()
    time = models.DateTimeField()

    def __init__(self, id=str(uuid.uuid4()), newsId=None, user=None, favorite=None, time=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.newsId = newsId,
        self.user = user,
        self.favorite = favorite
        self.time = time

    def __str__(self):
        return '%s' % self.newsId
