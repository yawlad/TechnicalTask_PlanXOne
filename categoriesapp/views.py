from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin, RetrieveModelMixin
from .serializers import CategorySerializer, CategoryAdminSerializer
from .models import Category
from .filters import CategoryFilter
from django_filters.rest_framework import DjangoFilterBackend

from authapp.models import User

class CategoryViewSet(GenericViewSet, 
                  ListModelMixin,
                  DestroyModelMixin,
                  CreateModelMixin,
                  UpdateModelMixin,
                  RetrieveModelMixin):
    filter_backends = (DjangoFilterBackend,)
    queryset = Category.objects.all()
    filterset_class = CategoryFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        Category.objects.get(id=serializer.data['id']).set_user(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return CategoryAdminSerializer
        return CategorySerializer