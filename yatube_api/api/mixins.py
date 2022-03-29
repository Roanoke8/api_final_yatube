from rest_framework import mixins, viewsets


class ListViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Миксин. HTTP_GET"""
    pass


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Миксиню HTTP_CREATE"""
    pass
