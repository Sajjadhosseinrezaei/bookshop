from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'publisher', views.PublisherViewSet, basename='publisher')


app_name = 'products'

urlpatterns = [
    path('api/', include(router.urls)),

]
