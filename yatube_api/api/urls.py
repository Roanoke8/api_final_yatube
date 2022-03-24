from django.urls import  include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

app_name = 'api'

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('v1', include(router.urls))
]
