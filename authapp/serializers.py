from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import User

class UserSerializer(ModelSerializer):
    balance = ReadOnlyField()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'balance']
   
class UserAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'    
        
    