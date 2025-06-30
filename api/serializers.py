# users/models.py (já temos)
# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import *
from core.models import *
from customers.models import *
from dashboard.models import *
from orders.models import *
from products.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'role', 'phone', 'avatar', 'theme', 'language', 'is_active']
        read_only_fields = ['id', 'is_active']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('Conta desativada.')
            else:
                raise serializers.ValidationError('Credenciais inválidas.')
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name', 'native_name', 'flag_icon', 
                 'is_active', 'is_default']

class TranslationSerializer(serializers.ModelSerializer):
    language_code = serializers.CharField(source='language.code', read_only=True)
    
    class Meta:
        model = Translation
        fields = ['id', 'key', 'value', 'context', 'language_code']