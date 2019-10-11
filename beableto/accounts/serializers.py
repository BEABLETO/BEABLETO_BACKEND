from rest_framework import serializers
from .models import User
from rest_auth.serializers import TokenSerializer


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'phone', 'guardian_phone', 'aids', 'push_agree')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            guardian_phone=validated_data['guardian_phone'],
            aids=validated_data['aids'],
            push_agree=validated_data['push_agree'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class AuthTokenSerializer(TokenSerializer):
    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields



