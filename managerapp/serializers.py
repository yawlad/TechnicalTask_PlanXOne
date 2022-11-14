from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Transaction
from categoriesapp.models import Category

class CategoryFilteredPrimaryKeyRelatedFiled(PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset=super(CategoryFilteredPrimaryKeyRelatedFiled, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)


class TransactionSerializer(ModelSerializer):
    category = CategoryFilteredPrimaryKeyRelatedFiled(queryset=Category.objects)
    class Meta:
        model = Transaction
        fields = ['id', 'category', 'money_amount', 'organization', 'description', 'datetime']

class TransactionAdminSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'