from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from .serializers import UserSerializer, UserAdminSerializer
from .models import User
from rest_framework.permissions import AllowAny
from djoser.views import UserViewSet

from categoriesapp.models import Category, StandartCategory

class MyUserViewSet(GenericViewSet,
                  ListModelMixin, 
                  UpdateModelMixin,
                  DestroyModelMixin,
                  RetrieveModelMixin):
    
    serializer_class = UserSerializer
    queryset = User.objects.filter()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return UserAdminSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()  
        return User.objects.filter(id=self.request.user.id)
        

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_deleted = True
        user.save()
        return Response(status=status.HTTP_200_OK)

class RegisterUserViewSet(UserViewSet):
    permission_classes = (AllowAny,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        for category in StandartCategory.objects.all():
            Category.objects.create(name=category.name, user=User.objects.get(id=serializer.data['id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

