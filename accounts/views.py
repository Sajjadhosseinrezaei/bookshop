from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from .models import User
# Create your views here.



class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer