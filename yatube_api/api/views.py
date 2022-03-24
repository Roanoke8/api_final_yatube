from rest_framework import mixins, viewsets

from posts.models import Comment, Follow, Group, Post
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer

class ListViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    pass

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class GroupViewSet(ListViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class CommentViewsSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer