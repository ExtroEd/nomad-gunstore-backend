import random

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser
from apps.users.tasks import send_verification_email, clear_verification_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email',
            'phone_number',
            'use_phone_for_2fa',
            'sms_daily_deals',
            'password', 'confirm_password',
            'newsletter_subscription'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        code = f"{random.randint(100000, 999999)}"

        user = CustomUser.objects.create_user(
            **validated_data,
            is_active=False,
            verification_code=code
        )

        send_verification_email.delay(user.email, code)

        clear_verification_code.apply_async(
            args=[user.pk],
            countdown=600
        )

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'], password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError("Неверные email или пароль.")
        if not user.is_verified:
            raise serializers.ValidationError("Email не подтверждён.")

        data = super().validate(attrs)
        data.update({
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone_number', 'use_phone_for_2fa', 'sms_daily_deals',
            'is_active', 'is_staff', 'date_joined', 'newsletter_subscription'
        ]


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        if user.verification_code != data['code']:
            raise serializers.ValidationError("Неверный код.")

        user.is_active = True
        user.is_verified = True
        user.verification_code = None
        user.save()

        return data


class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
