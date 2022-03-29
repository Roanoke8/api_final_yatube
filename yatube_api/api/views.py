from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Follow, Group, Post

from .mixins import CreateViewSet, ListViewSet
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


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

    def get_queryset(self):
        """Принимает передаваемое имя пользователя в
        запросе с ключем search.
        Если пользователь не найден возвращает 404"""
        queryset = self.request.user.follower.filter()
        user = self.request.query_params.get('search')
        if user is not None:
            queryset = get_list_or_404(
                queryset.filter(following__username=user)
            )
        return queryset

    def perform_create(self, serializer):
        """Получает имя пользователя передаваемое в запросе POST.
        Записывает в БД авторизованного инициатора запроса
        и имя пользователя в качестве подписки. Если автор не найден
        возваращает 404"""
        follow = get_object_or_404(
            User,
            username=self.request.data['following']
        )
        serializer.save(
            user=self.request.user,
            following=follow
        )


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
