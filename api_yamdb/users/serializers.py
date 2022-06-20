from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = User
        extra_kwargs = {'email': {'required': True}}
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username')
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Имя me недопустимо!")
        return value


class ApiLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=159)
    confirmation_code = serializers.CharField(max_length=10)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User
        extra_kwargs = {
            'email': {'required': True},
            'confirmation_code': {'required': True}
        }


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
