from common.exceptions import (
    CodeError,
    CodeExpiredOrInvalid,
    PhoneNumberAlreadyExists,
    PhoneNumberNotFound,
    PhoneNumberNotVerified,
)
from common.validators import validate_phone
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import UserProfile

User = get_user_model()


class AuthorizeSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_phone], min_length=12)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        phone = attrs["phone"]
        if User.objects.filter(phone=phone).exists():
            raise PhoneNumberAlreadyExists
        return attrs


class VerifySerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_phone])
    code = serializers.IntegerField()

    def validate_code(self, code):
        if code not in range(100000, 1000000):
            raise CodeError
        return code

    def validate(self, attrs):
        phone = attrs["phone"]
        code = attrs.pop("code")
        cache_data = cache.get(key=phone)
        if cache_data is None:
            raise CodeExpiredOrInvalid
        code_, value = cache_data
        if code_ != code:
            raise CodeExpiredOrInvalid
        match code_, value:
            case code_, None:
                cache.delete(key=phone)
                User.add_to_cache(key=phone, value=True, ttl=120)
            case code_, str():
                cache.delete(key=phone)
                attrs["password"] = value
            case _:
                raise CodeExpiredOrInvalid
        return attrs


class LoginSerializer(TokenObtainPairSerializer):
    pass


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_phone])

    def validate_phone(self, phone):
        if not User.objects.filter(phone=phone).exists():
            raise PhoneNumberNotFound
        return phone


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_phone])
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        phone = attrs.get("phone")
        value = cache.get(key=phone)
        cache.delete(key=phone)
        if value is None:
            raise PhoneNumberNotVerified
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'phone', 'name', 'email', 'default_shipping_address', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'phone']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        instance.save()
        return instance