from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Follow, Group, Post, User

from .mixins import CreateViewSet, ListViewSet
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PostViewSet(viewsets.ModelViewSet):
    """Возвращает и редактирует объект модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Добавляет пользователя в качестве автора поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(ListViewSet):
    """Вьюсет Модели GROUP, наследуется от Миксина ListViewSet.
    Обрабатывает запросы GET."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class FollowViewSet(ListViewSet, CreateViewSet):
    """Вьюсет модели Follow. Обрабатывает типы запросов:
    GET, POST."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username', )

    def get_queryset(self):
        """Получает по related_name список подписок
        пользователя - инициатора запроса"""
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower.all()


class CommentViewsSet(viewsets.ModelViewSet):
    """Вьюсет модели Comment. Обрабатывает типы запроса:
    POST, GET, PATCH, DELETE"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """Принимает переданный в запросе ID поста.
        Возвращает все комментарии к посту или 404 если пост не найден."""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return post.comments.all()

    def perform_create(self, serializer):
        """Создает комментарий к посту. Принимает переданный в запросе ID поста.
        В качестве комментария указываем авторизованного инициатора запроса.
        Возвращает 404, если пост с ID не найден"""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)
