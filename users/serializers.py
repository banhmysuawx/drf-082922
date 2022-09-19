import http
import imp
import re
from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "username"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        regex = "^(?=.{0}?[A-Z])(?=.*?[a-zA-Z0-9])(?=.*?[#?!@$ %^&*-]).{8}$"
        if re.match(regex, value) is None:
            raise ValidationError(
                "Password must must have 8 characters, first character is uppercase and have special character",
                http.HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        return value

    def validate_email(self, email):
        try:
            regex = "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
            if re.match(regex, email) is None:
                raise ValidationError("Email is not valid", http.HTTPStatus.UNPROCESSABLE_ENTITY)
            return email
        except ValidationError:
            raise ValidationError("Email is not valid", http.HTTPStatus.UNPROCESSABLE_ENTITY)

    def validate_username(self, username):
        try:
            if re.match(regex, username) is None:
                raise ValidationError(
                    "Username doesn't contains special characters or space ",
                    http.HTTPStatus.UNPROCESSABLE_ENTITY,
                )
            if User.objects.filter(username=username).exists():
                raise ValidationError(
                    "Username already exists", http.HTTPStatus.UNPROCESSABLE_ENTITY
                )
            regex = "^[a-zA-Z0-9]*$"
            print(username)
            return username
        except ValidationError as e:
            raise ValidationError(e, http.HTTPStatus.UNPROCESSABLE_ENTITY)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
