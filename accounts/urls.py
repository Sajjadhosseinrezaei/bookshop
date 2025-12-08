from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewset, basename='user')


urlpatterns = [
    path('', include(router.urls)),
]
