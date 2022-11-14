from rest_framework.serializers import ModelSerializer

from .models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    # def to_representation(self, value):
    #     return value.name

class CategoryAdminSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'