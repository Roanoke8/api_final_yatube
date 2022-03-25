from django.shortcuts import get_object_or_404

from posts.models import Comment, Follow, Group, Post

from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
from .permissions import IsOwnerOrReadOnly

class ListViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
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
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class CommentViewsSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return post.comments.all()
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)