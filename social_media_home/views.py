from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from social_media_home.models import Post, PostLike, PostComment
from . serializers import PostSerializer, PostLikeSerializer, PostCommentSerializer
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.all().filter(username=username).first()
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not check_password(password, user.password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_200_OK, data=get_tokens_for_user(user))


@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET': '/api/posts'},
        {'GET': '/api/posts/id'},
        {'GET': '/api/users'},
    ]

    return Response(routes)


class PostModelView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        instance = self.queryset.get(id=pk)
        if instance:
            return Response(self.serializer_class(instance).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            title = request.POST.get('title')
            body = request.POST.get('body')
            serializer.save()

            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.queryset.get(id=pk)
        if instance:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.queryset.get(id=pk)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostLikeViewSet(viewsets.ModelViewSet):
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None, *args, **kwargs):
        post_likes_objs = self.queryset.filter(postlike_post=pk)

        serializer = self.serializer_class(post_likes_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        postlike_id = Post.objects.get(id=request.data.get('id'))

        if postlike_id:
            self.queryset.create(postlike_user=request.user, postlike_post=postlike_id)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Not working
    def destroy(self, request, *args, **kwargs):
        postlike_id = Post.objects.get(id=request.data.get('id'))
        print(postlike_id)

        if postlike_id:
            postlike_obj = self.queryset.filter(postlike_user=request.user.id, postlike_post=postlike_id)
            postlike_obj.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        post_id = request.data.get('postid')
        post = Post.objects.get(id=post_id)
        # Not working
        if post:
            post_comment_obj = self.queryset.filter(postcomment_user=request.user, postcomment_post=post)
            serializer = self.serializer_class(post_comment_obj, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        post_id = request.data.get('postid')
        body = request.data.get('body')
        post = Post.objects.get(id=post_id)

        if post:
            self.queryset.create(postcomment_user=request.user, postcomment_post=post, body=body)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Not working yet..
    def destroy(self, request, *args, **kwargs):
        post_obj = Post.objects.get(request.data.get('post_id'))
        comment_obj = PostComment.objects.get(request.data.get('comment_id'))

        if post_obj and comment_obj:
            post_comment_obj = self.queryset.filter(postcomment_user=post_obj, postcomment_post=comment_obj)

            if post_comment_obj:
                post_comment_obj.delete()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)






