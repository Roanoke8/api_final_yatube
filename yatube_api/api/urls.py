from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewsSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = 'api'

router = DefaultRouter()

router.register(
    'posts',
    PostViewSet,
    basename='posts'
)
router.register(
    r'posts/(?P<post_pk>\d+)/comments',
    CommentViewsSet,
    basename='comments'
)
router.register(
    'groups',
    GroupViewSet,
    basename='groups'
)
router.register(
    'follow',
    FollowViewSet,
    basename='follow'
)

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
