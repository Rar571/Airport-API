from rest_framework import generics

from user.serializers import UserSerializer


class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
