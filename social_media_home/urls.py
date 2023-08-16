from django.urls import path, include
from . views import get_routes, PostModelView, PostLikeViewSet, LoginViewSet, PostCommentViewSet
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register('posts', PostModelView, basename="posts")
router.register('posts_likes', PostLikeViewSet, basename="posts_likes")
router.register('login', LoginViewSet, basename="login")
router.register('posts_comments', PostCommentViewSet, basename="posts_comments")


urlpatterns = [
    path('', get_routes),
    path('', include(router.urls)),

]

