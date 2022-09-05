import http
import imp
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed(detail="User not found")

        if not user.check_password(password):
            raise AuthenticationFailed(detail="Password is incorrect")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response({"jwt": token})

        response.set_cookie("token", token, httponly=True)

        response.data = {"jwt": token}

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("token")
        if token is None:
            raise AuthenticationFailed(detail="Token not found")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(detail="Token expired")

        serializer = UserSerializer(User.objects.get(id=payload["id"]))

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("token")
        response.data = {"message": "Logout successfully"}

        return response
