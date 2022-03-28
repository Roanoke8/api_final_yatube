from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Follow, Group, Post

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()

class ListViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """TODO"""
    pass


class PostViewSet(viewsets.ModelViewSet):
    """Возвращает и редактирует объект модели Post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Добавляет пользователя в качестве автора поста."""
        serializer.save(author=self.request.user)



class GroupViewSet(ListViewSet):
    """TODO"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class FollowViewSet(viewsets.ModelViewSet):
    """TODO"""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        """TODO"""
        queryset = self.request.user.follower.filter()
        user = self.request.query_params.get('search')
        if user is not None:
            queryset = get_list_or_404(queryset.filter(following__username=user))
        return queryset
    
    def perform_create(self, serializer):
        """TODO"""
        follow = get_object_or_404(User, username=self.request.data['following'])
        serializer.save(
            user=self.request.user,
            following=follow
        )

    

class CommentViewsSet(viewsets.ModelViewSet):
    """TODO"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """TODO"""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return post.comments.all()
    
    def perform_create(self, serializer):
        """TODO"""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)