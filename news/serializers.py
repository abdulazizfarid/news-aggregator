from rest_framework import serializers


class NewsSerializer(serializers.Serializer):
    id = serializers.CharField()
    headline = serializers.CharField()
    link = serializers.CharField()
    source = serializers.CharField()


class FavSerializer(serializers.Serializer):
    headline = serializers.CharField()
    link = serializers.CharField()
    source = serializers.CharField()
    user = serializers.CharField()
    newsId = serializers.CharField()
    favorite = serializers.CharField()
