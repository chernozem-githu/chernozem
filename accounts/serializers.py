from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import CustomUser
import random
from django.core.mail import send_mail


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'avatar', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        code = str(random.randint(100000, 999999))
        user.confirmation_code = code
        user.is_active = False
        user.save()

        send_mail(
            'Код подтверждения регистрации',
            f'Ваш код подтверждения: {code}',
            'from@example.com',  # или settings.DEFAULT_FROM_EMAIL
            [user.email],
            fail_silently=False,
        )
        return user



class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'avatar')
