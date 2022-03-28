from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """TODO"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """TODO"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    
    class Meta:
        fields = '__all__'
        read_only_fields = ('post',)
        model = Comment

class GroupSerializer(serializers.ModelSerializer):
    """TODO"""
    class Meta:
        fields = '__all__'
        model = Group

class FollowSerializer(serializers.ModelSerializer):
    """TODO"""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    validators = [
        UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('user', 'following'),
            message='Вы уже подписанны на данного пользователя'
        )
    ]

    def validate(self, data):
        """TODO"""
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'нельзя подписываться на самого себя!'
            )
        return data



    class Meta:
        fields = ('user', 'following')
        model = Follow
        