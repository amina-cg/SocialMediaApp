from rest_framework import serializers
from social_media_home.models import Post, PostLike, PostComment
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'

