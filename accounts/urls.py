from django.urls import path, include
from . import views



urlpatterns = [
    path('create', views.UserCreateView.as_view(), name='create'),
    path('update', views.UserUpdateView.as_view(), name='update'),
    path('delete', views.UserDeleteView.as_view(), name='delete'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
]
